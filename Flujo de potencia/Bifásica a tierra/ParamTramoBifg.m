clear all
clc

% Asigna las longitudes de cada uno de los tramos de la EEC
Long = [0.26386 9.910026 3.09144 7.97976 2.97622 3.41433 1.495 4.41558 3.73037 10.41391 7.695292 4.39497 8.025209 3.99747 5.70753 10.31599 7.45101]'; % Km

% Parámetros promedio línea
r1=(0.4153+0.8315*3)/4;
r0=(0.4148+0.8307*3)/4;
l1=(0.001327 + 0.001263 + 0.001096 + 0.001311)/4;
l0=(0.002029 + 0.002392 + 0.002727 + 0.002296)/4;

Rs=(2*r1+r0)/3;
Ls=(2*l1+l0)/3;

Xs=2*pi*60*Ls;
Zp=Rs+Xs*sqrt(-1);

Rm=(r0-r1)/3;
Lm=(l0-l1)/3;

Xm=2*pi*60*Lm;
Zm=Rm+Xm*sqrt(-1);

mx=[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; 0 0 0 0 0 0 0 0 0 0 6980 7330 16060 5120 10240 28640 9430 10130; 0 0 0 0 0 0 0 0 0 0 2040 2140 4690 1490 2990 8350 2750 2950; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]';

%Primero se definen los tramos de la troncal, luego los de las derivaciones

lx=[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17; 1 2 3 4 5 6 7 8 9 10 3 4 6 7 8 9 10; 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs; Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs]';
format shortG % Permite quitarle decimales innecesarios a los datos de algunas columnas

Sb=5e6;
Vbas=13500;

% Inicia la simulación del archivo de Simulink

find_system('Name','lineaEEC');
open_system('lineaEEC');
set_param(gcs,'SimulationCommand','Start');

pause(5) % Tiempo de espera en segundos para seguir ejecutando el código

% Primera aproximación método de Lubkeman

[Ipre]=flujo_carga_prefalla1(mx, lx, Sb, Vbas); % Fasores de corriente en prefalla

[Isub, Vsub]=fasores_posfalla1(Vsubes,Isubes,tout); % Fasores de corriente en posfalla

% ==============================================================================================

% Corriente de falla inicial (suposición)

% ====    Falla en fase A y B a tierra

Ifa=Isub(1)-Ipre(1,1); % Para fase A
Ifb=Isub(2)-Ipre(1,2); % Para fase B

x0=Zp*Isub(1) + Zm*Isub(2) + Zm*Isub(3);
x1=Zm*Isub(1) + Zp*Isub(2) + Zm*Isub(3);

% Matriz de coeficientes
Vab=[real(Vsub(1)) imag(Vsub(1)) real(Vsub(2)) imag(Vsub(2))]';

% Matriz inversa
Fab=inv([real(x0) real(Ifa) 0 real(Ifa+Ifb); imag(x0) imag(Ifa) 0 imag(Ifa+Ifb); real(x1) 0 real(Ifb) real(Ifa+Ifb); imag(x1) 0 imag(Ifb) imag(Ifa+Ifb)]);

% Cálculo de Distancia D
Res= Fab * Vab;
Res(1)

% ================================================================================================

% Corriente de falla inicial (suposición)

% ====    Falla en fase B y C a tierra

Ifb=Isub(2)-Ipre(1,2); % Para fase B
Ifc=Isub(3)-Ipre(1,3); % Para fase C

x0=Zm*Isub(1) + Zp*Isub(2) + Zm*Isub(3);
x1=Zm*Isub(1) + Zm*Isub(2) + Zp*Isub(3);

% Vector de coeficientes
Vbc=[real(Vsub(2)) imag(Vsub(2)) real(Vsub(3)) imag(Vsub(3))]';

% Matriz inversa
Fbc=inv([real(x0) real(Ifb) 0 real(Ifb+Ifc); imag(x0) imag(Ifb) 0 imag(Ifb+Ifc); real(x1) 0 real(Ifc) real(Ifb+Ifc); imag(x1) 0 imag(Ifc) imag(Ifb+Ifc)]);

% Cálculo de Distancia D
Res= Fbc* Vbc;
Res(1)

% ================================================================================================

% Corriente de falla inicial (suposición)

% ====    Falla en fase A y C a tierra

Ifa=Isub(1)-Ipre(1,1); % Para fase A
Ifc=Isub(3)-Ipre(1,3); % Para fase C

x0=Zp*Isub(1) + Zm*Isub(2) + Zm*Isub(3);
x1=Zm*Isub(1) + Zm*Isub(2) + Zp*Isub(3);

% Vector de coeficientes
Vac=[real(Vsub(1)) imag(Vsub(1)) real(Vsub(3)) imag(Vsub(3))]';

% Matriz inversa
Fac=inv([real(x0) real(Ifa) 0 real(Ifa+Ifc); imag(x0) imag(Ifa) 0 imag(Ifa+Ifc); real(x1) 0 real(Ifc) real(Ifa+Ifc); imag(x1) 0 imag(Ifc) imag(Ifa+Ifc)]);

% Cálculo de Distancia D
Res= Fac* Vac;
Res(1)
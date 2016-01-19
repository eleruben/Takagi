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

Z1=Zm-Zm; % Zm: impedancia mutua entre fases, Zp: impedancia propia de la fase
Z2=Zp-Zm;
Z3=Zm-Zp;

x1=Isub(1)*( (2/3)*Zp-(1/3)*Zm-(1/3)*Zm) + Isub(2)*( (2/3)*Zm -(1/3)*Zp-(1/3)*Zm) + Isub(3)*( (2/3)*Zm-(1/3)*Zm-(1/3)*Zp);
x2=Isub(1)*(-(1/3)*Zp+(2/3)*Zm-(1/3)*Zm) + Isub(2)*(-(1/3)*Zm +(2/3)*Zp-(1/3)*Zm) + Isub(3)*(-(1/3)*Zm+(2/3)*Zm-(1/3)*Zp);
x3=Isub(1)*(-(1/3)*Zp-(1/3)*Zm+(2/3)*Zm) + Isub(2)*(-(1/3)*Zm -(1/3)*Zp+(2/3)*Zm) + Isub(3)*(-(1/3)*Zm-(1/3)*Zm+(2/3)*Zp);

% Matriz de coeficientes
C=[real(x1) 2/3 -1/3 -1/3; imag(x1) 2/3 -1/3 -1/3; real(x2) -1/3 2/3 -1/3; imag(x2) -1/3 2/3 -1/3; real(x3) -1/3 -1/3 2/3; imag(x3) -1/3 -1/3 2/3;];

% Constantes
k1= (2/3)*Vsub(1) - (1/3)*Vsub(2) - (1/3)*Vsub(3);
k2=-(1/3)*Vsub(1) + (2/3)*Vsub(2) - (1/3)*Vsub(3);
k3=-(1/3)*Vsub(1) - (1/3)*Vsub(2) + (2/3)*Vsub(3);

% Matriz de constantes
K=[real(k1) imag(k1) real(k2) imag(k2) real(k3) imag(k3)]';

% Cálculo de Distancia D
Res= inv(C'*C) * C' * K;
Res(1)
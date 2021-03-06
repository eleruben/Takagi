clear all
clc

% Asigna las longitudes de cada uno de los tramos de la EEC
Long = [0.26386 9.910026 3.09144 7.97976 2.97622 3.41433 1.495 4.41558 3.73037 10.41391 7.695292 4.39497 8.025209 3.99747 5.70753 10.31599 7.45101]'; % Km

% Par�metros promedio l�nea
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

find_system('Name','lineaEEC');
open_system('lineaEEC');
set_param(gcs,'SimulationCommand','Start');

pause(5) % Tiempo de espera en segundos para seguir ejecutando el c�digo

% Primera aproximaci�n m�todo de Lubkeman

[Ipre]=flujo_carga_prefalla1(mx, lx, Sb, Vbas);

[Isub, Vsub]=fasores_posfalla1(Vsubes,Isubes,tout);

% =========================================================================================

% Corriente de falla inicial (suposici�n)

% Falla en fase A a tierra

If=Isub(1)-Ipre(1,1);

x=Zp*Isub(1) + Zm*Isub(2) + Zm*Isub(3);

% Vector de tensiones fase-neutro
Va=[real(Vsub(1)) imag(Vsub(1))]';

% Matriz de coeficientes
Fa=[real(x) real(If); imag(x) imag(If)];

% C�lculo de Distancia D
Res= inv(Fa) * Va;

D=Res(1);

% =========================================================================================

% Corriente de falla inicial (suposici�n)

% Falla en fase B a tierra

If=Isub(2)-Ipre(1,2);

x=Zm*Isub(1) + Zp*Isub(2) + Zm*Isub(3);

% Vector de tensiones fase-neutro
Vb=[real(Vsub(2)) imag(Vsub(2))]';

% Matriz de coeficientes
Fb=[real(x) real(If); imag(x) imag(If)];

% C�lculo de Distancia D
Res= inv(Fb) * Vb;

D=Res(1);

% =========================================================================================

% Corriente de falla inicial (suposici�n)

% Falla en fase C a tierra

If=Isub(3)-Ipre(1,3);

x=Zm*Isub(1) + Zm*Isub(2) + Zp*Isub(3);

% Vector de tensiones fase-neutro
Vc=[real(Vsub(3)) imag(Vsub(3))]';

% Matriz de coeficientes
Fc=[real(x) real(If); imag(x) imag(If)];

% C�lculo de Distancia D
Res= inv(Fc) * Vc;

D=Res(1);

% ==================================================================================
% ==================================================================================

D

for i=1:3
    for j=1:3
        if i==j
            Z(i,j)=Zp;
        else
            Z(i,j)=Zm;
        end
    end
end

Vnf=Vsub.'-D*Z*Isub.';

Vnf

abs(Vnf)

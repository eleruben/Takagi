clear all
clc

% Asigna las longitudes de cada uno de los tramos de la EEC
Long = [0.26386 9.910026 3.09144 7.97976 2.97622 3.41433 1.495 4.41558 3.73037 10.41391 7.695292 4.39497 8.025209 3.99747 5.70753 10.31599 7.45101]'; % Km

% Parámetros promedio línea
r1=(0.4153+0.8315*3)/4;
r0=(0.4148+0.8307*3)/4;
l1=(0.001327 + 0.001263 + 0.001096 + 0.001311)/4;
l0=(0.002029 + 0.002392 + 0.002727 + 0.002296)/4;

Rs=((2*r1+r0)/3);
Ls=((2*l1+l0)/3);

Xs=2*pi*60*Ls;
Xs=Ls;
z=Rs+Ls*sqrt(-1);
Z=z;

Zreal=real(Z);
Zimag=imag(Z);

mx=[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; 0 0 0 0 0 0 0 0 0 0 6980 7330 16060 5120 10240 28640 9430 10130; 0 0 0 0 0 0 0 0 0 0 2040 2140 4690 1490 2990 8350 2750 2950; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]';

% Primero se definen los tramos de la troncal, luego los de las derivaciones

lx=[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17; 1 2 3 4 5 6 7 8 9 10 3 4 6 7 8 9 10; 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs Rs; Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs Xs]';
format shortG % Permite quitarle decimales innecesarios a los datos de algunas columnas

Sb=5e6;
Vbas=13500;

ntramos=length(Long);

% Inicia la simulación del archivo de Simulink

find_system('Name','lineaEEC');
open_system('lineaEEC');
set_param(gcs,'SimulationCommand','Start');

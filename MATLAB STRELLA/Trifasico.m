% CALCULA CORTO CIRCUITOS TRIFASICOS EN CADA NODO DEL CIRCUITO
% Variables de entrada
% Informacion de tramos
% nodoP : Nodo inicial (aguas arriba, el mas cercano a la subestacion)
% nodoQ : Nodo final (aguas abajo, el mas lejano)
% Zabc  : Matriz de impedancia del tramo
% Z012  : Impedancias de secuencia (012) del tramo
% Long  : Longitud del tramo (km)
% PInst : Potencia instalada en el nodoQ (usada para calcular Sd)
% Usuarios : No. de usuarios conectados en nodoQ
% Sd    : Potencia de carga del nodoQ
% Nombres : Nombre del nodoQ
%
% dV    : delta de voltaje en el tramo
%
% Variables globales
% tramos: Numero de tramos
% nodos : Numero de nodos
% Vs    : Voltaje equivalente de la subestacion
% zth   : Impedancia equivalente de Thevenin del sistema de potencia
%         (Impedancia fuente)
% Ss    : Potencia medida en la subestacion
% Perd  : Perdidas de potencia (compleja)
% epsV  : Maximo cambio de voltaje permitido
%         (Controla la convergencia)
% epsP  : Error permisible de balance de potencia
% iter  : Numero de iteraciones
%
%zth = 0.05;%+0.05j;
%zth = 0.0232+0.0582j;
clear
zth = 0.0206 + 0.0328i;
zth1 = zth;
zth0 = zth
%Ss = 2.0801+1.2771j;
%Ss = 1.97+0.93j;
% Lee datos de tramos para el circuito
load tramos.mat;
% Determina el numero de tramos
Tramos = size(tramos,2);
% Determina el numero de nodos
nodos = Tramos+1;
ZABC = zeros(3,3,nodos);
Zsec = zeros(3,nodos);
% Calcula las matrices de impedancia nodales 

%
% Completar
%
save('Zmatrix.mat','Zsec','ZABC');
Zsec

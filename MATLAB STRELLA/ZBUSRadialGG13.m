% CALCULA MATRICES DE IMPEDANCIA NODALES (EQUIVALENTES THEVENIN)
% PARA CORTO CIRCUITO
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
SBase=1;% 1 MVA
VBase = 11.4; % 11.4 kV
IBase = SBase/(VBase*sqrt(3))
ZBase = VBase^2/SBase
zth = (0.0206 + 0.0328i)/ZBase
zth1 = zth;
zth0 = zth
%Ss = 2.0801+1.2771j;
%Ss = 1.97+0.93j;
% Lee datos de tramos para el circuito
load GG3A_2.mat;
% Determina el numero de tramos
Tramos = size(tramos,2);
% Determina el numero de nodos
nodos = Tramos+1;
ZABC = zeros(3,3,nodos);
Zsec = zeros(3,nodos);
% Calcula las matrices de impedancia nodales 
ZABC(:,:,1) = diag([zth zth zth]);
Zsec(:,1) = [zth0 zth1 zth1].';

for k=1:Tramos
   Zabck = tramos(k).Zabc;
   Z012k = tramos(k).Z012'
   NodAnt = tramos(k).nodoP;
   Nodo = tramos(k).nodoQ;
	ZABC(:,:,Nodo) = ZABC(:,:,NodAnt)+Zabck;
	Zsec(:,Nodo) = Zsec(:,NodAnt)+Z012k;
end
save('ZmatrixGG3A.mat','Zsec','ZABC','nodos','Tramos','ZBase','SBase','VBase','IBase');
Zsec


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
% 
% Variables globales
% nTramos: Numero de tramos
% nodos : Numero de nodos
% Vs    : Voltaje equivalente de la subestacion
% zth   : Impedancia equivalente de Thevenin del sistema de potencia
%         (Impedancia fuente)
% Ss    : Potencia medida en la subestacion
% Perd  : Perdidas de potencia (compleja)
% iter  : Numero de iteraciones
%
% Lee datos de tramos para el circuito
load tramos.mat;
% Determina el numero de tramos
nTramos = size(tramos,2);
% Determina el numero de nodos
nNodos = nTramos+1;
ZABC = zeros(3,3,nNodos);
Zsec = zeros(3,nNodos);
% Calcula las matrices de impedancia nodales 
ZABC(:,:,1) = diag([zth zth zth]);
Zsec(:,1) = [zth0 zth1 zth1]';

for k=1:nTramos
   NodAnt = tramos(k).nodoP;
   Nodo = tramos(k).nodoQ;
	ZABC(:,:,Nodo) = ZABC(:,:,NodAnt)+tramos(k).Zabc;
	Zsec(:,Nodo) = Zsec(:,NodAnt)+tramos(k).Z012';
end
save('Zmatrix.mat','Zsec','ZABC','nNodos','nTramos','Zbase');
Zsec

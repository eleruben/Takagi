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
zth = 0.1211 + 0.55555i;
zth1 = zth;
zth0 = 0.03650+0.23917i;
%Ss = 2.0801+1.2771j;
%Ss = 1.97+0.93j;
% Lee datos de tramos para el circuito
load tramos.mat;
% Determina el numero de tramos
Tramos = size(tramos,2);
% Determina el numero de nodos
nodos = Tramos+1;
ZABC = zeros(3,3,nodos);
ZABC(:,:,1) = diag([zth0 zth1 zth1]);
Zseq = zeros(3,nodos);
Zsec = zeros(3,nodos);
Dist = zeros(nodos,1);
Dist(1) = 0.0;
Zsec(:,1) = [zth; zth; zth];
% Calcula las matrices de impedancia nodales 
for k=1:Tramos
   Zseq(:,k) = tramos(k).Z012';
   Long(k) = tramos(k).Longitud;
end
for k=1:Tramos
   NodAnt = tramos(k).nodoP;
   Nodo = tramos(k).nodoQ;
   Zsec(:,Nodo) = Zsec(:,NodAnt)+Zseq(:,k);
   Dist(Nodo) = Dist(NodAnt)+Long(k);
end
%
% 	Flujo de carga radial
%

%
%	Calculo de corrientes de corto circuito
% 
for RF=0:0.025:0.05
	%La corriente de corto circuito para la fase a 
   %Se supone Vth=1 en el  nodo en falla 
   % (mejor usar el voltaje del flujo de carga)
   Icc=V./(Zsec(2,:)+RF);
   % Icc = V./(Zsec(2,:)+RF)
   %	Aqui sumar las corrientes de carga, obtenidas en el 
   %  Flujo de carga
   %  ISE = IcargaSE+Icc;
   %	V = Voltaje prefalla
   % 
   Zeq = Zsec(2,:)+RF;
   ZMag = abs(Zeq);
   ZAng = angle(Zeq);
%	subplot(3,1,1)
%  plot(Icc,'r*')
	plot(Dist,real(Zeq),'r.');
%	subplot(3,1,2)
%	plot(Dist,ZMag,'b.');	
%	subplot(3,1,3)
%  plot(Dist,ZAng,'g.');
   pause
end

save('Zmatrix.mat','Zsec','ZABC','Zsec','Icc');
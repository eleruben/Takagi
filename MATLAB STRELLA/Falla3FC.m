% Cortocircuito trifasico, junto con 
% FLUJO DE CARGA RADIAL
% Variables de entrada
% Informacion de tramos
% nodoP : Nodo inicial (aguas arriba, el mas cercano a la subestacion)
% nodoQ : Nodo final (aguas abajo, el mas lejano)
% z     : Impedancia serie del tramo
% PIns  : Potencia instalada en el nodoQ (usada para calcular Sd)
% Sd    : Potencia de carga del nodoQ
% dV    : delta de voltaje en el tramo
%
% Variables nodales
% V     : Voltaje complejo actual
% Vant  : Voltaje complejo anterior
% S     : Potencia neta del nodo
% PInst : Potencia instalada en el nodo (usada para calcular Sd)
% Id    : Corriente equivalente de la carga del nodo
% I     : Corriente acumulada en el nodo
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
zth = 0.0232+0.0582j;
SBase=1;
VBase = 11.400;
ZBase = VBase^2/SBase;
zth = (0.0206 + 0.0328i)/ZBase;
Vs = 1;
%Ss = 2.0801+1.2771j;
%Ss = 1.97+0.93j;
load tramos.mat
load Zmatrix.mat
nLineas = nTramos+1;
nNodos = nLineas+1;
% 	Leer datos de carga
Sdem = zeros(1,nNodos);
dV = zeros(1,nTramos);
V = ones(1,nNodos);
Vant = zeros(1,nNodos);
epsV = 1e-5;
epsP = 1e-5;
% Estimacion inicial de perdidas
PInstal(1) = 0;
PInstal(2) = 0;
divP(1) = 0;
divP(2) = 0;
NodP(1) = 1;
NodQ(1) = 2;
NodP(2) = 2;
NodQ(2) = 3;
z1(1) = zth;
z0(1) = zth;
z2(1) = zth;
for k=1:nTramos
   Pinstal(k+2) = tramos(k).Pinst/1000;
   NodP(k+1) = tramos(k).nodoP+1;
   NodQ(k+1) = tramos(k).nodoQ+1;
   z1(k+1) = tramos(k).Z012(2);
   z2(k+1) = tramos(k).Z012(3);
   z0(k+1) = tramos(k).Z012(1);
end
Ss = sum(Pinstal);
CargaSE = 0.6*(0.95+sin(acos(0.95))*j)*Ss/SBase;
Perd = 0.025*CargaSE;
PerA = 0;
pasos=0;
for k=1:nLineas
   divP(NodQ(k)) = Pinstal(k)/Ss;
end
while abs(Perd-PerA) > epsP & pasos < 1
   pasos = pasos+1;
   Sdem = (CargaSE-Perd)*divP;
   V = ones(1,nNodos)*Vs;
   Vant = V*0.0;
   iter = 0;
   while max(abs(V-Vant)) > epsV &  iter < 9
       iter = iter+1;
       Vant = V;
       Id = conj(Sdem./V);
       I = Id(2:nNodos);
       for k=nLineas:-1:2
           I(NodP(k)-1) = I(NodP(k)-1)+I(NodQ(k)-1);
       end
       dV = I.*z1;
       V(2) = Vs-dV(1);
       for k=2:nLineas
           V(NodQ(k)) = V(NodP(k))-dV(k);
       end
   end
   Ssac = Vs*conj(I(1));
   PerA = Perd;
   Perd = Ss-Ssac;
end
ISE = I(1);
% Calcula cortocircuitos trifasicos en cada nodo
for z=0.001:0.5:5
    Zf = z/ZBase;
    I3p = zeros(1,nNodos);
    V3p = zeros(1,nNodos);
    Z3p = zeros(1,nNodos);
    I3p(1) = 1;
%    for k=2:nNodos
%        I3p(k) = V(k)/(Zsec(1,k)+Zf)+ISE;
%        V3p(k) = V(1)-Zsec(1,1)*I3p(k);
%        Z3p(k) = V3p(k)/I3p(k);    
%    end
    I3p = V./(Zsec(2,:)+Zf)+ISE;
    I3psin = V./(Zsec(2,:)+Zf);
    V3p = V(1)-Zsec(2,1)*I3p;
    Z3p = V3p./I3p;
    Z3psin = V3p./I3psin;
    plot( DistASE,imag(Z3p),'.',DistASE,imag(Z3psin),'r.')
    axis([0 14 0 0.05])
    pause
%    plot( imag(Zsec(2,:)),imag(Z3psin),'.')
%    axis([0 0.05 0 0.05])
%    pause
end
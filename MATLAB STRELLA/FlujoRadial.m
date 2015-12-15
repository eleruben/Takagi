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
%zth = 0.0232+0.0582j;
clear;
zth = 0.0206 + 0.0328i;
Vs = 1;
%Ss = 2.0801+1.2771j;
%Ss = 1.97+0.93j;
[tramos,nodoP,nodoQ,z,PInst]=LeeTramos(zth);
Ss = sum(PInst)*1.2;
nodos=tramos+1;

Sd = zeros(1,nodos);
dV = zeros(1,tramos);
epsV = 1e-5;
epsP = 1e-5;
% Estimacion inicial de perdidas
Perd = 0.025*Ss;
PerA = 0;
divP = PInst/sum(PInst);
pasos=0;
while abs(Perd-PerA) > epsP & pasos < 1
   pasos = pasos+1;
   Sd = (Ss-Perd)*divP;
   V = ones(1,nodos)*Vs;
   Vant = V*0;
   iter = 0;
   while max(abs(V-Vant)) > epsV &  iter < 10
       iter = iter+1;
       Vant = V;
       Id = conj(Sd./V);
       I = Id(2:nodos);
       for k=tramos:-1:2
           I(nodoP(k)-1) = I(nodoP(k)-1)+I(nodoQ(k)-1);
       end
       dV = I.*z;
       for k=1:tramos
           V(nodoQ(k)) = V(nodoP(k))-dV(k);
       end
   end
   Ssac = Vs*conj(I(1));
   PerA = Perd;
   Perd = Ss-Ssac;
end
V
dlmwrite('salida.txt', [ abs(V); 180*angle(V)/pi]', '\t');
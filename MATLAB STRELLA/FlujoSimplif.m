% FLUJO DE CARGA RADIAL Simplificado
% Supone conocida la corriente en la subestacion
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
% S     : Potencia neta del nodo
% PInst : Potencia instalada en el nodo (usada para calcular Sd)
% Id    : Corriente equivalente de la carga del nodo
% I     : Corriente acumulada en el nodo
% 
% Variables globales
% nTramos: Numero de tramos
% nNodos : Numero de nodos
% Vsub  : Voltaje equivalente de la subestacion
% zth   : Impedancia equivalente de Thevenin del sistema de potencia
%         (Impedancia fuente)
% Ss    : Potencia medida en la subestacion
% Perd  : Perdidas de potencia (compleja)
% epsV  : Maximo cambio de voltaje permitido
%         (Controla la convergencia)
% epsP  : Error permisible de balance de potencia
% iter  : Numero de iteraciones
%% Corriente medida prefalla (usamos el primer valor de IA)
Isub = Ifase(1,2);
%Isub = I1(2);
% Voltaje medido prefalla (usamos el primer valor de VA)
Vsub = Vfase(1,2);
I = zeros(1,nTramos);
ITramo = zeros(1,nTramos);
% Calcula factores de distribucion de corrientes. Suponemos que todas estan en fase
for k=1:nTramos
   Pinstal(k) = tramos(k).PInst/1000;
   NodP(k) = tramos(k).nodoP;
   NodQ(k) = tramos(k).nodoQ;
   z1(k) = tramos(k).Z012(2);
   z2(k) = tramos(k).Z012(3);
   z0(k) = tramos(k).Z012(1);
end
k0 = (z0-z1)./(3*z1);
Ss = sum(Pinstal);
divP=zeros(1,nNodos);% 
for k=1:nTramos
   divP(1,NodQ(k)) = Pinstal(k)/Ss;
end
Id = Isub*divP;
I = Id;
for k=nTramos:-1:1
   I(NodP(k)) = I(NodP(k))+I(NodQ(k));
   ITramo(k) = I(NodP(k));
end
dV = ITramo.*z1;
Itransf = I(1);
V(1) = Vsub;
for k=1:nTramos
   V(NodQ(k)) = V(NodP(k))-dV(k);
end
% Almacena  valores de voltaje y corriente en S/E
% para ajustar los valores durante la falla
ISE = ITramo(1); 
plot(abs(V))

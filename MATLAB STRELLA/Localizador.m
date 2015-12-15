% LOCALIZADOR DE FALLAS EN CIRCUITOS DE DISTRIBUCION
% Utiliza la informacion sobre el circuitoSupone conocida la corriente en la subestacion
% Variables de entrada
% Informacion de tramos
%
% Variables nodales
% V     : Voltaje complejo actual
% S     : Potencia neta del nodo
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
%
% Lee TODOS los datos del circuito (tramos)
%     nodoP : Nodo inicial (aguas arriba, el mas cercano a la subestacion)
%     nodoQ : Nodo final (aguas abajo, el mas lejano)
%     Zabc  : Impedancia serie  (fase) del tramo
%     Z012  : Impedancia serie (secuencia) del tramo
%     Longitud
%     PInst : Potencia instalada en el nodo (usada para calcular Sd)
%     Usuarios
%     Sd
%     Nombres
%     zth1  : Impedancia Thevenin equivalente, especificada sec. +
%     zth2  : Impedancia Thevenin equivalente, especificada sec. -
%     zth0  : Impedancia Thevenin equivalente, especificada sec. 0
% Las matrices de impedancia nodal calculadas
%    Zsec
%    ZABC
%    nNodos
%    nTramos
%    Zbase
load DatosCircuito.mat
% Procesa mediciones de corrientes y voltajes de la falla
FasoresLineaATierra
% Calcula flujo de carga simplificado
FlujoSimplif
ISEfase = [ISE ; ISE*a^2 ; ISE*a];
VSE = Vsub; 
VSEfase = [VSE; VSE*a^2; VSE*a];
% Voltaje medido posfalla (usamos el 7o. valor de VA)
VsubFalla = Vfase(1,Ciclo);
IFalla = Ifase(:,Ciclo);
% Forma vectores de corrientes de carga estimadas durante la falla
% Considera una variacion de las corrientes proporcional a
%  (VoltajeDeFalla/VoltajePreFalla)^npot
npot = 1
%npot = 2
%npot = 0.5
FactorDeI = (abs(VsubFalla)/abs(Vsub))^npot;
ITramoFalla = ITramo*FactorDeI;
ISEFalla = ISEfase*FactorDeI;
IdFalla = Id*FactorDeI;
Isup=IFalla-ISEFalla;
% Localiza la falla
% FLReactancia
% FLTakagi
FLGeneral
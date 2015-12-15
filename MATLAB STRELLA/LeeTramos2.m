function [tramos,nodoP,nodoQ,z,PInst]=LeeTramos(zth)
% Lee los datos del sistema y los guarda en la forma requerida
% (Remplazar por una rutina de lectura en el caso general)
% Los tramos deben ir ordenados de manera que el 
% nodoP ya haya sido incluido.
% Para ello, basta ordenar los nodos empezando por la subestacion
% y continuar con tramos conectados a algun nodo ya existente.
% El primer tramo SIEMPRE debe ser el equivalente thevenin.
% La subestacion SIEMPRE debe ser el nodo numero 1
%
% Por lo tanto, las siguientes instrucciones siempre deben estar 
% incluidas:
PInst(2) = 0;
nodoP(1) = 1;
nodoQ(1) = 2;
z(1) = zth;
%
%tramos,nodoP,nodoQ,z,PInst
tramos = 3;
PInst(2) = 0;
nodoP(2) = 2;
nodoQ(2) = 3;
PInst(3) = 1+.4j;
z(2) = 0.0165 + 0.0262i;
nodoP(3) = 2;
nodoQ(3) = 4;
PInst(4) = 0.9+.45j;
z(3) = 0.0197 + 0.0205i;

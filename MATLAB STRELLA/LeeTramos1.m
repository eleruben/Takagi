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
% El resto de datos si son los de los tramos reales
%
PInst(2) = 1.1;
nodoP(2) = 2;
nodoQ(2) = 3;
PInst(3) = 0.8;
z(2) = 0.005+0.025j;
nodoP(3) = 3;
nodoQ(3) = 4;
PInst(4) = 0.5;
z(3) = 0.005+0.025j;
nodoP(4) = 3;
nodoQ(4) = 5;
PInst(5) = 0.4;
z(4) = 0.01+0.04j;
tramos = 4;
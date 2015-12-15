circuito = input('Nombre del circuito: ', 's');
VBase = input('Voltaje nominal del circuito (kV): ')
ArchTramos = [circuito,'.mat'];
ArchZthev = [circuito,'Zthev.mat'];
% Selecciona el circuito que se va a analizar
% Carga la informacion de tramos
% Lee datos del circuito (tramos)
%     nodoP
%     nodoQ
%     Zabc
%     Z012
%     Longitud
%     PInst
%     Usuarios
%     Sd
%     Nombres
load(ArchTramos)
% Lee datos especificados de impedancia Thevenin equivalente en la
% subestacion
%    zth1
%    zth2
%    zth0
load(ArchZthev)
% Calcula matrices de impedancia nodal  y valores base
SBase = 1; % Siempre usamos una base de 1 MVA para circuitos de distribucion
IBase = SBase*1000/(sqrt(3)*VBase);
ZBase = VBase^2/SBase;
% Determina el numero de tramos
nTramos = size(tramos,2);
% Determina el numero de nodos
nNodos = nTramos+1;
ZABC = zeros(3,3,nNodos);
Zsec = zeros(3,nNodos);
% Calcula las matrices de impedancia nodales 
a=(-1+sqrt(3)*j)/2;
Tfs=[1 1 1;1 a^2 a;1 a a^2]/3;
Tsf=inv(Tfs);
ZABC(:,:,1) = Tfs*diag([Zth0 Zth1 Zth2])*Tsf;
Zsec(:,1) = [Zth0; Zth1; Zth2];
for k=1:nTramos
    NodAnt = tramos(k).nodoP;
    Nodo = tramos(k).nodoQ;
    ZABC(:,:,Nodo) = ZABC(:,:,NodAnt)+tramos(k).Zabc;
	Zsec(:,Nodo) = Zsec(:,NodAnt)+tramos(k).Z012;%.';
end
save('DatosCircuitoA.mat','circuito','tramos','Zth1','Zth2','Zth0','Zsec','ZABC','nNodos','nTramos',...
     'ZBase','SBase','VBase','IBase');
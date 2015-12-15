% Localiza falla debida a 
% Cortocircuito Linea a Tierra, junto con 
% FLUJO DE CARGA RADIAL
% En circuito Talleres Centrales S/E Gorgonzola
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
% nTramos: Numero de tramos
% nNodos : Numero de nodos
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

%zth = 0.0232+0.0582j;
%

SBase=1;
VBase = 11.400
IBase = SBase/(VBase*sqrt(3))
ZBase = VBase^2/SBase
zth = (0.0206 + 0.0328i)/ZBase

%zth = 1+1j/ZBase;

Vs = 1;
%Ss = 2.0801+1.2771j;
%Ss = 1.97+0.93j;
load GG3A_2.mat;
load ZmatrixGG3A.mat
nTramos = Tramos;
nNodos = nTramos+1;
% 	Leer datos de carga
Sdem = zeros(1,nNodos);
dV = zeros(1,nTramos);
V = ones(1,nNodos);
Vant = zeros(1,nNodos);
I = zeros(1,nTramos);
ITramo = zeros(1,nTramos);
epsV = 1e-5;
epsP = 1e-5;
% Estimacion inicial de perdidas
for k=1:nTramos
   Pinstal(k) = tramos(k).PInst/1000;
   NodP(k) = tramos(k).nodoP;
   NodQ(k) = tramos(k).nodoQ;
   z1(k) = tramos(k).Z012(2);
   z2(k) = tramos(k).Z012(3);
   z0(k) = tramos(k).Z012(1);
end
Ss = sum(Pinstal);
CargaSE = sqrt(3)*0.085*11.4*(0.95+sin(acos(0.95))*j)/SBase;% cambio potencia
Carga100 = abs(CargaSE)/Ss
Perd = 0.005*CargaSE;
PerA = 0;
pasos=0;
divP=zeros(1,nNodos);
for k=1:nTramos
   divP(1,NodQ(k)) = Pinstal(k)/Ss;
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
       I = Id;
       for k=nTramos:-1:1
           I(NodP(k)) = I(NodP(k))+I(NodQ(k));
           ITramo(k) = I(NodP(k));
       end
       dV = ITramo.*z1;
       Itransf = I(1);
       V(1) = Vs-Itransf*zth;
       for k=1:nTramos
           V(NodQ(k)) = V(NodP(k))-dV(k);
       end
   end
   Ssac = Vs*conj(I(1));
   PerA = Perd;
   Perd = Ss-Ssac;
end
ISE = ITramo(1);
warning off MATLAB:divideByZero
N=16;
T1=0:2*pi/N:(N-1)*2*pi/N;
u=2*exp(j*T1)/(sqrt(3)*N);
M = csvread('FallaA1.csv');
Ia=M(:,1);
Ib=M(:,2);
Ic=M(:,3);
In=M(:,4);
Ig=M(:,5);
Va=M(:,6);
Va=M(:,6);
Vb=M(:,7);
Vc=M(:,8);
%Iabc=M(:,1:3);
%Vabc=M(:,6:8);
Iabc=[Ic Ia Ib];
Vabc=[Vc Va Vb];
Zabc=zeros(15,3);
% Transformacion de componentes simetricas
a=(-1+sqrt(3)*j)/2;
Tfs=[1 1 1;1 a^2 a;1 a a^2]/3;
for k=1:15
   for f=1:3
       ia=Ia((k-1)*16+1:k*16,:);
       IA(k)=u*ia;
       ib=Ib((k-1)*16+1:k*16,:);
       IB(k)=u*ib;
       ic=Ic((k-1)*16+1:k*16,:);
       IC(k)=u*ic;
       va=Va((k-1)*16+1:k*16,:);
       VA(k)=u*va;
       vb=Vb((k-1)*16+1:k*16,:);
       VB(k)=u*vb;
       vc=Vc((k-1)*16+1:k*16,:);
       VC(k)=u*vc;
       in=In((k-1)*16+1:k*16,:);
       IN(k)=u*in;
%        if abs(IA(k))> 1e-4 Zabc(k,1)=VA(k)/IA(k); end
%        if abs(IB(k))> 1e-4 Zabc(k,2)=VB(k)/IB(k); end
%        if abs(IC(k))> 1e-4 Zabc(k,3)=VC(k)/IC(k); end
   end
   Ifase=[IC(k);IA(k);IB(k)];
   abs(Ifase);
   Iseck=Tfs*Ifase;
   I0(k)=Iseck(1);
   I1(k)=Iseck(2);
   I2(k)=Iseck(3);
   Vfase=[VC(k);VA(k);VB(k)];
   Vseck=Tfs*Vfase;
   V0(k)=Vseck(1);
   V1(k)=Vseck(2);
   V2(k)=Vseck(3);
end
Vfa = VA(5)/VBase;
Vfb = VB(5)/VBase;
Vfc = VC(5)/VBase;
Ifa = IA(5)/(1000*IBase);
Ifb = IB(5)/(1000*IBase);
Ifc = IC(5)/(1000*IBase);
Vf1 = V1(5)/VBase;
Vf2 = V2(5)/VBase;
Vf0 = V0(5)/VBase;
If1 = I1(5)/(1000*IBase);
If2 = I2(5)/(1000*IBase);
If0 = I0(5)/(1000*IBase);
Vfalla = (abs(Vfa)+abs(Vfb)+abs(Vfc))/3
Vfalla = 1;
IcargaSE = ISE*Vfalla/abs(V(1));
% Calcula cortocircuitos A-T en cada nodo
%for z=0.001:0.5:5.001
    z = 0;
    Zf = z/ZBase;
    Ip0 = zeros(1,nNodos);
    Ip1 = zeros(1,nNodos);
    Vp0 = zeros(1,nNodos);
    Vp1 = zeros(1,nNodos);
    Vp2 = zeros(1,nNodos);
    Zp = zeros(1,nNodos);
    k0 = (Zsec(1,:)-Zsec(2,:))./Zsec(2,:);
    Ip0(1) = 1;
    Ip1(1) = 1;
%    for k=2:nNodos
%        I3p(k) = V(k)/(Zsec(1,k)+Zf)+ISE;
%        V3p(k) = V(1)-Zsec(1,1)*I3p(k);
%        Z3p(k) = V3p(k)/I3p(k);    
%    end
    unidad = ones(1,101);
    Ztotal = Zsec(1,:)+Zsec(2,:)+Zsec(3,:)+3*Zf;
    
    Ip0 = unidad./Ztotal;
    plot(abs(Ztotal))
    pause
    plot(abs(unidad./Ztotal))
    pause
    Ip1 =Ip0; 
    %Ip1 = V(:,2:489)./(Zsec(1,:)+Zsec(2,:)+Zsec(3,:)+3*Zf)+ISE;
    %Ia = 2*Ip1+Ip0;
    Iasin = 3*Ip0;
    Ia= Iasin;
    Vfp1 =V(:,:)-Zsec(2,1)*Ip1;
    Vfp2 = -Zsec(1,1)*Ip1;
    Vfp0 = -Zsec(3,1)*Ip0;
    Vfa = Vfp0+Vfp1+Vfp2;
    Vfc = Vfp0+a*Vfp1+a^2*Vfp2;

   
%end
% Reactancia en SE
XSE = imag(Vfc/(Ifc+k0(2)*3*If0))
% Restamos corriente de carga de la corriente de falla
If1 = If1-IcargaSE;
Ifc = Ifc-IcargaSE;
% Para cada tramo, verifica si la falla pudo ser aqui
for k=2:nTramos
    IFtramo = If1+ITramo(k)*Vfalla/abs(V(1));
    IFctramo = Ifc+ITramo(k)*Vfalla/abs(V(1));
    abs(IFtramo)
    Vfallaq = Vfc-IFtramo*Zsec(2,k)';
    max(abs(Vfallaq))
%   Metodo de reactancia
    Isk = IFctramo+k0(k)*3*If0
    Vsk = Vfc(NodP(k))
    xk = tramos(k).Z012'
    mx(k) = imag(Vsk/Isk)./imag(xk(2)');
%   Metodo de Takagi
    Isup = If1-ITramo(k);
    mtak(k) = imag(Vsk*Isup')/imag(xk(2)*Isk*Isup');
%   Metodo de     
    
    
end
min(mx)
min(mtak)
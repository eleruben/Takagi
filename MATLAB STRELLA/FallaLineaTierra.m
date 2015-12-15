% Cortocircuito Linea a Tierra, junto con 
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
% PInst : Potencia instalada en el nodo (usada para calcular Sd), al parecer es un arreglo de potencias
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

Vs = 1;
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
CargaSE = sqrt(3)*Ipre(1)*11.4/SBase;% cambio potencia
Carga100 = abs(CargaSE)/Ss
Perd = 0.05*Carga100;
PerA = 0;
pasos=0;
divP=zeros(1,nNodos);
for k=1:nTramos
   divP(1,NodQ(k)) = Pinstal(k)/Ss;
end
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
ISE = ITramo(1);


% Calcula cortocircuitos A-T en cada nodo
%for z=0.001:0.5:5.001
    z = 5;
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

    
    Ip0 = V(1,:)./(Zsec(1,:)+Zsec(2,:)+Zsec(3,:)+3*Zf);
    Ip1 =Ip0; 
    %Ip1 = V(:,2:489)./(Zsec(1,:)+Zsec(2,:)+Zsec(3,:)+3*Zf)+ISE;
    %Ia = 2*Ip1+Ip0;
    Iasin = 3*Ip0;
    Ia= Iasin;
    Vfp1 =V(:,2:nNodos)-Zsec(2,1)*Ip1;
    Vfp2 = -Zsec(1,1)*Ip1;
    Vfp0 = -Zsec(3,1)*Ip0;
    Vfa = Vfp0+Vfp1+Vfp2;
    

   
%end
%----------------------------------------------------
% Implentacion del algoritmo de localizacion de impedancia aparente.
% Articulo A fault location technique for rural distribution feeders. 

    Ip0=Ip1;
    Ia = Ip0 + 2 * Ip1;
    Iap = Ia + k0 .* Ip0;
    %Iapsin = Iasin+3*k0.*Ip0;
    Vp1 = V(1)-Zsec(2,1)*Ip1;
    Vp2 = V(1)-Zsec(1,1)*Ip1;
    Vp0 = V(1)-Zsec(3,1)*Ip0;
    Vf = Vp0+Vp1+Vp2;
    
    Va = Iap .* Zsec(1,:) + 3*Ip0*Zf;
    Zapp =Va./Iap;
    
    Icomp=3*Ip0;
    zpul=(0.0005+0.0046i);
%-------------------------------------------- 
    
    R1=real(zpul);
    X1=imag(zpul);
    Id=real(Icomp);
    Iq=imag(Icomp);
    Is1=real(Iap);
    Is2=imag(Iap);
    Rapp=real(Zapp);
    Xapp=imag(Zapp);
    Ism=abs(Iap);
    Ism2=Ism.*Ism;
    L=(Id.*Is1+Iq.*Is2)./Ism2;
    M=(-Id.*Is2+Iq.*Is1)./Ism2;
    D=(Rapp.*M-Xapp.*L)./(R1.*M-X1.*L);%longitud km
       
%-------------------------------------------  graficas

tramo1=tramos(1).Longitud(1)
ztram1=(0.07+0.0331i)/46

for k=1:nTramos
   Longitud(k)= tramos(k).Longitud;
   Impedancia(k)=ZABC(1,1,k+1);
end

Long=abs(Impedancia.*ZBase./(0.0005+0.0046i)); % se supone que calcula la distancia desde la subestacion hasta el nodo en falla

for k=1:nTramos
prop(k)=100*D(k+1)./Long(k);%resultado distancia %
end


%---------------------------------------------------------
%Metodo de circuitos directos I

    A1 = Zsec(3,:);
    B1 = zth+Zsec(3,:);
    %D11 = .01;
    
    %for kk=2:1:nLineas
    %I(NodP(k)-1) = I(NodP(k)-1)+I(NodQ(k)-1);
    %D1(kk)=V(kk)/I(NodP(kk)-1)+I(NodQ(kk)-1);
    %D1(kk)=V(kk)/(I(NodP(kk)-1)+I(NodQ(kk)-1)+D11);
    %D1(kk)=rand*1;
    %end
    D1 = 0.1;
    
    Iap = Ia+k0.*Ip0;
    Va = Iap.*Zsec(2,:)+3*Ip0*Zf; 

    a = (Ia+k0.*Ip0).*Zsec(2,:).*A1;
    b = ((Ia+k0.*Ip0).*Zsec(2,:).*D1)+(Va-(Ia+k0.*Ip0).*Zsec(2,:).*A1);
    c = (Va-((Ia+k0.*Ip0).*Zsec(2,:))).*D1;
    d = 3.*(B1+D1).*Ip1;
    
    ar = real(a);
    ai = imag(a);
    
    br = real(b);
    bi = imag(b);
    
    cr = real(c);
    ci = imag(c);
    
    dr = real(d);
    di = imag(d);
    
    w = ar-((dr/di)*ai);
    xvc = br-((dr/di)*bi);
    y = cr-((dr/di)*ci);
    
    pdis = [w' xvc' y'];
    
   xv=[0 0];
for nn=1:488
    qq=roots(pdis(nn,:));
    qqq=qq';
    xv=[xv;qqq];
end
xv=xv(2:end,:);
distancia1=1-xv;

%---------------------------------------------------------
%imagen
   figure(1)
    subplot(2,1,1)
   
    plot(abs(V),'*')
    title('V prefalla')
    GRID ON
    %figure(3)
    subplot(2,1,2)
    
    plot(abs(I),'*')
     title('I prefalla')
     GRID ON
     
         
     figure(2)
%figure(4)
subplot(2,1,1)
plot(abs(Vfa),'*')
 title('Vf V falla')
GRID ON
 %figure(5)
subplot(2,1,2)
plot(abs(Iasin),'*')
 title('I falla ')
 GRID ON
 
 
      figure(3)
    subplot(1,1,1)  
plot(distancia1(:,2),'*')
 title('Distancia a la falla')
GRID ON
 
   figure(4)
 subplot(1,1,1)
plot((prop),'*')
 title('Distancia a la falla')
 GRID ON


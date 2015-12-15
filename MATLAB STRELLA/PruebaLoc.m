tramos(1).nodoP=1;
tramos(1).nodoQ=2;
tramos(1).Zabc=diag([0.01+0.005j 0.01+0.005j 0.01+0.005j]);
tramos(1).Z012=[0.01+0.005j; 0.01+0.005j; 0.01+0.005j];
tramos(1).Longitud=100;
tramos(1).PInst=0;
tramos(1).Usuarios=0;
tramos(1).Sd=0;
tramos(1).Nombres='2';
tramos(2).nodoP=2;
tramos(2).nodoQ=3;
tramos(2).Zabc=diag([0.01+0.005j 0.01+0.005j 0.01+0.005j]);
tramos(2).Z012=[0.01+0.005j; 0.01+0.005j; 0.01+0.005j];
tramos(2).Longitud=100;
tramos(2).PInst=0;
tramos(2).Usuarios=100;
tramos(2).Sd=0;
tramos(2).Nombres='3';
tramos(3).nodoP=3;
tramos(3).nodoQ=4;
tramos(3).Zabc=diag([0.01+0.005j 0.01+0.005j 0.01+0.005j]);
tramos(3).Z012=[0.01+0.005j; 0.01+0.005j; 0.01+0.005j];
tramos(3).Longitud=100;
tramos(3).PInst=0;
tramos(3).Usuarios=100;
tramos(3).Sd=0;
tramos(3).Nombres='4';
tramos(4).nodoP=4;
tramos(4).nodoQ=5;
tramos(4).Zabc=diag([0.01+0.005j 0.01+0.005j 0.01+0.005j]);
tramos(4).Z012=[0.01+0.005j; 0.01+0.005j; 0.01+0.005j];
tramos(4).Longitud=100;
tramos(4).PInst=100;
tramos(4).Usuarios=100;
tramos(4).Pinst=100;
tramos(4).Sd=0;
tramos(4).Nombres='5';
save('Prueba.mat','tramos')
nTramos=4;
NNodos=5;
V4=1-4*(1.6+j)*(0.01+0.005j)
abs(V4)
Isub = 1.6+j;
%Isub = I1(2);
% Voltaje medido prefalla (usamos el primer valor de VA)
Vsub = 1;
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
k0 = (z0-z1)./(3*z1)
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
Vth=V(1)+ISE*zth1
zth1=0.005+0.01;
Zth0=zth1;
zth2=zth1;
Ifalla=V(4)/(0.06+0.03j+3*zth1);
abs(Ifalla)
IA=3*Ifalla;
abs(IA)
VA=Vth-Ifalla*zth1
abs(VA)
N=16;
T1=0:2*pi/N:(N-1)*2*pi/N;
%u=2*exp(j*T1)/(sqrt(3)*N);
u=2*exp(j*T1)/(N);
SBase=1;% 1 MVA
VBase = 34.5; % 34.5 kV
IBase = SBase*1000/(VBase*sqrt(3))
ZBase = VBase^2/SBase
M = csvread('CIPLAST_FCG.csv');
FaseFallada='c';
Ia=M(:,1)/(sqrt(2)*IBase);
Ib=M(:,2)/(sqrt(2)*IBase);
Ic=M(:,3)/(sqrt(2)*IBase);
In=M(:,4)/(sqrt(2)*IBase);
Va=M(:,6)*sqrt(3)/VBase;
Vb=M(:,7)*sqrt(3)/VBase;
Vc=M(:,8)*sqrt(3)/VBase;
Ig=M(:,5)/(sqrt(2)*IBase);
Iabc=[Ic Ia Ib];
Vabc=[Vc Va Vb];
Zabc=zeros(15,3);
% Transformacion de componentes simetricas
a=(-1+sqrt(3)*j)/2;
Tfs=[1 1 1;1 a^2 a;1 a a^2]/3
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
    switch FaseFallada
          case 'a'
            Ifase(:,k)=[IA(k);IB(k);IC(k)];
            Vfase(:,k)=[VA(k);VB(k);VC(k)];
          case 'b'
            Ifase(:,k)=[IB(k);IC(k);IA(k)];
            Vfase(:,k)=[VB(k);VC(k);VA(k)];
          otherwise
            Ifase(:,k)=[IC(k);IA(k);IB(k)];
            Vfase(:,k)=[VC(k);VA(k);VB(k)];
        end
 
   abs(Ifase);
   Iseck=Tfs*Ifase(:,k);
   I0(k)=Iseck(1);
   I1(k)=Iseck(2);
   I2(k)=Iseck(3);
   Vseck=Tfs*Vfase(:,k);
   V0(k)=Vseck(1);
   V1(k)=Vseck(2);
   V2(k)=Vseck(3);
end
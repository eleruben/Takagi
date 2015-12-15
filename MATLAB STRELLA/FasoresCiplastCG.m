warning off MATLAB:divideByZero
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
Ia=M(:,1);
Ib=M(:,2);
Ic=M(:,3);
In=M(:,4);
plot(Ia,'r')
hold on
plot(Ib,'g')
plot(Ic,'b')
%plot(In,'k')
hold off
pause
Ia=M(:,1)/(sqrt(2)*IBase);
Ib=M(:,2)/(sqrt(2)*IBase);
Ic=M(:,3)/(sqrt(2)*IBase);
In=M(:,4)/(sqrt(2)*IBase);
plot(Ia,'r')
hold on
plot(Ib,'g')
plot(Ic,'b')
%plot(In,'k')
hold off
pause
Va=M(:,6)*sqrt(3)/VBase;
Vb=M(:,7)*sqrt(3)/VBase;
Vc=M(:,8)*sqrt(3)/VBase;
plot(Va,'r')
hold on
plot(Vb,'g')
plot(Vc,'b')
%plot(In,'k')
hold off
pause
Ig=M(:,5)/(sqrt(2)*IBase);
%Iabc=M(:,1:3);
%Vabc=M(:,6:8);
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
Z1(1)=(V1(6)-V1(1))/(I1(6)-I1(1));%*ZBase
Z2(1)=(V2(6))/(I2(6));%*ZBase
Z0(1)=(V0(6))/(I0(6));%*ZBase
Z1(2)=(V1(7)-V1(1))/(I1(7)-I1(1));%*ZBase
Z2(2)=(V2(7))/(I2(7));%*ZBase
Z0(2)=(V0(7))/(I0(7));%*ZBase
Z1(3)=(V1(8)-V1(1))/(I1(8)-I1(1));%*ZBase
Z2(3)=(V2(8))/(I2(8));%*ZBase
Z0(3)=(V0(8))/(I0(8));%*ZBase
Z1(4)=(V1(6)-V1(5))/(I1(6)-I1(5));%*ZBase
Z2(4)=(V2(6)-V2(5))/(I2(6)-I2(5));%*ZBase
Z0(4)=(V0(6)-V0(5))/(I0(6)-I0(5));%*ZBase
Z1(5)=(V1(7)-V1(6))/(I1(7)-I1(6));%*ZBase
Z2(5)=(V2(7)-V2(6))/(I2(7)-I2(6));%*ZBase
Z0(5)=(V0(7)-V0(6))/(I0(7)-I0(6));%*ZBase
Z1(6)=(V1(8)-V1(7))/(I1(8)-I1(7));%*ZBase
Z2(6)=(V2(8)-V2(7))/(I2(8)-I2(7));%*ZBase
Z0(6)=(V0(8)-V0(7))/(I0(8)-I0(7));%*ZBase
Z1(7)=(V1(8)-V1(6))/(I1(8)-I1(6));%*ZBase
Z2(7)=(V2(8)-V2(6))/(I2(8)-I2(6));%*ZBase
Z0(7)=(V0(8)-V0(6))/(I0(8)-I0(6));%*ZBase
plot(Z1,'*');axis([-6 4 -5 5])
pause
plot(Z2,'*');axis([-6 4 -5 5])
pause
plot(Z0,'*');axis([-6 4 -5 5])
pause
% deltaV=Tfs*(Vfase(:,7)-Vfase(:,1));
% deltaI=Tfs*(Ifase(:,7)-Ifase(:,1));
% Zsec=deltaV*ZBase./deltaI
plot(abs(IA),'r')
hold on
plot(abs(IB),'g')
plot(abs(IC),'b')
plot(abs(IN),'k')
hold off
pause
plot(abs(VA),'r')
hold on
plot(abs(VB),'g')
plot(abs(VC),'b')
hold off
pause
plot(abs(I0),'r')
hold on
plot(abs(I1),'g')
plot(abs(I2),'b')
plot(abs(IN),'k*')
plot(3*abs(I0),'y')
plot(abs(I1-I0),'k')
hold off
pause
plot(abs(V0),'r')
hold on
plot(abs(V1),'g')
plot(abs(V2),'b')
hold off
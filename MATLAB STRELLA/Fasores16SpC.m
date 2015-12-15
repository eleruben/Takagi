warning off MATLAB:divideByZero
N=16;
T1=0:2*pi/N:(N-1)*2*pi/N;
u=2*exp(j*T1)/(sqrt(3)*N);
M = csvread('FallaA1.csv');
Ia=M(:,1);
Ib=M(:,2);
Ic=M(:,3);
In=M(:,4);
plot(Ia,'r')
hold on
plot(Ib,'g')
plot(Ic,'b')
plot(In,'k')
hold off
pause
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
Za=(VA./IA)'
Zb=(VB./IB)'
Zc=(VC./IC)'
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
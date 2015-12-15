% Muestras por ciclo
N=32;
% Muestras de exp(j2*k*pi/N)
T1=0:2*pi/N:(N-1)*2*pi/N;
u=2*exp(j*T1)/(sqrt(3)*N);
M = csvread('FallaA1.csv',',');
FaseFallada=input('Fase donde ocurrio la falla: ', 's');
FaseFallada
Ia=M(:,1);
Ib=M(:,2);
Ic=M(:,3);
In=M(:,4);
% plot(Ia,'r')
% hold on
% plot(Ib,'g')
% plot(Ic,'b')
% hold off
% pause
Va=M(:,5);
Vb=M(:,6);
Vc=M(:,7);
% plot(Va,'r')
% hold on
% plot(Vb,'g')
% plot(Vc,'b')
%plot(In,'k')
% hold off
% pause
% Ig=M(:,5);
%Iabc=M(:,1:3);
%Vabc=M(:,6:8);
% Matriz de la Transformacion de Componentes Simetricas
a=(-1+sqrt(3)*j)/2;
Tfs=[1 1 1;1 a^2 a;1 a a^2]/3
% Calculo de los fasores de corriente y voltaje
for k=1:15
   for f=1:3
       ia=Ia((k-1)*32+1:k*32,:);
       IA(k)=u*ia;
       ib=Ib((k-1)*32+1:k*32,:);
       IB(k)=u*ib;
       ic=Ic((k-1)*32+1:k*32,:);
       IC(k)=u*ic;
       va=Va((k-1)*32+1:k*32,:);
       VA(k)=u*va;
       vb=Vb((k-1)*32+1:k*32,:);
       VB(k)=u*vb;
       vc=Vc((k-1)*32+1:k*32,:);
       VC(k)=u*vc;
       in=In((k-1)*32+1:k*32,:);
       IN(k)=u*in;
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

ZBase =0.01+0.1i;
Zth1=(V1(6)-V1(1))/(I1(6)-I1(1)*ZBase)
Zth2=(V2(6)-V2(1))/(I2(6)-I2(1)*ZBase)
Zth0=(V0(6)-V0(1))/(I0(6)-I0(1)*ZBase)
%save('Fasores.mat','VA','VB','VC','IA','IB','IC','V0','V1','V2','I0','I1','I2','Ifase','Vfase',...
%    'Zth1','Zth2','Zth0','FaseFallada');

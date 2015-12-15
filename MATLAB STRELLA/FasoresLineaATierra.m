% FALLA DE LINEA A TIERRA
% Procesamiento de los datos instantaneos, medidos, para la falla
% Supone que los datos base del circuito ya han sido leidos
% Muestras por ciclo
N=16; % AJUSTAR SI ES NECESARIO
% Muestras de exp(j2*k*pi/N)
T1=0:2*pi/N:(N-1)*2*pi/N;
u=2*exp(j*T1)/(N);
[medidas, pathname] = uigetfile('*.csv', 'Seleccione el archivo de mediciones');
M = csvread(medidas);
FaseFallada=input('Fase donde ocurrio la falla: ', 's');
Ciclo=input('No del ciclo de falla: ');
FaseFallada
plot(M(:,6),'r')
hold on
plot(M(:,7),'g')
plot(M(:,8),'b')
hold off
pause
VBaseFase=VBase/sqrt(3);
% Ia=M(:,1)/IBase;
% Ib=M(:,2)/IBase;
% Ic=M(:,3)/IBase;
% In=M(:,4)/IBase;
% Ig=M(:,5)/IBase;
Ia=M(:,1)/(IBase*sqrt(2));
Ib=M(:,2)/(IBase*sqrt(2));
Ic=M(:,3)/(IBase*sqrt(2));
In=M(:,4)/(IBase*sqrt(2));
Ig=M(:,5)/(IBase*sqrt(2));
plot(Ia,'r')
hold on
plot(Ib,'g')
plot(Ic,'b')
hold off
pause
Va=M(:,6)/VBaseFase;
Vb=M(:,7)/VBaseFase;
Vc=M(:,8)/VBaseFase;
plot(Va,'r')
hold on
plot(Vb,'g')
plot(Vc,'b')
%plot(In,'k')
hold off
pause
%Iabc=M(:,1:3);
%Vabc=M(:,6:8);
% Matriz de la Transformacion de Componentes Simetricas
a=(-1+sqrt(3)*j)/2;
Tsf=[1 1 1;1 a^2 a;1 a a^2];
Tfs=inv(Tfs);
% Calculo de los fasores de corriente y voltaje
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
   end
    switch FaseFallada
          case 'a'
            Ifase(:,k)=[IA(k);IC(k);IB(k)];
            Vfase(:,k)=[VA(k);VC(k);VB(k)];
          case 'b'
            Ifase(:,k)=[IB(k);IA(k);IC(k)];
            Vfase(:,k)=[VB(k);VA(k);VC(k)];
          otherwise
            Ifase(:,k)=[IC(k);IB(k);IA(k)];
            Vfase(:,k)=[VC(k);VB(k);VA(k)];
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
switch FaseFallada
          case 'a'
            theta=angle(VA(5))
            alfa=cos(-theta)+j*sin(-theta)
          case 'b'
            theta=angle(VB(5))
            alfa=cos(-theta)+j*sin(-theta)
          otherwise
            theta=angle(VC(5))
            alfa=cos(-theta)+j*sin(-theta)
        end
Ifase=Ifase*alfa;
Vfase=Vfase*alfa;
IN=IN*alfa;
Zth1=(V1(Ciclo)-V1(1))/(I1(1)-I1(Ciclo))
Zth2=(V2(Ciclo)-V2(1))/(I2(1)-I2(Ciclo))
Zth0=(V0(Ciclo)-V0(1))/(I0(1)-I0(Ciclo))
% Escribe los datos de fasores (pu) medidos en la subestacion:
%    'VA','VB','VC'
%    'IA','IB','IC'
%    'V0','V1','V2'
%    'I0','I1','I2'
% Cada vector contiene 15 fasores correspondientes a 15 ciclos
%    'Ipref','Vpref' (Corriente y voltaje de fase prefalla)
%    'Ifase','Vfase' (Corriente y voltaje de fase durante falla)
%    'Zth1','Zth2','Zth0'
% Ademas, lee la fase donde ocurrio la falla: 
%    'FaseFallada'
save('Fasores.mat','VA','VB','VC','IA','IB','IC','V0','V1','V2','I0','I1','I2','Ifase','Vfase',...
    'Zth1','Zth2','Zth0','FaseFallada'); 
N=16;
T1=0:2*pi/N:(N-1)*2*pi/N;
u=2*exp(j*T1)/(sqrt(3)*N);
M = csvread('FallaA1.csv',',', r, c);
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
% Transformacion de componentes simetricas
a=(-1+sqrt(3)*j)/2;
Tfs=[1 1 1;1 a^2 a;1 a a^2]/3;
% Usaremos el quinto ciclo para la corriente de falla
ia=Ia(81:96);
ib=Ib(81:96);
ic=Ic(81:96);
in=In(81:96);
IA=u*ia;
IB=u*ib;
IC=u*ic;
IN=u*in;
Ifase=[IC;IA;IB];
abs(Ifase)
[If,fasef]=max(abs(Ifase))
% Ahora usaremos la fase con la corriente maxima como referencia
indice=(fasef-1)*5;
% Redefinimos los fasores:
ia=Ia(81+indice:96+indice);
ib=Ib(81+indice:96+indice);
ic=Ic(81+indice:96+indice);
in=In(81+indice:96+indice);
IA=u*ia;
IB=u*ib;
IC=u*ic;
IN=u*in;
Ifase=[IC;IA;IB];
Iseck=Tfs*Ifase;
I0=Iseck(1);
I1=Iseck(2);
I2=Iseck(3);
% Usaremos el primer ciclo para la corriente prefalla
ia=Ia(1+indice:16+indice);
ib=Ib(1+indice:16+indice);
ic=Ic(1+indice:16+indice);
Ipre(1)=u*ia;
Ipre(2)=u*ib;
Ipre(3)=u*ic;
plot(abs(IA),'r*')
hold on
plot(abs(IB),'g*')
plot(abs(IC),'b*')
plot(abs(IN),'k*')
hold off
pause
plot(abs(I0),'r*')
hold on
plot(abs(I1),'g*')
plot(abs(I2),'b*')
plot(abs(IN),'k*')
plot(3*abs(I0),'y*')
plot(abs(I1-I0),'k*')
hold off

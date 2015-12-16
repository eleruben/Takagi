volt=voltage*KVb;
volt

tetha1=120*pi/180;
tetha2=240*pi/180;

ang1=[angle(1) angle(1)+(tetha1) angle(1)+(tetha2)];
ang2=[angle(2) angle(2)+(tetha1) angle(2)+(tetha2)];
ang3=[angle(3) angle(3)+(tetha1) angle(3)+(tetha2)];
ang4=[angle(4) angle(4)+(tetha1) angle(4)+(tetha2)];

ang=[ang1;ang2;ang3;ang4]'

%NODO GENERADOR
v1=[volt(1)*exp(sqrt(-1)*ang(1,1)) volt(1)*exp(sqrt(-1)*ang(2,1)) volt(1)*exp(sqrt(-1)*ang(3,1))];

%NODO 1
v2=[volt(2)*exp(sqrt(-1)*ang(1,2)) volt(1)*exp(sqrt(-1)*ang(2,2)) volt(1)*exp(sqrt(-1)*ang(3,2))];

%NODO 2
v3=[volt(3)*exp(sqrt(-1)*ang(1,3)) volt(1)*exp(sqrt(-1)*ang(2,3)) volt(1)*exp(sqrt(-1)*ang(3,3))];

%NODO 3
v4=[volt(4)*exp(sqrt(-1)*ang(1,4)) volt(1)*exp(sqrt(-1)*ang(2,4)) volt(1)*exp(sqrt(-1)*ang(3,4))];

Vpre=[v1; v2; v3; v4].'

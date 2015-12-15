clc
clear
%Localizador de fallas basado en analisis deiredto de circuitos%Localizador de fallas usando el factor de distribucion
%Calculos para un sistma balanceado trifasico, con falla linea-tierra en a

%Valores de entrada:Son los valores medidos por los TC y TV en un el nodo a
%Valores de las corrientes para las tres fase medidas en el nodo
%El valor de el voltaje medido en el nodo
%Valores de salida: el valor de salida es la distancia

%Valores de las corrientes para las tres fase medidas en el nodo
ISabc=[1.0000; -0.5000+0.8660i; -0.5000-0.8660i;];
%El valor de el voltaje medido en el nodo
Va=0.95;

%Primera fila de la matriz Zlabc

ZL1=[0.655+1.469i 0.19+1.27i 0.095+0.637i];
C1=ZL1*ISabc;

%Primera fila de la matriz Zrabc

Zr1=[1.07+0.392i 0.005+0.067i 0.014+0.059i]*10e1;

C2=Zr1*ISabc;

%Valores de la posicion (1,1) de las matrices Zlabc y Zrabc


Zlaa=ZL1(1,1);
Zraa=Zr1(1,1);


a=C1*Zlaa;   //
b=Va*Zlaa-(C1*Zlaa*C1*Zraa);
c=Zraa*(Va-C1);
d=Va-C1-C2;


e=real(a);
f=imag(a);

g=real(b);
h=imag(b);

k=real(c);
l=imag(c);

m=real(d);
n=imag(d);


R=[(e-(m/n)*f) (g-(m/n)*h) (k-(m/n)*l)];

%Valores de salida: el valor de salida es la distancia
disp('Valores de d')
d=roots(R)


clc
clear
%Algoritmo de Takagi Modificado de localizacion de falla para una Falla monofasica 
%en la fase a.

%El programa comienza cuando detecta la falla
%Valores de entrada:Son los valores medidos por los TC y TV en un nodo
%Va1= Voltaje de la fase a en falla para la terminal
%I= corriente  medida en el nodo despues de la falla
%Ipre= corriente  medida en el nodo antes de la falla
%Isec0 = corriente de sec (0)

%Valores de salida
% x= Distancia de la falla al nodo de medicion

%impedancia de la linea en P.U de longitud.
Z =0.01+0.1i;

Va1= input ('Voltaje de la fase a: ');
I= input ('Introdusca la corriente despues de la falla: ');
Ipre= input ('Introdusca la corriente antes de la falla: ');

Isec0 = input ('Introdusca la corriente de sec(0): ');
Isec=3*Isec0;

%Calcula el angulo de la corriente de falla y la corriente de sec(0)
If=I-Ipre;
a= If/(3*Isec0);
T= angle(a);
s= exp(-j*T);


x=imag(Va1*Isec'*s)/imag(Z*I*Isec'*s);

   
x
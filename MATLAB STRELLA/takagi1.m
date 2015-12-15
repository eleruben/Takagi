clc
clear
%Algoritmo de Takagi de localizacion de falla para una Falla monofasica 
%en la fase a. La torre tiene dos circuitos
%El programa comienza cuando detecta la falla
%Valores de entrada:Son los valores medidos por los TC y TV en un nodo
%Va1= Voltaje de la fase a en falla para la terminal
%Ia1=Diferencia de corriente en la fase antes y despues de la falla
%VLa1= Suma del efecto de las impedancia propia y de las otras fases
%z11...Z16 = Valores de impedancias propias y mutuas
%I1,: = Corrientes por las lineas

%Valores de salida
% x= Distancia de la falla al nodo de medicion

za1a1 = 1;
za1b1 = 1;
za1c1 = 1;
za1a2 = 1;
za1b2 = 1;
za1c2 = 1;

Ia1 = 1i;
Ib1 = 1;
Ic1 = 1;
Ia2 = 1;
Ib2 = 1;
Ic2 = 1i;

Z = [za1a1 za1b1 za1c1 za1a2 za1b2 za1c2];
I = [Ia1; Ib1; Ic1; Ia2; Ib2; Ic2;];
Vla=Z*I;

Va1= input ('Voltaje de la fase a: ');
Ia1= input ('Diferencia de corriente antes y despues de la falla: ');
x=imag(Va1*Ia1')/imag(Vla*Ia1');
if (x>0) & (x<5)
   x
else 
   disp('No hay convergencia')
takagi
end
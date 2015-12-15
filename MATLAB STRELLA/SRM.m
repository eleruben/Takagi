clc
clear
%Algoritmo de Metodo  de reactancia simple para localizacion de falla
%en una Falla monofasica en la fase a.

%Valores de entrada:Son los valores medidos por los TC y TV en un nodo
%Va1= Voltaje de la fase a en falla para la terminal
%I= corriente  medida en el nodo despues de la falla

Va1= input ('Voltaje de la fase a: ');
I= input ('Introdusca la corriente despues de la falla: ');

Z=0.1;

x=imag(Va1/I)/Z;


if (x>0)& (x<20)
   x
   else ('NO converge')
end



function [fasor,magnitud,fase] = lsq(p,t)
% Muestras
%t=[0:1/(60*31):1/60];

%T=t(length(t)); %Periodo fundamental
T=t(length(t)); %Periodo fundamental

w=2*pi*(60); % Frecuencia fundamental
%v=500*exp(-t./(0.1))+300.*cos(w.*t)+300.*cos(3*w.*t);

%m= length(v); %Cantidad de muestras
m= length(p);

% ===== MATRIZ DE COEFICIENTES CONOCIDOS =====

A=zeros(m, 12);

for fila = 1:m % Columnas correspondientes a los 7 coeficientes
    for columna = 1:12 % Filas correspondientes a 9 muestras
        if columna==1
            A(fila,1) = 1;
        end
        
        if columna==2
            A(fila,2) = t(fila);
        end
        
        if columna==3
            A(fila,3) = cos(w*t(fila));
        end
        
        if columna==4
            A(fila,4) = cos(2*w*t(fila));
        end
        
        if columna==5
            A(fila,5) = cos(3*w*t(fila));
        end
        
        if columna==6
            A(fila,6) = cos(4*w*t(fila));
        end
        
        if columna==7
            A(fila,7) = cos(5*w*t(fila));
        end    
        
        if columna==8
            A(fila,8) = sin(w*t(fila));
        end    
        
        if columna==9
            A(fila,9) = sin(2*w*t(fila));
        end    
        
        if columna==10
            A(fila,10) = sin(3*w*t(fila));
        end    
        
        if columna==11
            A(fila,11) = sin(4*w*t(fila));
        end    
        
        if columna==12
            A(fila,12) = sin(5*w*t(fila));
        end    
        
    end 
end

% ===== Matriz pseudo-inversa =====

%A_pinv=pinv(A);  Función que incluye Matlab
A_pinv=(inv(A'*A))*A';

% ===== Vector Desconocido =====

%S=v'; %vector columna para poder hacer la multiplicación

x=A_pinv*p; %Vector de valores desconocidos

% ===== DETERMINACIÓN DE COEFICIENTES =====

%k1=x(1); % Constante K1 de v(t)



% Revisar si se puede resolver así

fasor=x(8)+j*x(3); %fasor
magnitud=abs(fasor);  %magnitud
fase=angle(fasor); %fase

%plot(t,p);


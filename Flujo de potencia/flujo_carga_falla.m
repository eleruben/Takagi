% ALGORITMO PARA FLUJO DE POTENCIA EN FALLA
clc;
%clear all;
format short;
tic
%Datos de potencias activa (columna 2) y reactiva (columna 3)
m=[1 2 3 4; 0 67.5e3 67.5e3 67.5e3; 0 32.69e3 32.69e3 32.69e3; 0 0 0 0]';
%Datos de resistencia (columna 4) y reactancia (columna 5)
l=[1 2 3; 1 2 3; 2 3 4; 0.2746 0.1373 0.2059; 0.0040 0.0020 0.0030]';

Vsub=Vspos;
Isub=Ispos;% falta cuadrar los fasores porque la corriente tiene componente exponencial

br=length(l(:,1));   %ramas
no=length(m(:,1));   %nodos
MVAb=270000;  %potencia base
KVb=115000;  %tensión base
Zb=(KVb^2)/MVAb; %impedancia base
% Per unit Values  para resistencias, reactancias, potencias activa y
% reactiva
for i=1:br
    R(i,1)=(l(i,4))/Zb;  
    X(i,1)=(l(i,5))/Zb;
end
for i=1:no
    P(i,1)=((m(i,2))/(MVAb));
    Q(i,1)=((m(i,3))/(MVAb));
end
for i=1:length(Vsub) %Tensiones y corrientes vistas en S/E para falla en pu
    Vs(i)=Vsub(i)/KVb;
    Is(i)=Isub(i)/KVb;
end

R
X
P
Q
Vs
Is

% 
% for i=1:br
%     for j=1:br
%         Vj(i,j)=Vs(j);
%     end
% end
% 
% Vnode=Vj.'; % valor inicial para iniciar iteraciones
% error=0.05; %Definición de error
% 
% %iteraciones
% %for abs((deltav(k)-deltav(k-1))<error
%     for i=1:br
%         for j=1:br
%             Inode(i,j)=conj(Snode(i)/Vnode(j,i));
%         end
%     end
% 
%     Inode
    

C=zeros(br,no); % matriz de tamaño tramos * nodos
for i=1:br % Muestra conexiones entre nodos y tramos: donde -1 indica conexión entre nodo y tramo
                                                          %  1 indica que el nodo tiene carga
    a=l(i,2);
    b=l(i,3);
    for j=1:no
        if a==j
            C(i,j)=-1;
        end
        if b==j
            C(i,j)=1;
        end
    end
end
C
e=1;
for i=1:no    % Determina los nodos finales de la troncal y las ramas
    d=0;
    for j=1:br
        if C(j,i)==-1
            d=1;
        end
    end
    if d==0
        endnode(e,1)=i;
        e=e+1;
    end
end
endnode
h=length(endnode);
for j=1:h   %Organiza en una matriz cada derivación por filas, desde el tramo final al inicial
    e=2;
    
    f=endnode(j,1);
   % while (f~=1)
   for s=1:no
     if (f~=1)
       k=1;  
       for i=1:br
           if ((C(i,f)==1)&&(k==1))
                f=i;
                k=2;
           end
       end
       k=1;
       for i=1:no
           if ((C(f,i)==-1)&&(k==1));
                f=i;
                g(j,e)=i;
                e=e+1;
                k=3;
           end            
       end
     end
   end
end

g

for i=1:h %Organiza en una matriz cada derivación por filas, desde cada nodo final al inicial
    g(i,1)=endnode(i,1);
end
g;
g
w=length(g(1,:)) %Número de nodos de la troncal más larga
w
for i=1:h %Organiza en una matriz cada derivación por filas, desde cada nodo inicial al final
    j=1;
    for k=1:no 
        for t=1:w
            if g(i,t)==k
                g(i,t)=g(i,j);
                g(i,j)=k;
                j=j+1;
             end
         end
    end
end
g;
g

for k=1:br  %Organiza en la columna 1 todos los nodos menos los conectados directos a la troncal
            %Columnas son las ramas del sistema o derivaciones 
            %Las filas indican cada uno de los nodos
    e=1;
    for i=1:h
        for j=1:w-1
            if (g(i,j)==k) 
                if g(i,j+1)~=0
                    adjb(k,e)=g(i,j+1);            
                    e=e+1;
                else
                    adjb(k,1)=0;
                end
             end
        end
    end
end
adjb;
adjb

for i=1:br-1  %La columna 1 no cambia
              %Columnas son las ramas del sistema o derivaciones 
              %Las filas indican cada uno de los nodos
              %Deja solamente los nodos de conexión directa a la troncal
              
    for j=h:-1:1
        for k=j:-1:2
            if adjb(i,j)==adjb(i,k-1)
                adjb(i,j)=0;
            end
        end
    end
end
adjb;
adjb

x=length(adjb(:,1)); %filas
ab=length(adjb(1,:));%columnas
for i=1:x  %Organiza en la columna 1 todos los tramos menos los conectados directos a la troncal
           %Columnas son las ramas del sistema o derivaciones 
           %Las filas indican cada uno de los nodos
    for j=1:ab
        if adjb(i,j)==0 && j~=ab
            if adjb(i,j+1)~=0
                adjb(i,j)=adjb(i,j+1);
                adjb(i,j+1)=0;
            end
        end
        if adjb(i,j)~=0
            adjb(i,j)=adjb(i,j)-1;
        end
    end
end
adjb;
adjb

for i=1:x-1 %Elimina la fila 1 de la matriz
    for j=1:ab
        adjcb(i,j)=adjb(i+1,j);
    end
end

adjcb %Matriz que tiene las derivaciones sin tener en cuenta los tramos conectados directamente con troncal
%Muestra los tramos conectados a cada unos los tramos (filas)

%Cálculos de tensión y corriente
% voltage current program

b=length(adjcb);  %Cantidad de filas de la matriz adjcb => # cantidad de tramos

for i=1:no %Inicializa el vector de tensión con "unos"
    for j=1:3
        vb(i,j)=Vs(j); %Matriz de inicialización de tensiones Vnodo=Vsubestación_falla //// filas: nodos, columnas: fases
    end
end

vb

%===============================================================================
%===============================================================================
%CÁLCULO ITERATIVO

for i=1:3 % Número de fases
    Ssub(i)=Vs(i)*(Is(i))';
end

Ssub;
Ssub

S=complex(P(:,1),Q(:,1));

for i=1:br
    Ssum=abs(sum(S));
end

Ssum;
Ssum

for i=1:no
    for j=1:3
        Snode(i,j)=Ssub(j)*(abs(S(i)) / Ssum);
    end
end

Snode;
Snode

for s=1:10 %Definición del error ==> Define número de iteraciones
    for i=1:no
        for j=1:3  %número de fases
            Iload(i,j)=conj(Snode(i,j))/(vb(i,j)); %Corrientes de carga
        end
    end
    
    Iload;
    
    for i=1:br  % Asume corrientes de los tramos como las corrientes de carga de su nodo correspondiente
        for j=1:3
            Ibr(i,j)=Iload(i+1,j);
        end
    end
    
    Ibr;
    Ibr
    
    xy=length(adjcb(1,:)); %Asigna a "xy" la cantidad de ramales del circuito
    
    %Barrido de corriente de tramo desde último tramo hasta S/E
    for j=1:3
        for i=br-1:-1:1  %Inicia desde el tramo énesimo-1 hasta llegar al tramo 1
            for k=1:xy % Ayuda a seleccionar los tramos conectados al tramo en cuestión
                if adjcb(i,k)~=0 % Si hay tramos conectados al tramo en cuestión hace instrucción
                    u=adjcb(i,k); %Asigna el número del tramo que está conectado al tramo en cuestión a la variable "u"
                    %Ibr(i,1)=nlc(i+1,1)+Ibr(k,1);
                    Ibr(i,j)=Ibr(i,j)+Ibr(u,j);   %Corrientes de tramos
                end
            end      
        end
    end
    
    Ibr;
    
    %Asigna las tensiones en los nodos => recorrido de S/E hacia nodos terminales
        
    for j=1:3
        for i=2:no
            g=0;
            for a=1:b  %b: # tramos
                if xy>1 %xy: ramales o derivaciones
                    for k=1:xy % Ayuda a seleccionar los tramos conectados al tramo en cuestión
                        if adjcb(a,k)==i-1 %Verifica los tramos conectados directamente a troncal
                            u=adjcb(a,k);
                            vb(i,j)=((vb(u,j))-((Ibr(i-1,j))*(complex((R(i-1,1)),X(i-1,1))))); %Asigna tensiones en los nodos
                            g=1;
                        end                   
                    end
                end
            end
                
            if g==0
                vb(i,j)=((vb(i-1,j))-((Ibr(i-1,j))*(complex((R(i-1,1)),X(i-1,1)))));   %De aquí sacar el delta de tensión para comparar con el error
            end
        end
    end
    
    s=s+1; % Comparación entre delta new con delta old
    
end

Iload;
Ibr;
vb
vbp=[abs(vb) angle(vb)*180/pi]; % Tensiones de fase de nodos

toc; % Tiempo en hacer iteración
for i=1:no
    va(i,2:3)=vbp(i,1:2);
end
for i=1:no
    va(i,1)=i;
end
va;

Ibrp=[abs(Ibr) angle(Ibr)*180/pi]; % Corrientes de fase de tramos 
% PL(1,1)=0;
% QL(1,1)=0;

% losses
% for f=1:br
%     Pl(f,1)=(Ibrp(f,1)^2)*R(f,1);
%     Ql(f,1)=X(f,1)*(Ibrp(f,1)^2);
%     PL(1,1)=PL(1,1)+Pl(f,1);
%     QL(1,1)=QL(1,1)+Ql(f,1);
% end
% 
% Plosskw=(Pl)*100000000
% Qlosskw=(Ql)*100000000
% PL=(PL)*100000000
% QL=(QL)*100000000


voltage = vbp(:,1);
angle = vbp(:,2)%*(pi/180) % ángulos en grados;

%=====================================================================================
%
volt=voltage*KVb;

tetha1=120*pi/180;
tetha2=240*pi/180;

ang1=[angle(1) angle(1)+(tetha1) angle(1)+(tetha2)];
ang2=[angle(2) angle(2)+(tetha1) angle(2)+(tetha2)];
ang3=[angle(3) angle(3)+(tetha1) angle(3)+(tetha2)];
ang4=[angle(4) angle(4)+(tetha1) angle(4)+(tetha2)];

ang=[ang1;ang2;ang3;ang4]';

for i=1:br
    for j=1:no
        Vpre(i,j)=volt(i)*exp(sqrt(-1)*ang(i,j));
    end
end

%Corrientes de carga en prefalla
Pot=[m(:,2) m(:,3)];
Pot(1,:)=[];

for i=1:br
    for j=1:br
        Ilpre(i,j)=complex(Pot(j,1),Pot(j,2)) / (sqrt(3) * Vpre(i,j));
    end
end

%Corriente Subestación prefalla
for i=1:br
    for j=1:br
        Isubpre(i,1)=sum(Ilpre(i,:));
    end
end

Vpre % Fasores de tensiones en la subestación y en los nodos
%Ibrp(:,1)*(MVAb/(sqrt(3) * KVb))*sqrt(2)  %Corrientes por tramos, entre nodo p y nodo q

%Falta cuadrar fasores de corrientes para cada fase

Inode=Ibrp(:,1)*(MVAb/(sqrt(3) * KVb));
anglenode=Ibrp(:,2)*pi/180;

Inod=[Inode anglenode];

ang1=[anglenode(1) anglenode(1)+(tetha1) anglenode(1)+(tetha2)];
ang2=[anglenode(2) anglenode(2)+(tetha1) anglenode(2)+(tetha2)];
ang3=[anglenode(3) anglenode(3)+(tetha1) anglenode(3)+(tetha2)];

angul=[ang1;ang2;ang3]';

for i=1:br
    for j=1:br
        Ipre(i,j)=Inode(i)*exp(sqrt(-1)*angul(i,j));
    end
end
Ipref=Ipre.';
abs(Ipre.')

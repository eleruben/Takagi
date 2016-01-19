function [MagTenPos, AngTenPos, MagIPos, AngIPos]=flujo_carga_falla(Vsfalla,Isfalla, mx, lx, Sb, Vbas )

% ALGORITMO PARA FLUJO DE POTENCIA EN FALLA

format long;
tic %Inicia conteo de tiempo de simulación
%Datos de potencias activa (columna 2) y reactiva (columna 3)
%m=[1 2 3 4; 0 67.5e3 67.5e3 67.5e3; 0 32.69e3 32.69e3 32.69e3; 0 0 0 0]';

%m=[1 2 3 4 5 ; 0 Pact Pact Pact Pact; 0 Qreact Qreact Qreact Qreact; 0 0 0 0 0]';

m=mx;

%Datos de resistencia (columna 4) y reactancia (columna 5)
%l=[1 2 3; 1 2 3; 2 3 4; 0.2746 0.1373 0.2059; 0.0040 0.0020 0.0030]';

%l=[1 2 3 4; 1 2 2 4; 2 3 4 5; Rs Rs Rs Rs; Xs Xs Xs Xs]';

l=lx;

m,l

Vsub=Vsfalla;
Isub=Isfalla;

br=length(l(:,1));   %ramas
no=length(m(:,1));   %nodos
Sbase=Sb;  %potencia base
Vbase=Vbas;  %tensión base
Zb=(Vbase^2)/Sbase; %impedancia base
% Per unit Values  para resistencias, reactancias, potencias activa y
% reactiva
for i=1:br %Resistencia y reactancia de la línea
    R(i,1)=(l(i,4))/Zb;  
    X(i,1)=(l(i,5))/Zb;
end
for i=1:no %Potencias consumidas de cada nodo
    P(i,1)=((m(i,2))/(Sbase));
    Q(i,1)=((m(i,3))/(Sbase));
end
for i=1:length(Vsub) %Tensiones y corrientes vistas en S/E para falla en pu
    Vs(i)=Vsub(i)/Vbase;
    Is(i)=Isub(i)/(Sbase/Vbase);
end

% R
% X
% P
% Q
% Vs
% Is

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
% C
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
% endnode

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

for i=1:h %Organiza en una matriz cada derivación por filas, desde cada nodo final al inicial
    g(i,1)=endnode(i,1);
end
g;

w=length(g(1,:)); %Número de nodos de la troncal más larga

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

for i=1:x-1 %Elimina la fila 1 de la matriz
    for j=1:ab
        adjcb(i,j)=adjb(i+1,j);
    end
end

adjcb; %Matriz que tiene las derivaciones sin tener en cuenta los tramos conectados directamente con troncal
%Muestra los tramos conectados a cada unos los tramos (filas)

%Cálculos de tensión y corriente
% voltage current program

b=length(adjcb);  %Cantidad de filas de la matriz adjcb => # cantidad de tramos

for i=1:no %Inicializa el vector de tensión con "unos"
    for j=1:3
        vb(i,j)=Vs(j); %Matriz de inicialización de tensiones Vnodo=Vsubestación_falla //// filas: nodos, columnas: fases
    end
end

%===============================================================================
%===============================================================================
%CÁLCULO ITERATIVO

for i=1:3 % Número de fases
    Ssub(i)=Vs(i)*(Is(i))';
end

Ssub;

S=complex(P(:,1),Q(:,1));

for i=1:br
    Ssum=abs(sum(S));
end

Ssum;

for i=1:no
    for j=1:3
        Snode(i,j)=Ssub(j)*(abs(S(i)) / Ssum);
    end
end

Snode;

for s=1:100 %Definición del error ==> Define número de iteraciones
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
    vb;
    s=s+1; % Comparación entre delta new con delta old
    
end

Iload;
Ibr;
vb;

toc; % Tiempo en hacer iteración
vj=vb*Vbase;

Itramo=Ibr*(Sbase/Vbase);
% vj,Itramo

Vjpos=abs(vj)*sqrt(2);
angVjpos=angle(vj);

MagTenPos=Vjpos;
AngTenPos=angVjpos;

Itramopos=abs(Itramo)*sqrt(2);
angItramopos=angle(Itramo);

% Iposf=Itramopos(2,2);
% angIposf=angItramopos(2,2);

MagIPos=Itramopos;
AngIPos=angItramopos;



% MagIPos=abs(Itramo(2,2)+(Isfalla(2)-Iprefalla(1,2)));
% AngIPos=angle(Itramo(2,2)+(Isfalla(2)-Iprefalla(1,2)));
% 
% MagTenPos=Vjpos(2,2);
% AngTenPos=angVjpos(2,2);

% [f m p]=lsq(Vtramo5(145:177,2),tout(145:177)');
% 
% MagTenPos=m;
% AngTenPos=p;
% 
% [f m p]=lsq(Itramo5(145:177,2),tout(145:177)');
% 
% MagIPos=m;
% AngIPos=p;


function [Iprefalla, angIprefalla, Ipre]=flujo_carga_prefalla(mx, lx, Sb, Vbas)

% ALGORITMO PARA FLUJO DE POTENCIA EN PREFALLA

format long;
tic
%Datos de potencias activa (columna 2) y reactiva (columna 3)

m=mx;

%Datos de resistencia (columna 4) y reactancia (columna 5)

l=lx;

br=length(l(:,1));   %ramas
no=length(m(:,1));   %nodos
Sbase=Sb;  %potencia base
Vbase=Vbas;  %tensión base
Zb=(Vbase^2)/Sbase; %impedancia base
% Per unit Values  para resistencias, reactancias, potencias activa y
% reactiva
for i=1:br
    R(i,1)=(l(i,4))/Zb;  
    X(i,1)=(l(i,5))/Zb;
end
for i=1:no
    P(i,1)=((m(i,2))/(Sbase));
    Q(i,1)=((m(i,3))/(Sbase));
end
% R
% X
% P
% Q
C=zeros(br,no); % matriz de tamaño tramos * nodos
for i=1:br
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
for i=1:no    % Determina los nodos finales
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
for j=1:h   % Determina los nodos involucrados desde el nodo terminal al nodo 1
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

% g

for i=1:h
    g(i,1)=endnode(i,1);
end
g;
% g
w=length(g(1,:))
% w
for i=1:h %Organiza la matriz " g "
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
% g
for k=1:br  %Matriz adjunta de " g "
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
% adjb
for i=1:br-1  %Matriz adjunta de la adjunta de " g "
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
for i=1:x  %Matriz adjunta de la adjunta de la adjunta
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
for i=1:x-1
    for j=1:ab
        adjcb(i,j)=adjb(i+1,j);
    end
end
b=length(adjcb);  %asocia cantidad de datos en columna - 1

%Cálculos de tensión y corriente
% voltage current program

for i=1:no %Inicializa el vector de tensión con "unos"
    for j=1:3
        vb(i,j)=1;
    end
end
for s=1:10
    for i=1:no
        for j=1:3
            nlc(i,j)=conj(complex(P(i,1),Q(i,1)))/(vb(i,j));
        end
    end
    nlc;
    for i=1:br  %borra el primer dato porque es cero de nlc
        for j=1:3
        Ibr(i,j)=nlc(i+1,j);
        end
    end
    Ibr;
    xy=length(adjcb(1,:)); %columnas de la última matriz adjunta

        for j=1:3
            for i=br-1:-1:1
                for k=1:xy
                    if adjcb(i,k)~=0
                        u=adjcb(i,k);
                        %Ibr(i,1)=nlc(i+1,1)+Ibr(k,1);
                        Ibr(i,j)=Ibr(i,j)+Ibr(u,j);
                    end
                end      
            end
        end
Ibr;

% for i=2:no
%       g=0;
%       for a=1:b 
%           if xy>1
%             if adjcb(a,2)==i-1 
%                 u=adjcb(a,1);
%                 vb(i,1)=((vb(u,1))-((Ibr(i-1,1))*(complex((R(i-1,1)),X(i-1,1)))));
%                 g=1;
%             end
%             if adjcb(a,3)==i-1 
%                 u=adjcb(a,1);
%                 vb(i,1)=((vb(u,1))-((Ibr(i-1,1))*(complex((R(i-1,1)),X(i-1,1)))));
%                 g=1;
%             end
%           end
%         end
%         if g==0
%             vb(i,1)=((vb(i-1,1))-((Ibr(i-1,1))*(complex((R(i-1,1)),X(i-1,1)))));
%         end
% end

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

s=s+1;
end
nlc;
Ibr;
% vb

toc; % Tiempo en hacer iteración

Itramopre=Ibr*(Sbase/Vbase);

Iprefalla=abs(Itramopre)*sqrt(2);
angIprefalla=angle(Itramopre);
Ipre=Ibr*(Sbase/Vbase)*sqrt(2);



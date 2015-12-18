% ALGORITMO PARA FLUJO DE POTENCIA EN PREFALLA
clc;
clear all;
format short;
tic
%Datos de potencias activa (columna 2) y reactiva (columna 3)
m=[1 2 3 4; 0 67.5e3 67.5e3 67.5e3; 0 32.69e3 32.69e3 32.69e3; 0 0 0 0]';
%Datos de resistencia (columna 4) y reactancia (columna 5)
l=[1 2 3; 1 2 3; 2 3 4; 0.2746 0.1373 0.2059; 0.0040 0.0020 0.0030]';

br=length(l(:,1));   %ramas
no=length(m(:,1));   %nodos
MVAb=100000000;  %potencia base
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
R
X
P
Q
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
C
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
endnode
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
for i=1:h
    g(i,1)=endnode(i,1);
end
g;
w=length(g(1,:))
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
    vb(i,1)=1;
end
for s=1:10
for i=1:no
    nlc(i,1)=conj(complex(P(i,1),Q(i,1)))/(vb(i,1));
end
nlc;
for i=1:br  %borra el primer dato porque es cero de nlc
    Ibr(i,1)=nlc(i+1,1);
end
Ibr;
xy=length(adjcb(1,:)); %columnas de la última matriz adjunta
for i=br-1:-1:1
    for k=1:xy
        if adjcb(i,k)~=0
            u=adjcb(i,k);
            %Ibr(i,1)=nlc(i+1,1)+Ibr(k,1);
            Ibr(i,1)=Ibr(i,1)+Ibr(u,1);
        end
    end      
end
Ibr;
for i=2:no
      g=0;
      for a=1:b 
          if xy>1
            if adjcb(a,2)==i-1 
                u=adjcb(a,1);
                vb(i,1)=((vb(u,1))-((Ibr(i-1,1))*(complex((R(i-1,1)),X(i-1,1)))));
                g=1;
            end
            if adjcb(a,3)==i-1 
                u=adjcb(a,1);
                vb(i,1)=((vb(u,1))-((Ibr(i-1,1))*(complex((R(i-1,1)),X(i-1,1)))));
                g=1;
            end
          end
        end
        if g==0
            vb(i,1)=((vb(i-1,1))-((Ibr(i-1,1))*(complex((R(i-1,1)),X(i-1,1)))));
        end
end
s=s+1;
end
nlc;
Ibr;
vb
vbp=[abs(vb) angle(vb)*180/pi]

toc;
for i=1:no
    va(i,2:3)=vbp(i,1:2);
end
for i=1:no
    va(i,1)=i;
end
va;

Ibrp=[abs(Ibr) angle(Ibr)*180/pi];
PL(1,1)=0;
QL(1,1)=0;

% losses
for f=1:br
    Pl(f,1)=(Ibrp(f,1)^2)*R(f,1);
    Ql(f,1)=X(f,1)*(Ibrp(f,1)^2);
    PL(1,1)=PL(1,1)+Pl(f,1);
    QL(1,1)=QL(1,1)+Ql(f,1);
end

Plosskw=(Pl)*100000000
Qlosskw=(Ql)*100000000
PL=(PL)*100000000
QL=(QL)*100000000


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

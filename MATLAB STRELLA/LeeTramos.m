function [tramos,nodoP,nodoQ,z,PInst]=LeeTramos(zth)
% Lee los datos del sistema y los guarda en la forma requerida
% (Remplazar por una rutina de lectura en el caso general)
% Los tramos deben ir ordenados de manera que el 
% nodoP ya haya sido incluido.
% Para ello, basta ordenar los nodos empezando por la subestacion
% y continuar con tramos conectados a algun nodo ya existente.
% El primer tramo SIEMPRE debe ser el equivalente thevenin.
% La subestacion SIEMPRE debe ser el nodo numero 1
%
% Por lo tanto, las siguientes instrucciones siempre deben estar 
% incluidas:
PInst(2) = 0;
nodoP(1) = 1;
nodoQ(1) = 2;
z(1) = zth;
%
% El resto de datos si son los de los tramos reales
%
%PInst(2) = 1.1;
%nodoP(2) = 2;
%nodoQ(2) = 3;
%PInst(3) = 0.8;
%z(2) = 0.005+0.025j;
%nodoP(3) = 3;
%nodoQ(3) = 4;
%PInst(4) = 0.5;
%z(3) = 0.005+0.025j;
%nodoP(4) = 3;
%nodoQ(4) = 5;
%PInst(5) = 0.4;
%z(4) = 0.01+0.04j;
%tramos = 4;

%tramos,nodoP,nodoQ,z,PInst
%tramos = 3;
%PInst(2) = 0;
%nodoP(2) = 2;
%nodoQ(2) = 3;
%PInst(3) = 1+.4j;
%z(2) = 0.0165 + 0.0262i;
%z(2) = 0.0186+0.0466j;
%nodoP(3) = 2;
%nodoQ(3) = 4;
%PInst(4) = 0.9+.45j;
%z(3) = 0.0197 + 0.0205i;
%z(3) = 0.0221+0.0359j;
%[PtoIni PtoFin Long Material Calibre]=textread('SF15.txt','%u %u %u %s %s');
[PtoIni PtoFin Long Material Calibre]=textread('us16.txt','%u %u %u %s %s');
MatrizImpedanciaLineas;

Nombres=zeros(1);
Nombres(1)=PtoIni(1);
for I=1:size(PtoIni,1)
   ind=0;
   for J=1:size(Nombres,1)   
      if PtoIni(I)==Nombres(J)
         ind=1;
         J=size(Nombres,1);
      end
   end
   if ind==0
   	Nombres = [ Nombres; PtoIni(I)];
   end
end

for I=1:size(PtoFin,1)
   ind=0;
   for J=1:size(Nombres,1)   
      if PtoFin(I)==Nombres(J)
         ind=1;
         J=size(Nombres,1);
      end
   end
   if ind==0
   	Nombres = [ Nombres; PtoFin(I)];
   end
end

NodoP0=zeros(size(PtoIni));
NodoQ0=zeros(size(PtoIni));
for I=1:size(PtoIni,1)
   ind=find(Nombres==PtoIni(I));
   NodoP0(I)=ind(1);
   ind=find(Nombres==PtoFin(I));
   NodoQ0(I)=ind(1);
end

nodoP = zeros(1);
nodoQ = zeros(1);
z = zeros(1);
for I=1:size(NodoP0,1)
   ind2=0;
   if NodoP0(I)<NodoQ0(I)
      ind=find(nodoP==NodoP0(I));
      if (isempty(ind))
         nodoP = [nodoP; NodoP0(I)];
         nodoQ = [nodoQ; NodoQ0(I)];
      	if Buscar(ImpedanciaLineas.Tipo, [char(Material(I)) '_' char(Calibre(I))])
            z = [z (Long(I)/1000)*ImpedanciaLineas.Valor(Buscar(ImpedanciaLineas.Tipo, [char(Material(I)) '_' char(Calibre(I))]))];
         else
            z = [z (Long(I)/1000)*ImpedanciaLineas.Valor(Buscar(ImpedanciaLineas.Tipo, 'CU_4/0'))];
        end
      else
         NodoQ1=nodoQ(ind);
         for J=1:size(NodoQ1)
            if NodoQ1(J)==NodoQ0(I)
               ind2=1;
               J=size(NodoQ1);
            end
         end
         if(ind2==0)
            nodoP = [nodoP; NodoP0(I)];
            nodoQ = [nodoQ; NodoQ0(I)];
         	if Buscar(ImpedanciaLineas.Tipo, [char(Material(I)) '_' char(Calibre(I))])
            	z = [z (Long(I)/1000)*ImpedanciaLineas.Valor(Buscar(ImpedanciaLineas.Tipo, [char(Material(I)) '_' char(Calibre(I))]))];
	        else
   	            z = [z (Long(I)/1000)*ImpedanciaLineas.Valor(Buscar(ImpedanciaLineas.Tipo, 'CU_4/0'))];
      	    end
         end
      end
   end
end
nodoP = nodoP(2:end);
nodoQ = nodoQ(2:end);
z = z(2:end);
z = z / 129.96; %Zbase

tramos = size(nodoP,1);

for I=2:size(nodoP,1)+1
	PInst(I)=0;   
end

SumPot=0;
%[Nodo Potencia]= textread('PotenciaSF15.txt','%u %f');
[Nodo Potencia]= textread('Potenciaus16.txt','%u %f');
for I=1:size(Nodo,1)
   PInst(find(Nombres==Nodo(I))) = 0.3*(Potencia(I)*.8+j*Potencia(I)*.6)/1000;
end


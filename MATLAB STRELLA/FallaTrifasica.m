[PtoIni PtoFin Long0 Material Calibre]=textread('us16.txt','%u %u %u %s %s');
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
Long = zeros(1);
for I=1:size(NodoP0,1)
   ind2=0;
   if NodoP0(I)<NodoQ0(I)
      ind=find(nodoP==NodoP0(I));
      if (isempty(ind))
         nodoP = [nodoP; NodoP0(I)];
         nodoQ = [nodoQ; NodoQ0(I)];
         Long = [Long; Long0(I)];
         if Buscar(ImpedanciaLineas.Tipo, [char(Material(I)) '_' char(Calibre(I))])
            z = [z (Long0(I)/1000)*ImpedanciaLineas.Valor(Buscar(ImpedanciaLineas.Tipo, [char(Material(I)) '_' char(Calibre(I))]))];
         else
            z = [z (Long0(I)/1000)*ImpedanciaLineas.Valor(Buscar(ImpedanciaLineas.Tipo, 'CU_4/0'))];
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
            Long = [Long; Long0(I)];
         	if Buscar(ImpedanciaLineas.Tipo, [char(Material(I)) '_' char(Calibre(I))])
            	z = [z (Long0(I)/1000)*ImpedanciaLineas.Valor(Buscar(ImpedanciaLineas.Tipo, [char(Material(I)) '_' char(Calibre(I))]))];
	         else
   	         z = [z (Long0(I)/1000)*ImpedanciaLineas.Valor(Buscar(ImpedanciaLineas.Tipo, 'CU_4/0'))];
      	   end
         end
      end
   end
end
nodoP = nodoP(2:end);
nodoQ = nodoQ(2:end);
z = z(2:end);
Long = Long(2:end);
z = z / 129.96; %Zbase

z_suma = zeros(size(z));
Long_suma = zeros(size(Long));
for I=1:size(nodoQ,1)
    %nodoFin = nodoQ(I);
    nodoIni = nodoP(I);
    z_suma(I) = z(I);
    Long_suma(I) = Long(I);
    J=I;
    while nodoIni~=1
         J = find(nodoQ==nodoIni);
         nodoIni = nodoP(J);
         z_suma(I) = z_suma(I) + z(J);
         Long_suma(I) = Long_suma(I) + Long(J);
    end
end

z_max=max(abs(z_suma));
%z_max = min(abs(z_suma));
for I=7:-1:0
   z_suma=[z_suma;z_suma(1,:)+z_max*(1-I/8)];
end
zMag = abs(z_suma);
zAngle = angle(z_suma)*180/pi;
plot(Long_suma,zMag,'.');
title('Falla Trifasica');
xlabel('Distancia m');
ylabel('Magnitud p.u.');
figure;
plot(Long_suma,zAngle,'.');
title('Falla Trifasica');
xlabel('Distancia m');
ylabel('Angulo º');




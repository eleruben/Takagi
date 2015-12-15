[PtoIni PtoFin Long Material Calibre]=textread('SF15.txt','%u %u %u %s %s');
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
z = z / 129.96;



      
      




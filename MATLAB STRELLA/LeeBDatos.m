function tramos = LeeDatos(archivoCircuito, archivoPotencia)

[PtoIni PtoFin Long Material Calibre]=textread(archivoCircuito,'%u %u %u %s %s');
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

Pos = 0;
for I=1:size(NodoP0,1)
   ind2=0;
   if NodoP0(I)<NodoQ0(I)
      ind=find(nodoP==NodoP0(I));
      if (isempty(ind))
          Pos = Pos + 1;
          tramos(Pos).nodoP = NodoP0(I);
          tramos(Pos).nodoQ = NodoQ0(I);
          tramos(Pos).long = Long(I);
          if Buscar(ImpedanciaLineas(1).Tipo, [char(Material(I)) '_' char(Calibre(I))])
              Pos2 = Buscar(ImpedanciaLineas(1).Tipo, [char(Material(I)) '_' char(Calibre(I))]);
          else
              Pos2 =Buscar(ImpedanciaLineas(1).Tipo, 'CU_4/0');
          end
          tramos(Pos).zabc = ((Long(I)/1000)*ImpedanciaLineas(Pos2).Zabc) / 129.96;
          tramos(Pos).z012 = ((Long(I)/1000)*ImpedanciaLineas(Pos2).Z012) / 129.96;
      else
          NodoQ1=nodoQ(ind);
          for J=1:size(NodoQ1)
              if NodoQ1(J)==NodoQ0(I)
                  ind2=1;
                  J=size(NodoQ1);
              end
          end
          if(ind2==0)
              Pos = Pos + 1;
              tramos(Pos).nodoP = NodoP0(I);
              tramos(Pos).nodoQ = NodoQ0(I);
              tramos(Pos).long = Long(I);
              if Buscar(ImpedanciaLineas(1).Tipo, [char(Material(I)) '_' char(Calibre(I))])
                  Pos2 = Buscar(ImpedanciaLineas(1).Tipo, [char(Material(I)) '_' char(Calibre(I))]);
              else
                  Pos2 =Buscar(ImpedanciaLineas(1).Tipo, 'CU_4/0');
              end
              tramos(Pos).zabc = ((Long(I)/1000)*ImpedanciaLineas(Pos2).zabc) / 129.96;
              tramos(Pos).z012 = ((Long(I)/1000)*ImpedanciaLineas(Pos2).Z012) / 129.96;
          end
      end
   end
end

for I=1:Pos
	tramos(I).PInst=0;   
end

%[Nodo Potencia]= textread('PotenciaSF15.txt','%u %f');
[Nodo Potencia]= textread(archivoPotencia,'%u %f');
for I=1:size(Nodo,1)
   tramos(find(Nombres==Nodo(I))).PInst = Potencia(I);
end

for I=1:Pos
    tramos(I).Usuarios = [0 0 0];
    tramos(I).Sd = 0;
    tramos(I).Nombres = Nombres(tramos(I).nodoQ);
end

save('tramos.mat','tramos');


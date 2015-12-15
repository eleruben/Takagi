
load tramos.mat;
[PtoFin Pot]=textread('Potenciaus16.txt','%u %u');
Tramos = size(tramos,2)
Trafos = size(Pot,1)
Sinst = zeros(Tramos,1);
for m=1:Trafos
   k=1;
   while  k < Tramos
      if PtoFin(m) == tramos(k).Nombres
         Sinst(k) = Pot(m);
         break
      else
         k=k+1;
      end
   end
end
for k=1:Tramos
   tramos(k).Pinst=Sinst(k);
end
save('tramos.mat','tramos');

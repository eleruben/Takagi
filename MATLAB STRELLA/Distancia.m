function D = Distancia(rmg, CoorCond)
%D = [rmg dab dac; dab rmg dcb; dac dcb rmg];
Dim = size(CoorCond);
Tam = Dim(1,2);

D = zeros(Tam);
for I = 1:Tam
   D(I,I) = rmg;
end

for I = 1:Tam
   for J = I:Tam
      if (I ~= J)
	      D(I,J) = sqrt (( CoorCond(1,I) - CoorCond(1,J) )^2 + ( CoorCond(2,I) - CoorCond(2,J) )^2);
      	D(J,I) = D(I,J);   
      end
   end
end
      


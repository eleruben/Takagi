function Indice = Buscar(Matriz,Cadena)
Indice=0;
for I=1:size(Matriz,2)
   if (size(Cadena,2)==size(char(Matriz(I)),2))
	   if (prod(double((Cadena==char(Matriz(I))))))
   	   Indice = I;
      	I=size(Matriz,2);
	   end
	end
end

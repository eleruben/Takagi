% Falla en el nodo 7, LP12R
Z6=Zsec(:,6)
IFalla6=3*IBase*V1(1)/(sum(Z6))
abs(IFalla6)
Imedida6=(I0(5)+I1(5)+I2(5))*IBase
abs(Imedida6)
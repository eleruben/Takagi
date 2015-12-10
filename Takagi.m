% Localiza la falla en un circuito de distribucion
% Usando metodo de Takagi


for k=2:ntramos
%   Primero calcula la corriente de superposicion
    Isup=Ifalla-ISE;
%   Calcula la reactancia
%   Nodos del tramo
    np=NodP(k);
    nq=NodQ(k);
    TramoFallado(k)=0;
%   Calcula corriente Is
    Is=Isup+ITramo(k);
%   Calcula voltaje Vs
    Vs=Vfalla-Zsec(2,np)*Is;
    m=imag(Vs*conj(Isup))/imag(tramos(k).Z012(2)*Is*conj(Isup))
    if m  > 0 & m < 1
       TramoFallado(k)=1;
   end
end
NodosEnFalla=TramoFallado>0
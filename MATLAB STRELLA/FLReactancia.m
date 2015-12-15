% Localiza la falla en un circuito de distribucion
% Usando metodo de reactancia
for l=2:nTramos
%   Calcula el voltaje en nodoP durante la falla
%   suponiendo que la falla ocurrio al final del tramo
%   (en el nodoQ)
    INodF = zeros(1,nTramos);
    ITramoF = zeros(1,nTramos);
    INodF = IdFalla;
%se hace un recorrido del for desde nTramos hasta 1
    for k=nTramos:-1:1
       INodF(NodP(k)) = INodF(NodP(k))+INodF(NodQ(k));
       ITramoF(k) = INodF(NodP(k));
    end
    dV = ITramoF.*z1;
    VNodF(1) = VsubFalla;
    for k=1:nTramos
       VNodF(NodQ(k)) = VNodF(NodP(k))-dV(k);
    end
%   Calcula corriente del tramo
    Iabcpq = [Isup+ITramoF(l);a^2*ITramoF(l);a*ITramoF(l)];
    dVabc = tramos(l).Zabc*Iabcpq/tramos(l).Longitud;
    M = [real(dVabc(1)) real(Isup);imag(dVabc(1)) imag(Isup)];
    b = [real(VNodF(NodP(k)));imag(VNodF(NodP(k)))];
    X = M\b;
    m = X(1)
    Rf = X(2);
    TramoFallado(l)=0;
    if m  > -0.05 & m < 1.05
       TramoFallado(l)=1;
    end
end
NodosEnFalla=TramoFallado>0
for k=2:nTramos
%   Calcula la reactancia
%   Nodos del tramo
    np=NodP(k);
    nq=NodQ(k);
    TramoFallado(k)=0;
    Xaparente=imag(Vfalla/(Ifalla+3*k0(k)*Ifalla0));
    Xmin=imag(Zsec(2,np));
    Xmax=imag(Zsec(2,nq));
    if Xaparente  > Xmin & Xaparente < Xmax
       TramoFallado(k)=1;
   end
end
NodosEnFalla=TramoFallado>0

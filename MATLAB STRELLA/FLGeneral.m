% Localiza una falla L-T en un circuito de distribucion
% Usando metodo de Senger
% Calcula el flujo de carga solo para las corrientes de carga durante la
% falla
INodF = zeros(1,nTramos);
ITramoF = zeros(1,nTramos);
INodF = IdFalla;
for k=nTramos:-1:1
    INodF(NodP(k)) = INodF(NodP(k))+INodF(NodQ(k));
    ITramoF(k) = INodF(NodP(k));
end
dV = ITramoF.*z1;
VNodF(1) = VsubFalla;
for k=1:nTramos
    VNodF(NodQ(k)) = VNodF(NodP(k))-dV(k);
end
for l=1:nTramos
% Calcula la caida de voltaje desde la subestacion, debida a la corriente
% de falla
    dVabc = ZABC(:,:,NodP(l))*Isup;
    Vpabc = VNodF(NodP(l))-dVabc;
%   Calcula el voltaje en nodoP durante la falla
%   suponiendo que la falla ocurrio al final del tramo
%   (en el nodoQ)
%   Calcula corriente del tramo
    Iabcpq = Isup+[ITramoF(l);a^2*ITramoF(l);a*ITramoF(l)];
    zIabc = tramos(l).Zabc*Iabcpq/tramos(l).Longitud;
    M = [real(zIabc(1)) real(Isup(1));imag(zIabc(1)) imag(Isup(1))];
    b = [real(VNodF(NodP(k)));imag(VNodF(NodP(k)))];
    X = M\b;
    m = X(1)
    Rf = X(2);
    TramoFallado(l)=0;
    if m  > -0.05 & m < 1.05
       TramoFallado(l)=1;
    end
end
NodosEnFalla = TramoFallado>0

for i=1:3
    z=impedancia(zCircuito(i,1), zCircuito(i,2), zCircuito(i,3), zCircuito(i,4), zCircuito(i,5));
    [FasorIpre, MagIpre, AngIpre]=lsq(I(1:32,1,i),tout(1:32,1));
    [FasorTenPos, MagTenPos, AngTenPos]=lsq(V(96:128,   1,i),tout(96:128,1));
    [FasorIPos, MagIPos, AngIPos]=lsq(I(96:128,1,i),tout(96:128,1));
    m=takagi2(MagIpre, AngIpre, MagTenPos, AngTenPos, MagIPos, AngIPos,real(z), imag(z))
end
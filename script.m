
for i=1:3
    z=impedancia(zCircuito(i,1), zCircuito(i,2), zCircuito(i,3), zCircuito(i,4), zCircuito(i,5));
    [FasorIpre, MagIpre, AngIpre]=lsq(I(iniPre:iniPre+31,faseEnFalla,i),tout(iniPre:iniPre+31,1));
    [FasorTenPos, MagTenPos, AngTenPos]=lsq(V(iniPost:iniPost+31, faseEnFalla,i),tout(iniPost:iniPost+31,1));
    [FasorIPos, MagIPos, AngIPos]=lsq(I(iniPost:iniPost+31,faseEnFalla,i),tout(iniPost:iniPost+31,1));
    m=takagi2(MagIpre, AngIpre, MagTenPos, AngTenPos, MagIPos, AngIPos,real(z), imag(z))
end
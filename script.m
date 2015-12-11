z=impedancia(4*0.01273, 4*0.3864, 4*0.9337e-3, 4*4.1264e-3, 20);
[FasorIpre, MagIpre, AngIpre]=lsq(I3(1:32,1),tout(1:32,1));
[FasorTenPos, MagTenPos, AngTenPos]=lsq(V3(96:128,1),tout(96:128,1));
[FasorIPos, MagIPos, AngIPos]=lsq(I3(96:128,1),tout(96:128,1));
m=takagi2(MagIpre, AngIpre, MagTenPos, AngTenPos, MagIPos, AngIPos,real(z), imag(z))
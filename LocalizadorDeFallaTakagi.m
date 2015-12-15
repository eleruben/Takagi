%Creación del circuito con los parametros deseados
zCircuito=  [   0.01273,    0.3864,     0.9337e-3,      4.1264e-3,      20;
                2*0.01273,  2*0.3864,   2*0.9337e-3,    2*4.1264e-3,    20;
                4*0.01273,  4*0.3864,   4*0.9337e-3,    4*4.1264e-3,    20; ];
          
V=V1;
V(:,:,2)=V2;
V(:,:,3)=V3;
I=I1;
I(:,:,2)=I2;
I(:,:,3)=I3;
%Verificacion de la fase en falla
for i=1:3
   [fase, iniPre, iniPost]=verificar(I1(:,i),tout);
   if fase == 1
      faseEnFalla=i;
      break
   end
end
%Localización de la falla usando takagi

for i=1:3
    z=impedancia(zCircuito(i,1), zCircuito(i,2), zCircuito(i,3), zCircuito(i,4), zCircuito(i,5));
    [FasorIpre, MagIpre, AngIpre]=lsq(I(iniPre:iniPre+31,faseEnFalla,i),tout(iniPre:iniPre+31,1));
    [FasorTenPos, MagTenPos, AngTenPos]=lsq(V(iniPost:iniPost+31, faseEnFalla,i),tout(iniPost:iniPost+31,1));
    [FasorIPos, MagIPos, AngIPos]=lsq(I(iniPost:iniPost+31,faseEnFalla,i),tout(iniPost:iniPost+31,1));
    m=takagi2(MagIpre, AngIpre, MagTenPos, AngTenPos, MagIPos, AngIPos,real(z), imag(z));
    if m > 0 && m <= 1 
       M=m;
       seccion=i;
    end
end
disp('La falla se encuentra a: ')
disp(M*zCircuito(i,5))
disp('Km del inicio del segmento:')
disp(seccion)
disp('en la fase:')
disp(faseEnFalla)
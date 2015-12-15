Pcomp=VA(1)*conj(IA(1))+VB(1)*conj(IB(1))+VC(1)*conj(IC(1))
pinstant=Ia.*Va+Ib.*Vb+Ic.*Vc;
Pprom=sum(pinstant(1:16))*2/16
Psec=3*(V1(1)*conj(I1(1))+V0(1)*conj(I0(1))+V2(1)*conj(I2(1)))


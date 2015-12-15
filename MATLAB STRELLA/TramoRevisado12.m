% Tramos revisados
VBase=34.5;
SBase=1;
ZBase=VBase^2/SBase;
IBase=SBase*1000/(sqrt(3)*VBase)
NodoP=[1:9]
NodoQ=[2:10]
longitud=[65 56 89 11 21 119 366 366 194]
% Valores de Codensa
zth1=(0.08590+0.43232j)/100;
zth2=(0.08634+0.43270j)/100;
zth0=(0.02015+0.16570j)/100;
a=(-1+sqrt(3)*j)/2;
Tfs=[1 1 1;1 a^2 a;1 a a^2];
Tsf=inv(Tfs);
zc1=(0.228+0.332j)/1609
zc0=(0.512+3.612j)/1609
z1pu=zc1/ZBase
z0pu=zc0/ZBase
zphase=Tfs*diag([z0pu z1pu z1pu])*Tsf;
Z1Tramo=z1pu*longitud;
Z0Tramo=z0pu*longitud;
for k=1:9
    Zseq(2,k)=Z1Tramo(k);
    Zseq(3,k)=Z1Tramo(k);
    Zseq(1,k)=Z0Tramo(k);
    Zphase(:,:,k)=zphase*longitud(k);
end
Zbusf=zeros(3,3,10);
Zbusf(:,:,1) = Tfs*diag([Zth0 Zth1 Zth1])*Tsf;
Zbuss = zeros(3,8);
Zbuss(:,1) = [zth0; zth1; zth2];
for k=1:9
    NodAnt = NodoP(k);
    Nodo = NodoQ(k);
    Zbusf(:,:,Nodo) = Zbusf(:,:,NodAnt)+Zphase(:,:,k);
	Zbuss(:,Nodo) = Zbuss(:,NodAnt)+Zseq(:,k);
end
% Voltaje nodo 7 durante la falla
vp=Vfase(:,5)-Zbusf(:,7)*Ifase(5)
abs(vp)
% Falla en el nodo 8, LP12R
Z8=Zbuss(:,8)
IFalla8=3*IBase*V1(1)/(sum(Z8))
abs(IFalla8)
FactorI=abs(V1(5)/V1(1))
Imedida8=(I0(5)+I1(5)+I2(5)-FactorI*I1(1))*IBase
abs(Imedida8)
longA8=sum(longitud(1:7))
ZA8=[z0pu z1pu z1pu]*longA8
IFalla8E=3*IBase*V1(1)/(sum(ZA8))
abs(IFalla8E)
z0E=3*V1(1)*a*IBase/Imedida8-sum(ZA8)
IFalla8E=3*IBase*V1(1)/(sum(ZA8)+z0E)
abs(IFalla8E)
% Calcula el voltaje en el nodo p
p=4
Voltpabc=Vfase(:,5)-Zbusf(:,:,p)*Ifase(:,5)
abs(Voltpabc)
Iabcpq = Ifase(:,5);
Ifalla=Iabcpq-FactorI*Ifase(1)
zIabc = Zbusf(:,:,p)*Iabcpq/longitud(p);
M = [real(zIabc) real(Ifalla);imag(zIabc) imag(Ifalla)];
b = [real(Voltpabc);imag(Voltpabc)];
X = M\b;
m = X(1)
Rf = X(2);

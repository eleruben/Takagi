Spre=complex(Pot(:,1),Pot(:,2))
Vsub=Vspos;

for i=1:3
    Iload1(1,i)=(Spre(1) / (abs(Vpre(i,1)))^2)*Vsub(i);
end

Iload1.'

for i=1:3
    Iload2(1,i)=(Spre(2) / (abs(Vpre(i,2)))^2)*Vsub(i);
end

Iload2.'

for i=1:3
    Iload3(1,i)=(Spre(3) / (abs(Vpre(i,3)))^2)*Vsub(i);
end

Iload3.'

Iload=[Iload1; Iload2; Iload3].' % datos de cada nodo por columnas
sqrt(2) * abs(Iload)
sqrt(2) * abs(Ip)

Ia=;
Iapre=Ipre(1,1)

If=Ia-Iapre;
If

r0=0.01273;
r1=0.3864;
l0=0.9337e-3;
l1=4.1264e-3;

Rs=(2*r1 +r0)/3;
Ls=(2*l1+l0)/3
Rm=(r0-r1)/3;
Lm=(l0-l1)/3;

Xs=2*pi*60*Ls;
Xm=2*pi*60*Lm;

zs=complex(Rs,Xs);
zm=complex(Rm,Xm);

for i=1:br
    for j=1:br
        if i==j
            Zmatriz(i,j)=zs;
        else
            Zmatriz(i,j)=zm;
        end
    end
end

Zmatriz


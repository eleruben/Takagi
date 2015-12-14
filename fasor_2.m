%NODO 02
%fasor tensión prefalla
VA2=v2(:,1,:);
[f2 m2 p2]=lsq(VA2(88:120),tout(88:120)');
Va2=m2*exp(j*p2);

%fasor corriente prefalla
IA2=i2(:,1,:);
[f2 m2 p2]=lsq(IA2(88:120),tout(88:120)');
Ia2=m2*exp(j*p2);

%===============================================================
%fasor tensión prefalla
VB2=v2(:,2,:);
[f2 m2 p2]=lsq(VB2(88:120),tout(88:120)');
Vb2=m2*exp(j*p2);
        
%fasor corriente prefalla
IB2=i2(:,2,:);
[f2 m2 p2]=lsq(IB2(88:120),tout(88:120)');
Ib2=m2*exp(j*p2);

%================================================================
%fasor tensión prefalla
VC2=v2(:,3,:);
[f2 m2 p2]=lsq(VC2(88:120),tout(88:120)');
Vc2=m2*exp(j*p2);
        
%fasor corriente prefalla
IC2=i2(:,3,:);
[f2 m2 p2]=lsq(IC2(88:120),tout(88:120)');
Ic2=m2*exp(j*p2);

Vp2=[Va2 Vb2 Vc2];
Ip2=[Ia2 Ib2 Ic2];

%°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
%NODO 01
%fasor tensión prefalla
VA1=v1(:,1,:);
[f1 m1 p1]=lsq(VA1(88:120),tout(88:120)');
Va1=m1*exp(j*p1);

%fasor corriente prefalla
IA1=i1(:,1,:);
[f1 m1 p1]=lsq(IA1(88:120),tout(88:120)');
Ia1=m1*exp(j*p1);

%===============================================================
%fasor tensión prefalla
VB1=v1(:,2,:);
[f1 m1 p1]=lsq(VB1(88:120),tout(88:120)');
Vb1=m1*exp(j*p1);
        
%fasor corriente prefalla
IB1=i1(:,2,:);
[f1 m1 p1]=lsq(IB1(88:120),tout(88:120)');
Ib1=m1*exp(j*p1);

%================================================================
%fasor tensión prefalla
VC1=v1(:,3,:);
[f1 m1 p1]=lsq(VC1(88:120),tout(88:120)');
Vc1=m1*exp(j*p1);
        
%fasor corriente prefalla
IC1=i1(:,3,:);
[f1 m1 p1]=lsq(IC1(88:120),tout(88:120)');
Ic1=m1*exp(j*p1);

Vp1=[Va1 Vb1 Vc1];
Ip1=[Ia1 Ib1 Ic1];

%°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
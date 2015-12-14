%SUBESTACIÓN

%fasor corriente posfalla
IA=ip1(:,1,:);
[f m p]=lsq(IA(97:129),tout(97:129)');
Ia=m*exp(j*p);

%===============================================================
      
%fasor corriente posfalla
IB=ip1(:,2,:);
[f m p]=lsq(IB(97:129),tout(97:129)');
Ib=m*exp(j*p);

%================================================================
    
%fasor corriente prefalla
IC=ip1(:,3,:);
[f m p]=lsq(IC(97:129),tout(97:129)');
Ic=m*exp(j*p);

Isu=[Ia Ib Ic];

%°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
%°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

%NODO 01
%fasor tensión posfalla
VA=v1(:,1,:);
[f m p]=lsq(VA(97:129),tout(97:129)');
Va=m*exp(j*p);

%fasor corriente posfalla
IA=i1(:,1,:);
[f m p]=lsq(IA(97:129),tout(97:129)');
Ia=m*exp(j*p);

%===============================================================
%fasor tensión posfalla
VB=v1(:,2,:);
[f m p]=lsq(VB(97:129),tout(97:129)');
Vb=m*exp(j*p);
        
%fasor corriente posfalla
IB=i1(:,2,:);
[f m p]=lsq(IB(97:129),tout(97:129)');
Ib=m*exp(j*p);

%================================================================
%fasor tensión posfalla
VC=v1(:,3,:);
[f m p]=lsq(VC(97:129),tout(97:129)');
Vc=m*exp(j*p);
        
%fasor corriente posfalla
IC=i1(:,3,:);
[f m p]=lsq(IC(97:129),tout(97:129)');
Ic=m*exp(j*p);

V1=[Va Vb Vc];
I1=[Ia Ib Ic];

%°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
%°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

%NODO 02

%fasor tensión posfalla
VA=v2(:,1,:);
[f m p]=lsq(VA(97:129),tout(97:129)');
Va=m*exp(j*p);

%fasor corriente posfalla
IA=i2(:,1,:);
[f m p]=lsq(IA(97:129),tout(97:129)');
Ia=m*exp(j*p);

%===============================================================
%fasor tensión posfalla
VB=v2(:,2,:);
[f m p]=lsq(VB(97:129),tout(97:129)');
Vb=m*exp(j*p);
        
%fasor corriente posfalla
IB=i2(:,2,:);
[f m p]=lsq(IB(97:129),tout(97:129)');
Ib=m*exp(j*p);

%================================================================
%fasor tensión posfalla
VC=v2(:,3,:);
[f m p]=lsq(VC(97:129),tout(97:129)');
Vc=m*exp(j*p);
        
%fasor corriente posfalla
IC=i2(:,3,:);
[f m p]=lsq(IC(97:129),tout(97:129)');
Ic=m*exp(j*p);

V2=[Va Vb Vc];
I2=[Ia Ib Ic];

%°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
%°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

%NODO 03

%fasor tensión posfalla
VA=v3(:,1,:);
[f m p]=lsq(VA(97:129),tout(97:129)');
Va=m*exp(j*p);

%fasor corriente posfalla
IA=i3(:,1,:);
[f m p]=lsq(IA(97:129),tout(97:129)');
Ia=m*exp(j*p);

%===============================================================
%fasor tensión posfalla
VB=v3(:,2,:);
[f m p]=lsq(VB(97:129),tout(97:129)');
Vb=m*exp(j*p);
        
%fasor corriente posfalla
IB=i3(:,2,:);
[f m p]=lsq(IB(97:129),tout(97:129)');
Ib=m*exp(j*p);

%================================================================
%fasor tensión posfalla
VC=v3(:,3,:);
[f m p]=lsq(VC(97:129),tout(97:129)');
Vc=m*exp(j*p);
        
%fasor corriente posfalla
IC=i3(:,3,:);
[f m p]=lsq(IC(97:129),tout(97:129)');
Ic=m*exp(j*p);

V3=[Va Vb Vc];
I3=[Ia Ib Ic];

V=[V1;V2;V3]'
I=[I1;I2;I3]'
Isu

%NODO 03

%fasor tensión prefalla
VA3=v3(:,1,:);
[f m p]=lsq(VA3(88:120),tout(88:120)');
Va3=m*exp(j*p);

%fasor corriente prefalla
IA3=i3(:,1,:);
[f m p]=lsq(IA3(88:120),tout(88:120)');
Ia3=m*exp(j*p);

%===============================================================
%fasor tensión prefalla
VB3=v3(:,2,:);
[f m p]=lsq(VB3(88:120),tout(88:120)');
Vb3=m*exp(j*p);
        
%fasor corriente prefalla
IB3=i3(:,2,:);
[f m p]=lsq(IB3(88:120),tout(88:120)');
Ib3=m*exp(j*p);

%================================================================
%fasor tensión prefalla
VC3=v3(:,3,:);
[f m p]=lsq(VC3(88:120),tout(88:120)');
Vc3=m*exp(j*p);
        
%fasor corriente prefalla
IC3=ip3(:,3,:);
[f m p]=lsq(IC3(88:120),tout(88:120)');
Ic3=m*exp(j*p);

Vp3=[Va3 Vb3 Vc3];
Ip3=[Ia3 Ib3 Ic3];

% Vp=(1/sqrt(2))*[Vp1;Vp2;Vp3]'
% Ip=(1/sqrt(2))*[Ip1;Ip2;Ip3]'

Vp=[Vp1;Vp2;Vp3]'
Ip=[Ip1;Ip2;Ip3]'

%=====================================================================

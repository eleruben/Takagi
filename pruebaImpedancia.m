%SUBESTACI�N
%fasor tensi�n prefalla
VA=vs(:,1,:);
[f m p]=lsq(VA(88:120),tout(88:120)');
Va=m*exp(j*p);

%fasor corriente prefalla
IA=is(:,1,:);
[f m p]=lsq(IA(88:120),tout(88:120)');
Ia=m*exp(j*p);

%===============================================================
%fasor tensi�n prefalla
VB=vs(:,2,:);
[f m p]=lsq(VB(88:120),tout(88:120)');
Vb=m*exp(j*p);
        
%fasor corriente prefalla
IB=is(:,2,:);
[f m p]=lsq(IB(88:120),tout(88:120)');
Ib=m*exp(j*p);

%================================================================
%fasor tensi�n prefalla
VC=vs(:,3,:);
[f m p]=lsq(VC(88:120),tout(88:120)');
Vc=m*exp(j*p);
        
%fasor corriente prefalla
IC=is(:,3,:);
[f m p]=lsq(IC(88:120),tout(88:120)');
Ic=m*exp(j*p);

% Vs=(1/sqrt(2))*[Va Vb Vc];
% Is=(1/sqrt(2))*[Ia Ib Ic];

Vs=[Va Vb Vc];
Is=[Ia Ib Ic];

%mag=[abs(Ia) abs(Ib) abs(Ic)]
%ang=[angle(Ia) angle(Ib) angle(Ic)]*180/pi

%P=Vs(1)*Is(1) + Vs(2)*Is(2) + Vs(3)*Is(3);

S=sqrt(3) * abs(Vs(1)) * abs(Is(1));

%�����������������������������������������������������
%��������������������������������������������������������

%��������������������������������������������������������������
% %NODO 01
% %fasor tensi�n prefalla
% VA=v1(:,1,:);
% [f m p]=lsq(VA(88:120),tout(88:120)');
% Va=m*exp(j*p);
% 
% %fasor corriente prefalla
% IA=i1(:,1,:);
% [f m p]=lsq(IA(88:120),tout(88:120)');
% Ia=m*exp(j*p);
% 
% %===============================================================
% %fasor tensi�n prefalla
% VB=v1(:,2,:);
% [f m p]=lsq(VB(88:120),tout(88:120)');
% Vb=m*exp(j*p);
%         
% %fasor corriente prefalla
% IB=i1(:,2,:);
% [f m p]=lsq(IB(88:120),tout(88:120)');
% Ib=m*exp(j*p);
% 
% %================================================================
% %fasor tensi�n prefalla
% VC=v1(:,3,:);
% [f m p]=lsq(VC(88:120),tout(88:120)');
% Vc=m*exp(j*p);
%         
% %fasor corriente prefalla
% IC=i1(:,3,:);
% [f m p]=lsq(IC(88:120),tout(88:120)');
% Ic=m*exp(j*p);
% 
% Vp1=[Va Vb Vc];
% Ip1=[Ia Ib Ic];
% 
% %�����������������������������������������������������
% %��������������������������������������������������������

% %NODO 02
% 
% %fasor tensi�n prefalla
% VA=v2(:,1,:);
% [f m p]=lsq(VA(88:120),tout(88:120)');
% Va=m*exp(j*p);
% 
% %fasor corriente prefalla
% IA=i2(:,1,:);
% [f m p]=lsq(IA(88:120),tout(88:120)');
% Ia=m*exp(j*p);
% 
% %===============================================================
% %fasor tensi�n prefalla
% VB=v2(:,2,:);
% [f m p]=lsq(VB(88:120),tout(88:120)');
% Vb=m*exp(j*p);
%         
% %fasor corriente prefalla
% IB=i2(:,2,:);
% [f m p]=lsq(IB(88:120),tout(88:120)');
% Ib=m*exp(j*p);
% 
% %================================================================
% %fasor tensi�n prefalla
% VC=v2(:,3,:);
% [f m p]=lsq(VC(88:120),tout(88:120)');
% Vc=m*exp(j*p);
%         
% %fasor corriente prefalla
% IC=i2(:,3,:);
% [f m p]=lsq(IC(88:120),tout(88:120)');
% Ic=m*exp(j*p);
% 
% Vp2=[Va Vb Vc];
% Ip2=[Ia Ib Ic];

%�������������������������������������������������������������������

% %NODO 03
% 
% %fasor tensi�n prefalla
% VA=v3(:,1,:);
% [f m p]=lsq(VA(88:120),tout(88:120)');
% Va=m*exp(j*p);
% 
% %fasor corriente prefalla
% IA=i3(:,1,:);
% [f m p]=lsq(IA(88:120),tout(88:120)');
% Ia=m*exp(j*p);
% 
% %===============================================================
% %fasor tensi�n prefalla
% VB=v3(:,2,:);
% [f m p]=lsq(VB(88:120),tout(88:120)');
% Vb=m*exp(j*p);
%         
% %fasor corriente prefalla
% IB=i3(:,2,:);
% [f m p]=lsq(IB(88:120),tout(88:120)');
% Ib=m*exp(j*p);
% 
% %================================================================
% %fasor tensi�n prefalla
% VC=v3(:,3,:);
% [f m p]=lsq(VC(88:120),tout(88:120)');
% Vc=m*exp(j*p);
%         
% %fasor corriente prefalla
% IC=ip3(:,3,:);
% [f m p]=lsq(IC(88:120),tout(88:120)');
% Ic=m*exp(j*p);
% 
% Vp3=[Va Vb Vc];
% Ip3=[Ia Ib Ic];
% 
% % Vp=(1/sqrt(2))*[Vp1;Vp2;Vp3]'
% % Ip=(1/sqrt(2))*[Ip1;Ip2;Ip3]'
% 
% Vp=[Vp1;Vp2;Vp3]'
% Ip=[Ip1;Ip2;Ip3]'
% 
% %=====================================================================

% %Fasores  para tensi�n durante falla vistas en la subestaci�n
% 
% %fasor tensi�n posfalla
% VA=vpos(:,1,:);
% [f m p]=lsq(VA(88:120),tout(88:120)');
% Va=m*exp(j*p);
% 
% %fasor corriente posfalla
% IA=ipos(:,1,:);
% [f m p]=lsq(IA(88:120),tout(88:120)');
% Ia=m*exp(j*p);
% 
% %===============================================================
% %fasor tensi�n posfalla
% VB=vpos(:,2,:);
% [f m p]=lsq(VB(88:120),tout(88:120)');
% Vb=m*exp(j*p);
%         
% %fasor corriente posfalla
% IB=ipos(:,2,:);
% [f m p]=lsq(IB(88:120),tout(88:120)');
% Ib=m*exp(j*p);
% 
% %================================================================
% %fasor tensi�n posfalla
% VC=vpos(:,3,:);
% [f m p]=lsq(VC(88:120),tout(88:120)');
% Vc=m*exp(j*p);
%         
% %fasor corriente posfalla
% IC=ipos(:,3,:);
% [f m p]=lsq(IC(88:120),tout(88:120)');
% Ic=m*exp(j*p);
% 
% %Vspos=(1/sqrt(2))*[Va Vb Vc];
% %Ispos=(1/sqrt(2))*[Ia Ib Ic];
% 
% Vspos=[Va Vb Vc];
% Ispos=[Ia Ib Ic];
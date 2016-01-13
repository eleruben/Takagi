function [Ispref, Vspref]=fasores_prefalla1(Vsubes,Isubes,tout)

% %Fasores  para tensión durante falla vistas en la subestación
% 
% %fasor tensión posfalla
VA=Vsubes(:,1,:);
[f m p]=lsq(VA(1:32),tout(1:32)');
Va=m*exp(sqrt(-1)*p);
% 
% %fasor corriente posfalla
IA=Isubes(:,1,:);
[f m p]=lsq(IA(1:32),tout(1:32)');
Ia=m*exp(sqrt(-1)*p);
% 
% %===============================================================
% %fasor tensión posfalla
VB=Vsubes(:,2,:);
[f m p]=lsq(VB(1:32),tout(1:32)');
Vb=m*exp(sqrt(-1)*p);
%         
% %fasor corriente posfalla
IB=Isubes(:,2,:);
[f m p]=lsq(IB(1:32),tout(1:32)');
Ib=m*exp(sqrt(-1)*p);
% 
% %================================================================
% %fasor tensión posfalla
VC=Vsubes(:,3,:);
[f m p]=lsq(VC(1:32),tout(1:32)');
Vc=m*exp(sqrt(-1)*p);
%         
% %fasor corriente posfalla
IC=Isubes(:,3,:);
[f m p]=lsq(IC(1:32),tout(1:32)');
Ic=m*exp(sqrt(-1)*p);

Vspref=[Va Vb Vc];
Ispref=[Ia Ib Ic];



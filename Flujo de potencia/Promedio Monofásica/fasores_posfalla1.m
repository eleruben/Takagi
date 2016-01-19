function [Isfalla, Vsfalla]=fasores_posfalla1(Vsubes,Isubes,tout)

% %Fasores  para tensión durante falla vistas en la subestación
% 
% %fasor tensión posfalla
VA=Vsubes(:,1,:);
[f m p]=lsq(VA(145:177),tout(145:177)');
Va=m*exp(sqrt(-1)*p);
% 
% %fasor corriente posfalla
IA=Isubes(:,1,:);
[f m p]=lsq(IA(145:177),tout(145:177)');
Ia=m*exp(sqrt(-1)*p);
% 
% %===============================================================
% %fasor tensión posfalla
VB=Vsubes(:,2,:);
[f m p]=lsq(VB(145:177),tout(145:177)');
Vb=m*exp(sqrt(-1)*p);
%         
% %fasor corriente posfalla
IB=Isubes(:,2,:);
[f m p]=lsq(IB(145:177),tout(145:177)');
Ib=m*exp(sqrt(-1)*p);
% 
% %================================================================
% %fasor tensión posfalla
VC=Vsubes(:,3,:);
[f m p]=lsq(VC(145:177),tout(145:177)');
Vc=m*exp(sqrt(-1)*p);
%         
% %fasor corriente posfalla
IC=Isubes(:,3,:);
[f m p]=lsq(IC(145:177),tout(145:177)');
Ic=m*exp(sqrt(-1)*p);

Vsfalla=[Va Vb Vc];
Isfalla=[Ia Ib Ic];



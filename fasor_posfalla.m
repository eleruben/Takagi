%Fasores  para tensión durante falla vistas en la subestación

%fasor tensión posfalla
VAp=vpos(:,1,:);
[f m p]=lsq(VAp(88:120),tout(88:120)');
Vap=m*exp(j*p);

%fasor corriente posfalla
IAp=ipos(:,1,:);
[f m p]=lsq(IAp(88:120),tout(88:120)');
Iap=m*exp(j*p);

%===============================================================
%fasor tensión posfalla
VBp=vpos(:,2,:);
[f m p]=lsq(VBp(88:120),tout(88:120)');
Vbp=m*exp(j*p);
        
%fasor corriente posfalla
IBp=ipos(:,2,:);
[f m p]=lsq(IBp(88:120),tout(88:120)');
Ibp=m*exp(j*p);

%================================================================
%fasor tensión posfalla
VCp=vpos(:,3,:);
[f m p]=lsq(VCp(88:120),tout(88:120)');
Vcp=m*exp(j*p);
        
%fasor corriente posfalla
ICp=ipos(:,3,:);
[f m p]=lsq(ICp(88:120),tout(88:120)');
Icp=m*exp(j*p);

%Vspos=(1/sqrt(2))*[Va Vb Vc];
%Ispos=(1/sqrt(2))*[Ia Ib Ic];

Vspos=[Vap Vbp Vcp];
Ispos=[Iap Ibp Icp];
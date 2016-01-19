% Primera aproximación método de Lubkeman

[MagIpre, AngIpre]=flujo_carga_prefalla1(mx, lx, Sb, Vbas);

[Isfalla, Vsfalla]=fasores_posfalla1(Vsubes,Isubes,tout); % Cálcula los fasores de las tensiones y corrientes vistas en la S/E
                                                         % durante la falla
                                                         
[Ispref, Vspref]=fasores_prefalla1(Vsubes,Isubes,tout);

tout(length(tout))=[];

Subes=[tout Vsubes Isubes];

%xlswrite('simulacion.xlsx',Subes); % Genera un archivo en Excel con los datos de tiempo, tensiones y corrientes vistos en la S/E

% [MagTenPos, AngTenPos, MagIPos, AngIPos]=flujo_carga_falla(Vsfalla,Isfalla, mx, lx, Sb, Vbas);

%tramos_falla=zeros(1,ntramos);
%distancias=zeros(1,ntramos);
%Vn=Vsfalla(2); % Asigna la tensión de falla vista en la S/E al nodo 1 (S/E) para iniciar cálculos

%[MagIpre, AngIpre, Ipre]=flujo_carga_prefalla(mx, lx, Sb, Vbas);

%Isup=Isfalla(2)-Ipre(1,2); %Se debe ajustar de acuerdo con la fase en falla

%Itramo=Ipre(1,2)+Isup;

MagTenPos=abs(Vsfalla(1));
AngTenPos=angle(Vsfalla(1));

MagIPos=abs(Isfalla(1));
AngIPos=angle(Isfalla(1));

MagIpre=abs(Ispref(1));
AngIpre=angle(Ispref(1));

[m]=takagi2(MagIpre, AngIpre, MagTenPos, AngTenPos, MagIPos, AngIPos, Zreal(1), Zimag(1));
m

%Vn=Vn-(Isup+Ipre(1,2))*Z(1);

% for i=2:ntramos    
%     
%     [MagIpre, AngIpre, Ipre]=flujo_carga_prefalla(mx, lx, Sb, Vbas);
% 
%     Isup=Isfalla(2)-Ipre(1,2); %Se debe ajustar de acuerdo con la fase en falla
% 
%     Itramo=Ipre(i-1,2)+Isup;
% 
%     abs(Vn)
%     abs(Isup+Ipre(i-1,2))
%     
%     MagTenPos=abs(Vn);
%     AngTenPos=angle(Vn);
% 
%     MagIPos=abs(Itramo);
%     AngIPos=angle(Itramo);
% 
%     [m]=takagi2(MagIpre(i-1,2), AngIpre(i-1,2), MagTenPos, AngTenPos, MagIPos, AngIPos, Zreal(1), Zimag(1));
%     m
%     i
%         
%     if (m >= 0) && (m <= 1)
%         tramos_falla(end+1)= i;
%         distancias(end+1) = m;
%     end
%     
%     Vn=Vn-(Isup+Ipre(i-1,2))*Z(1);
%                   
% end
% 
% tramos_falla
% distancias
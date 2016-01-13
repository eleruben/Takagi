function [m]=takagi2(MagIpre, AngIpre, MagTenPos, AngTenPos, MagIPos, AngIPos, Zreal, Zimag)


Ipre_f = MagIpre*exp(sqrt(-1)* AngIpre);
Vs = MagTenPos*exp(sqrt(-1)*AngTenPos);
Ipos = MagIPos*exp(sqrt(-1)* AngIPos);

Is_d = Ipos-Ipre_f;

z = Zreal+2*pi*60*Zimag*sqrt(-1);

m = imag(Vs * conj(Is_d)) / imag(z*Ipos*conj(Is_d));


function [m]=takagi(MagIpre, AngIpre, MagTenPos, AngTenPos, MagIPos, AngIPos, Zreal, Zimag)


Ipre_f = MagIpre*exp(i* AngIpre)
Vs = MagTenPos*exp(i*AngTenPos)
Ipos = MagIPos*exp(i* AngIPos)

Is_d = Ipos-Ipre_f;

z = Zreal+2*pi*60*Zimag*i;

x = imag(Vs * conj(Is_d)) / imag(z*Ipos*conj(Is_d))


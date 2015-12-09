function [m]=takagi(MagIpre, AngIpre, MagTenPos, AngTenPos, MagIpos, AngIpos)


Ipre_f = Iprea*exp(i* tethaprea)
Vs = Vpo*exp(i*tethapov)
Ipos = Ipo*exp(i* tethapo)

Is_d = Ipos-Ipre_f;

z = 0.5531+2*pi*60*2.3356e-3*i;

x = imag(Vs * conj(Is_d)) / imag((z*Ipos)*conj(Is_d))


%Método Takagi

% terminal S se supone que es la ubicación del reconectador que almacena
% los datos de tensión y corriente (32 muestras por ciclo)

% Vs   : tensión en terminal S
% Is   : corriente que pasa por el terminal S
% Is_d : diferencia entre la corriente de pre-falla y de pos-falla

% ==== DATOS NECESARIOS ====

Ipre_f = Iprea*exp(i* tethaprea)
Vs = Vpo*exp(i*tethapov)
Ipos = Ipo*exp(i* tethapo)

Is_d = Ipos-Ipre_f;


Ipos;
%Is=;


z = 0.5531+2*pi*60*2.3356e-3*i;

x = imag(Vs * conj(Is_d)) / imag((z*Ipos)*conj(Is_d))
imag(Vs * conj(Is_d));
imag((z*Ipos)*conj(Is_d));

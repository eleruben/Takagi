SBase=100;% 100 MVA
VBase = 11.4; % 34.5 kV
IBase = SBase*1000/(VBase*sqrt(3))
If3=IBase/(z1);
ang=-101.77*pi/180;
If3med=9207*(cos(ang)+sin(ang)*j)
abs(If3)
angle(If3)*180/pi
abs(If3med)
z1= 0.10666+0.56044i;
z2=0.10719+0.56081i;
z0=0.01065+0.14498i;
If=3*IBase/(z1+z2+z0)
abs(If)
Z1e=IBase/(If3med)
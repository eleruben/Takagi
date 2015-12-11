function[z]=impedancia(R1,R0,L1,L0,d)
Rs=(2*R1+R0)/3;
Ls=(2*L1+L0)/3;
zl=Rs+i*Ls;
z=zl*d;
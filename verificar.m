function [sirve, iniPre, iniFalla] = verificar(senal, tiempo)
Magn=[];
etapa=1;
pre=0;
iniPre=0;
iniFalla=0;
for j=1:(length(senal)-31)
    [Fasor, Mag, Ang]=lsq(senal(j:j+31,1,1),tiempo(j:j+31,1));
    Magn(end+1)=Mag;
end
for j=1:(length(Magn)-3)
    if etapa==1;
       dif=abs(Magn(j+3)-Magn(j));
       if dif < 2
            pre = pre + 1;
            if iniPre == 0
                iniPre = j+10;
            end
            if pre == 20
                etapa=2;
                pre=0;
            end
       else
            pre=0;
            iniPre=0;
       end
    elseif etapa==2;
            dif=abs(Magn(j+3)-Magn(j));
            if dif < 2
                pre = 0;    
            else
                pre=pre+1;
                if pre == 20
                    etapa=3;
                    pre=0;
                end
            end        
    elseif etapa == 3;
            dif=abs(Magn(j+3)-Magn(j));
            if dif < 2
                pre = pre + 1;
                    if iniFalla == 0
                        iniFalla = j+10;
                    end
                    if pre == 20
                        etapa=4;
                        pre=0;
                    end
            else
                pre=0;
                iniFalla=0;
        end
    end
end
       
if etapa == 4;
    sirve=1;
else
    sirve=0;
end
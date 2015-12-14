pre=0;
inestable=0;
Magn=[];
diff=[];
h='';
punto=0;
for j=1:276 
[Fasor, Mag, Ang]=lsq(I(j:j+31,1,1),tout(j:j+31,1));
Magn(end+1)=Mag;
end
for j=1:275
    diff(end+1)=abs(Magn(j+1)-Magn(j));
end
for j=1:(length(Magn)-3)
    dif=abs(Magn(j+3)-Magn(j));
    if dif < 1
       pre = pre + 1;
       if punto == 0
           punto = j+10;
       end
       if pre == 20
           h='sirve';
           break
       end
    else
        punto=0;
        inestable=inestable+1;
        if inestable == 20
            h = 'No sirve';
            break;
        end
    end
end


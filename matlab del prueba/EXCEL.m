muestra=[1:308]';
%archivo={'Muestra', 'Hora', 'Vc', 'Vb', 'Va', 'Min', 'Seg', 'Seg', 'Ic', 'Ib', 'Ia', 'In';
%tout(1:308), muestra, muestra, V(:,3), V(:,2), V(:,1), muestra, muestra, muestra, I(:,1), I(:,2), I(:,3), I(:,1)};
%archivo=[tout(1:308), muestra, muestra, V(3)];
archivo=table(tout(1:308).*1000, muestra, muestra, V(:,3), V(:,2), V(:,1), muestra, muestra, muestra, I(:,3), I(:,2), I(:,1), I(:,1));
filename='MonofasicaFaseA-Tramo3-AltaImpedancia.xls';
writetable(archivo, filename);
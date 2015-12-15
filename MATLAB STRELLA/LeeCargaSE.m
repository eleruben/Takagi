[PSE QSE]=textread('CurvaCargaUS16.txt','%u %u');
SSE = PSE+j*QSE;
magSSE = abs(SSE)
plot(magSSE);
cosphi = cos(angle(SSE));
plot(cosphi);
save('Carga.mat','SSE');
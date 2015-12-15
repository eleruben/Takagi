%%%%%%%Variables

%% Rcon : Resistencia Conductor [ ohm /km]
%% rmg : Radio Medio Geometrico [mm]
%% T : Temperatura de operación [ºC]
%% CoorCond : Matriz de Coordenadas de Conductores
%% dab : Separación a - b [m]
%% dac : Separación a - c [m]
%% dcb : Separación c - b [m]
%% dgk : Distancia equivalente del conductor de tierra
%% D : Distancia entre conductores
%% Rg : Resistividad del terreno [ohm-m]

%% A : Matriz de transformación de componentes simetricas

%% Zabc : Matriz de Impedancia
%% Zabc2 : Reducción de la matriz al incluir el efecto de la tierra
%% Z012 : Matriz a componentes simetricas

function [Z012, Zabc3] = ImpedanciaLinea(Rcon, rmg, CoorCond)
Rcon = Rcon/1000;
rmg = rmg/1000;
T = 75;
%dab = 1.3;
%dac = 1.9;
%dcb = 0.6;
Rg =100;

dgk = sqrt(656.6*sqrt(Rg/60));

D = Distancia(rmg, CoorCond);
Dim = size(CoorCond);
Tam = Dim(1,2);
%D = [rmg dab dac; dab rmg dcb; dac dcb rmg];

%%Impedancia Original del Sistema
Zabc = zeros(Tam+1);
for I = 1:Tam
   for J = 1:Tam
      if I == J
         Zabc(I,J) = Rcon + i*2*pi*60*2e-7*log(1/D(I,J));
      else
         Zabc(I,J) = i*2*pi*60*2e-7*log(1/D(I,J));      
      end
   end
   Zabc(I,Tam+1) = i*2*pi*60*2e-7*log(1/dgk);
   Zabc(Tam+1,I) = Zabc(I,Tam+1);
   Zabc(Tam+1,Tam+1) = 9.869e-7*60;
end
Zabc = Zabc*1000;

%% Reducción del efecto de retorno por tierra
Zabc2 = zeros(Tam);
for I = 1:Tam
   for J = 1:Tam
		Zabc2(I,J) = Zabc(I,J)+Zabc(Tam+1,Tam+1)-Zabc(I,Tam+1)-Zabc(Tam+1,J);      
   end
end

%% Reducción de Kron
Zabc3 = zeros(3);
Dim2 = size(Zabc2);
Tam2 = Dim2(1,1);
if Tam2 == 3
   Zabc3 = Zabc2;
else
   for K = 1:(Tam2-3)
		for I = 1:3
   		for J = 1:3
            Zabc3(I,J) = Zabc2(I,J)+Zabc2(I,3+K)*Zabc2(3+K,J)/Zabc2(3+K,3+K);
         end
		end
   end
end


%% Matriz en comonentes simetricas
a = exp(j*2*pi/3);
A = [ 1 1 1; 1 a^2 a; 1 a a^2];
Z012 = inv(A)*Zabc3*A;




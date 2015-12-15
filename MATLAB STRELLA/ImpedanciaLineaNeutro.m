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

function Z012 = ImpedanciaLineaNeutro(Rcon, rmg, CoorCond)
Rcon = Rcon/1000;
rmg = rmg/1000;
T = 75;
%dab = 1.3;
%dac = 1.9;
%dcb = 0.6;
Rg =100;

dgk = sqrt(656.6*sqrt(Rg/60));

%D = zeros(3);
D = Distancia(rmg, CoorCond);
%D = [rmg dab dac; dab rmg dcb; dac dcb rmg];

Zabc = zeros(4);
for I = 1:3
   for J = 1:3
      if I == J
         Zabc(I,J) = Rcon + i*2*pi*60*2e-7*log(1/D(I,J));
      else
         Zabc(I,J) = i*2*pi*60*2e-7*log(1/D(I,J));      
      end
   end
   Zabc(I,4) = i*2*pi*60*2e-7*log(1/dgk);
   Zabc(4,I) = Zabc(I,4);
   Zabc(4,4) = 9.869e-7*60;
end
Zabc = Zabc*1000;

Zabc2 = zeros(3);
for I = 1:3
   for J = 1:3
		Zabc2(I,J) = Zabc(I,J)+Zabc(4,4)-Zabc(I,4)-Zabc(4,J);      
   end
end

a = exp(j*2*pi/3);
A = [ 1 1 1; 1 a^2 a; 1 a a^2];
Z012 = inv(A)*Zabc2*A;




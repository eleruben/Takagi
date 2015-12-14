% FASORES DE TENSIÓN Y CORRIENTE ANTES Y DURANTE LA FALLA

Vpre=Vpref; % Fasor de tensión prefalla para cada nodo ==> matriz con datos por fase y por nodo tamaño=[3 * # nodos]

Vpos=Vposf; % Fasor de tensión durante la falla para cada nodo==> matriz con datos por fase y por nodo tamaño=[3 * # nodos]
%Ipos=Iposf; % Fasor de corriente durante la falla para cada nodo ==> matriz con datos por fase y por nodo tamaño=[3 * # nodos]

Vpre,Vpos

% ESTIMACIÓN DE LA POTENCIA COMPLEJA PREFALLA

Snom=[250e6 150e6]; % Potencia nominal de los transformadores conectados a cada nodo ==> vector con datos de potencia nom de trafos
Ssum=sum(Snom); % Suma de las potencias nominales de los trafos
Ssum

x=P(1)+j*Q(1); % Potencia compleja trifásica prefalla medida en la subestación

Sspre=[x/3 x/3 x/3]'; % Potencia compleja prefalla medida para la subestación ==> vector con datos por fase

Snom_s=[Snom(1)/Ssum Snom(2)/Ssum]; 

Spre=Sspre*Snom_s;  % potencia comleja prefalla ==> Matiz que contiene datos de potencia de cada fase y en cada nodo 
Spre

% FLUJO DE POTENCIA DURANTE LA FALLA

n=[0 1 2]; % Exponente carga vs modelo de carga. 0 => Potencia Constante
                                               % 1 => Corriente Constante
                                               % 2 => Impedancia Constante
for i=1:length(Spre)
    Spos=Spre*(abs(Vpos(i)/Vpre(i)))^n(1);
end

Spos

% OJO colocar bien los datos de matrices para que las operaciones no tengan
% problemas por dimensiones


for i=1:length(Spre)
    for k=1:length()
        Iload=(conj(Spre(i))) * (((abs(Vpos(i)))^(n(1)-2))/((abs(Vpre(i)))^n(1)))*Vpos(i); % Fasor de corrente de carga para cada nodo durante la falla
    end
end

Iload

% ESTIMACIÓN DE LA CORRIENTE DE FALLA

Isub=Isu; % Fasor de corriente de la subestación durante la falla
Isum=sum(Iload);
If=Isub-Isum;
If

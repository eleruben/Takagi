CoordenadasEstructuras;
Conductores;

%Cu 2
[Z_Cu_2_012 Z_Cu_2_abc] = ImpedanciaLinea(CuD(2,4), CuD(2,10), LA111);

%Cu 1
[Z_Cu_1_012 Z_Cu_1_abc] = ImpedanciaLinea(CuD(3,4), CuD(3,10), LA111);

%Cu 2/0
[Z_Cu_2_0_012 Z_Cu_2_0_abc] = ImpedanciaLinea(CuD(5,4), CuD(5,10), LA111);

%Cu 4/0
[Z_Cu_4_0_012 Z_Cu_4_0_abc] = ImpedanciaLinea(CuD(7,4), CuD(7,10), LA111);

%Al 2
[Z_Al_2_012 Z_Al_2_abc] = ImpedanciaLinea(Al(2,4), Al(2,7), LA111);

%Al 1
[Z_Al_1_012 Z_Al_1_abc] = ImpedanciaLinea(Al(3,4), Al(3,7), LA111);

%Al 2/0
[Z_Al_2_0_012 Z_Al_2_0_abc] = ImpedanciaLinea(Al(5,4), Al(5,7), LA111);

%Al 4/0
[Z_Al_4_0_012 Z_Al_4_0_abc] = ImpedanciaLinea(Al(7,4), Al(7,7), LA111);

%ACSR 2
[Z_ACSR_2_012 Z_ACSR_2_abc] = ImpedanciaLinea(ACSR(2,5), ACSR(2,8), LA111);

%ACSR 1
[Z_ACSR_1_012 Z_ACSR_1_abc] = ImpedanciaLinea(ACSR(3,5), ACSR(3,8), LA111);

%ACSR 2/0
[Z_ACSR_2_0_012 Z_ACSR_2_0_abc] = ImpedanciaLinea(ACSR(5,5), ACSR(5,8), LA111);

%ACSR 4/0
[Z_ACSR_4_0_012 Z_ACSR_4_0_abc] = ImpedanciaLinea(ACSR(7,5), ACSR(7,8), LA111);

ImpedanciaLineas.Tipo = {'CU_2', 'CU_1', 'CU_2/0', 'CU_4/0', 'AL_2', 'AL_1', 'Al_2/0', 'Al_4/0', 'ACSR_2', 'ACSR_1', 'ACSR_2/0', 'ACSR_4/0'};

ImpedanciaLineas(1).Z012 = diag(Z_Cu_2_012)' ;
ImpedanciaLineas(1).Zabc = Z_Cu_2_abc;

ImpedanciaLineas(2).Z012 = diag(Z_Cu_1_012)' ;
ImpedanciaLineas(2).Zabc = Z_Cu_1_abc;

ImpedanciaLineas(3).Z012 = diag(Z_Cu_2_0_012)' ;
ImpedanciaLineas(3).Zabc = Z_Cu_2_0_abc;

ImpedanciaLineas(4).Z012 = diag(Z_Cu_4_0_012)' ;
ImpedanciaLineas(4).Zabc = Z_Cu_4_0_abc;

ImpedanciaLineas(5).Z012 = diag(Z_Al_2_012)' ;
ImpedanciaLineas(5).Zabc = Z_Al_2_abc;

ImpedanciaLineas(6).Z012 = diag(Z_Al_1_012)' ;
ImpedanciaLineas(6).Zabc = Z_Al_1_abc;

ImpedanciaLineas(7).Z012 = diag(Z_Al_2_0_012)' ;
ImpedanciaLineas(7).Zabc = Z_Al_2_0_abc;

ImpedanciaLineas(8).Z012 = diag(Z_Al_4_0_012)' ;
ImpedanciaLineas(8).Zabc = Z_Al_4_0_abc;

ImpedanciaLineas(9).Z012 = diag(Z_ACSR_2_012)' ;
ImpedanciaLineas(9).Zabc = Z_ACSR_2_abc;

ImpedanciaLineas(10).Z012 = diag(Z_ACSR_1_012)' ;
ImpedanciaLineas(10).Zabc = Z_ACSR_1_abc;

ImpedanciaLineas(11).Z012 = diag(Z_ACSR_2_0_012)' ;
ImpedanciaLineas(11).Zabc = Z_ACSR_2_0_abc;

ImpedanciaLineas(12).Z012 = diag(Z_ACSR_4_0_012)' ;
ImpedanciaLineas(12).Zabc = Z_ACSR_4_0_abc;

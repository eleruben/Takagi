# -*- coding: utf-8 -*-
import numpy as np
import math as mt
import cmath as cm
import sys

class Nodo(object):
    #constructor
    def __init__(self, ID, ALIAS, TRONCAL):
        self.id=ID;
        self.alias=ALIAS;
        self.tron=TRONCAL;
        self.ten=np.matrix([[1],[1*(np.exp(2.09j))],[1*(np.exp(-2.09j))]]);
        self.tenPost=np.matrix([[1],[1*(np.exp(2.09j))],[1*(np.exp(-2.09j))]])
        self.ant=0;
        self.sig=[];
        self.ver=0;

    def CalculoTension(self, TensionNodoAnterior, CorrienteLineaAnterior, ImpedanciaLineaAnterior, DistanciaLienaAnterior):
        #Calcula la tensi�n del nodo ingresando la tensi�n del nodo anterior, la corriente de la linea
        #anterior que est� conectada al nodo y su impedancia.
        self.V=TensionNodoAnterior-(CorrienteLineaAnterior*ImpedanciaLineaAnterior*DistanciaLienaAnterior)

class Olinea(object):
    #constructor
    def __init__(self, ID, ALIAS, NODO1, NODO2, R0, R1, L0, L1, D):
        self.id=ID;
        self.alias=ALIAS;
        self.nodo1=NODO1;
        self.nodo2=NODO2;
        self.R0=R0;
        self.R1=R1;
        self.L0=L0;
        self.L1=L1;
        self.D=D;
        self.I=np.matrix([[0], [0], [0]]);
        self.IPost=np.matrix([[0], [0], [0]]);
        self.Z=0;
        self.impedancia();
        self.falla=0;
        self.DFalla=0;
        self.ver=0;
        self.Indicador=0;
        self.IdIndicador='NaN';
        self.AliasIndicador='NaN';
        self.EstadoIndicador=0;
        self.DisIndicador=0;
        self.PosibleFalla=0;

    def impedancia(self):
        Rs=(2*self.R1+self.R0)/3;
        Rm=(self.R0-self.R1)/3;
        Ls=(2*self.L1+self.L0)/3;
        Lm=(self.L0-self.L1)/3;
        Xs=Ls;
        Xm=Lm;
        ZAA=complex(Rs,Xs);
        ZAB=complex(Rm,Xm);
        self.Z=np.matrix([[ZAA,ZAB,ZAB],[ZAB, ZAA, ZAB],[ZAB,ZAB,ZAA]]);

    def CalculoCorriente(self, corrientes):
        #Corriente de carga
        for i in corrientes:
            self.I=self.I+i;

class carga(object):
    def __init__(self, ID, NODO, ALIAS, P, Q):
        self.id=ID;
        self.alias=ALIAS;
        self.nodo=NODO;
        self.I=[0, 0, 0];
        self.P=P;
        self.Q=Q;
        #self.potencia()

    def potencia(self):
        phi = np.arccos(self.fp)
        self.P = self.PA * np.cos(phi)
        self.Q = self.PA * np.sin(phi)

    def CalculoCorriente(self, tension):
        #print complex(self.P,self.Q)
        I = np.conjugate((complex(self.P, self.Q)) / (np.sqrt(3)*tension))
        I = I*np.sqrt(2)
        self.I=np.matrix([I, I*np.exp(2.09j), I*np.exp(-2.09j)])

##################################################################################
#                                                                                #
#                                 FUNCIONES                                      #
#                                                                                #
##################################################################################

#Verificar si encontró linea

def VerificarLinea(Linea, Nodo):
    if Linea == 'NaN':
        print('Error: Nodo ' +str(Nodo) + ' desconectado')
        error = 1
    else:
        error = 0
    return error;
'''
def VerificarCarga(Carga):
    if Carga == 'NaN':
        print('Error: Carga ' +str(Carga) + ' desconectada')
        error = 1
    else:
        error =
    return error;
    '''


#Localización monofásica

def DistanciaMonofasica(Linea, Nodo, Fases):
    if Fases == 0:
        x=Linea.IPost[0,0]*Linea.Z[0,0] + Linea.IPost[1,0]*Linea.Z[0,1] + Linea.IPost[2,0]*Linea.Z[0,2]
        If = Linea.IPost[0]-Linea.I[0]
        #Vector funciones fase neutro
        V=np.matrix([[np.real(Nodo.tenPost[0,0])],[np.imag(Nodo.tenPost[0,0])]])
        #Matriz de coeficientes
        F=np.matrix([[np.real(x), np.real(If)], [np.imag(x), np.imag(If)]])
        #Calculo de distancia
        res=np.linalg.inv(F)*V
        D=res[0,0]
        return D
    elif Fases == 1:
        x=Linea.IPost[0,0]*Linea.Z[1,0] + Linea.IPost[1,0]*Linea.Z[1,1] + Linea.IPost[2,0]*Linea.Z[1,2]
        print 'corriente de prefalla'
        print np.abs(Linea.I[1])
        print 'corriente de postfalla'
        print np.abs(Linea.IPost[1])
        If = Linea.IPost[1]-(Linea.I[1])
        print np.abs(If)
        #Vector funciones fase neutro
        V=np.matrix([[np.real(Nodo.tenPost[1,0])],[np.imag(Nodo.tenPost[1,0])]])
        print 'voltajes'
        print np.abs(Nodo.tenPost)
        print np.angle(Nodo.tenPost)
        #Matriz de coeficientes
        F=np.matrix([[np.real(x), np.real(If)], [np.imag(x), np.imag(If)]])
        #Calculo de distancia
        res=np.linalg.inv(F)*V
        D=res[0,0]
        return D
    elif Fases == 2:
        x=Linea.IPost[0,0]*Linea.Z[2,0] + Linea.IPost[2,0]*Linea.Z[1,1] + Linea.IPost[2,0]*Linea.Z[2,2]
        If = Linea.IPost[2]-Linea.I[2]
        #Vector funciones fase neutro
        V=np.matrix([[np.real(Nodo.tenPost[2,0])],[np.imag(Nodo.tenPost[2,0])]])
        #Matriz de coeficientes
        F=np.matrix([[np.real(x), np.real(If)], [np.imag(x), np.imag(If)]])
        #Calculo de distancia
        res=np.linalg.inv(F)*V
        D=res[0,0]
        return D

def DistanciaBifasicaAislada(Linea, Nodo, Fases):
    if Fases == 0:
        If=Linea.IPost[0]-Linea.I[0]
        Z1=Linea.Z[0,1]-Linea.Z[0,1]
        Z2=Linea.Z[0,0]-Linea.Z[0,1]
        Z3=Linea.Z[0,1]-Linea.Z[0,0]
        x=Z2*Linea.IPost[0,0]+Z3*Linea.IPost[1,0]+Z1*Linea.IPost[2,0]
        #Matriz de coeficientes
        Fab=np.matrix([[np.real(x), np.real(If)], [np.imag(x), np.imag(If)]])
        Vab=np.matrix([[np.real(Nodo.tenPost[0,0]-Nodo.tenPost[1,0])], [np.imag(Nodo.tenPost[0,0]-Nodo.tenPost[1,0])]])
        res=np.linalg.inv(Fab)*Vab
        D=res[0,0]
        return D
    if Fases == 1:
        If=Linea.IPost[1]-Linea.I[1]
        Z1=Linea.Z[0,1]-Linea.Z[0,1]
        Z2=Linea.Z[0,0]-Linea.Z[0,1]
        Z3=Linea.Z[0,1]-Linea.Z[0,0]
        x=Z1*Linea.IPost[0,0]+Z2*Linea.IPost[1,0]+Z3*Linea.IPost[2,0]
        #Matriz de coeficientes
        Fab=np.matrix([[np.real(x), np.real(If)], [np.imag(x), np.imag(If)]])
        Vab=np.matrix([[np.real(Nodo.tenPost[1,0]-Nodo.tenPost[2,0])], [np.imag(Nodo.tenPost[1,0]-Nodo.tenPost[2,0])]])
        res=np.linalg.inv(Fab)*Vab
        D=res[0,0]
        return D
    if Fases == 2:
        If=Linea.IPost[0]-Linea.I[0]
        Z1=Linea.Z[0,1]-Linea.Z[0,1]
        Z2=Linea.Z[0,0]-Linea.Z[0,1]
        Z3=Linea.Z[0,1]-Linea.Z[0,0]
        x=Z2*Linea.IPost[0,0]+Z1*Linea.IPost[1,0]+Z3*Linea.IPost[2,0]
        #Matriz de coeficientes
        Fab=np.matrix([[np.real(x), np.real(If)], [np.imag(x), np.imag(If)]])
        Vab=np.matrix([[np.real(Nodo.tenPost[0,0]-Nodo.tenPost[2,0])], [np.imag(Nodo.tenPost[0,0]-Nodo.tenPost[2,0])]])
        res=np.linalg.inv(Fab)*Vab
        D=res[0,0]
        return D

def DistanciaBifasicaTierra(Linea, Nodo, Fases):
    if Fases == 0:
        Ifa=Linea.IPost[0,0]-Linea.I[0,0] # Para fase A
        Ifb=Linea.IPost[1,0]-Linea.I[1,0]

        x0=Linea.Z[0,0]*Linea.IPost[0,0] + Linea.Z[0,1]*Linea.IPost[1,0] + Linea.Z[0,2]*Linea.IPost[2,0]
        x1=Linea.Z[1,0]*Linea.IPost[0,0] + Linea.Z[1,1]*Linea.IPost[1,0] + Linea.Z[1,2]*Linea.IPost[2,0]

        # Matriz de coeficientes
        Vab=np.matrix([[np.real(Nodo.tenPost[0,0])], [np.imag(Nodo.tenPost[0,0])], [np.real(Nodo.tenPost[1,0])], [np.imag(Nodo.tenPost[1,0])]])

        #Matriz inversa
        Fab=np.linalg.inv(np.matrix([[np.real(x0), np.real(Ifa), 0, np.real(Ifa+Ifb)], [np.imag(x0), np.imag(Ifa), 0, np.imag(Ifa+Ifb)], [np.real(x1), 0, np.real(Ifb), np.real(Ifa+Ifb)], [np.imag(x1), 0, np.imag(Ifb), np.imag(Ifa+Ifb)]]))
        #Calculo de Distancia D
        Res= Fab * Vab
        D=Res[0,0]
        return D
    if Fases == 1:
        Ifb=Linea.IPost[1,0]-Linea.I[1,0] # Para fase A
        Ifc=Linea.IPost[2,0]-Linea.I[2,0]

        x0=Linea.Z[1,0]*Linea.IPost[0,0] + Linea.Z[1,1]*Linea.IPost[1,0] + Linea.Z[1,2]*Linea.IPost[2,0]
        x1=Linea.Z[2,0]*Linea.IPost[0,0] + Linea.Z[2,1]*Linea.IPost[1,0] + Linea.Z[2,2]*Linea.IPost[2,0]

        # Matriz de coeficientes
        Vbc=np.matrix([[np.real(Nodo.tenPost[1,0])], [np.imag(Nodo.tenPost[1,0])], [np.real(Nodo.tenPost[2,0])], [np.imag(Nodo.tenPost[2,0])]])

        #Matriz inversa
        Fbc=np.linalg.inv(np.matrix([[np.real(x0), np.real(Ifb), 0, np.real(Ifb+Ifc)], [np.imag(x0), np.imag(Ifb), 0, np.imag(Ifb+Ifc)], [np.real(x1), 0, np.real(Ifc), np.real(Ifb+Ifc)], [np.imag(x1), 0, np.imag(Ifc), np.imag(Ifb+Ifc)]]))
        #Calculo de Distancia D
        Res= Fbc * Vbc
        D=Res[0,0]
        return D
    if Fases == 2:
        Ifa=Linea.IPost[0,0]-Linea.I[0,0] # Para fase A
        Ifc=Linea.IPost[2,0]-Linea.I[2,0]

        x0=Linea.Z[0,0]*Linea.IPost[0,0] + Linea.Z[0,1]*Linea.IPost[1,0] + Linea.Z[0,2]*Linea.IPost[2,0]
        x1=Linea.Z[2,0]*Linea.IPost[0,0] + Linea.Z[2,1]*Linea.IPost[1,0] + Linea.Z[2,2]*Linea.IPost[2,0]

        # Matriz de coeficientes
        Vac=np.matrix([[np.real(Nodo.tenPost[0,0])], [np.imag(Nodo.tenPost[0,0])], [np.real(Nodo.tenPost[2,0])], [np.imag(Nodo.tenPost[2,0])]])

        #Matriz inversa
        Fac=np.linalg.inv(np.matrix([[np.real(x0), np.real(Ifa), 0, np.real(Ifa+Ifc)], [np.imag(x0), np.imag(Ifa), 0, np.imag(Ifa+Ifc)], [np.real(x1), 0, np.real(Ifc), np.real(Ifa+Ifc)], [np.imag(x1), 0, np.imag(Ifc), np.imag(Ifa+Ifc)]]))
        #Calculo de Distancia D
        Res= Fac * Vac
        D=Res[0,0]
        return D


def TipoDeFalla(Linea, Nodo, TipoDeFalla, Fases):
    #Recibe los datos de la falla y decide cual ecuación usar
    if TipoDeFalla == 0:
        #Falla monofasica
        #Para falla monofásica, falla fase A, Fases = 0
        #Falla fase B, Fases=1
        #Falla fase C, Fases = 2
        D=DistanciaMonofasica(Linea, Nodo, Fases)
    elif TipoDeFalla == 1:
        #Falla Bifasica aislada
        #Falla A-B, Fases = 0
        #Falla B-C, Fases = 1
        #Falla C-A, Fases = 2
        D=DistanciaBifasicaAislada(Linea, Nodo, Fases)
    elif TipoDeFalla == 2:
        #Falla Bifasica Tierra
        #Falla A-B, Fases = 0
        #Falla B-C, Fases = 1
        #Falla C-A, Fases = 2
        D=DistanciaBifasicaTierra(Linea, Nodo, Fases)
    elif TipoDeFalla == 3:
        #Falla trifasica aislada
        D=DistanciaTrifasicaAislada(Linea, Nodo, Fases)
    elif TipoDeFalla == 4:
        #Falla trifasica aislada
        D=DistanciaTrifasicaTierra(Linea, Nodo, Fases)
    return D


#Buscar linea conociendo sus dos nodos
def BuscarLinea(nodo1, nodo2, Lineas):
    for i in range(len(Lineas)):
        if Lineas[i].nodo1 == nodo1 and Lineas[i].nodo2 == nodo2:
            LineaActual=i
            break
    return LineaActual

#Verificar los nodos que están adelante del nodo actual
def VerificarNodos(nodoActual, Nodos):
    terminar = 0
    actual = nodoActual
    NodosSiguientesVerificados=0
    while terminar == 0:
        if len(Nodos[actual].sig) == 0:
            Nodos[actual].ver=1
            actual = nodoActual
        else:
            for i in range(len(Nodos[actual].sig)):
                if Nodos[Nodos[actual].sig[i]-1].ver == 0:
                    actual = Nodos[actual].sig[i]-1
                    NodosSiguientesVerificados=0
                    break
                else:
                    NodosSiguientesVerificados = 1
            if NodosSiguientesVerificados == 1:
                Nodos[actual].ver=1
                actual=nodoActual
        for i in range(len(Nodos[nodoActual].sig)):
            if Nodos[Nodos[nodoActual].sig[i]-1].ver == 0:
                terminar = 0
                break
            else:
                terminar = 1
    return Nodos

#tipo 0 monofasico fase 0 A FASE 1 B FASE 2 C
#tipo 1 bifasico aislado fase 0 AB FASE 1 BC FASE 2 AC
#tipo 2 bifasico tierra (todavia no) fase 0 AB FASE 1 BC FASE 2 AC
#tipo 3 trifasico aislado (todavia no)
#tipo 4 trifasico tierra (todavia no)
def Localizacion(Vpre, Ipre,VPost, IPost, TaNodos, TaLineas, TaCargas, Tipo, Fase):

    Va=Vpre[0]
    Vb=Vpre[1]
    Vc=Vpre[2]
    Ia=Ipre[0]
    Ib=Ipre[1]
    Ic=Ipre[2]
    VaPost=VPost[0]
    VbPost=VPost[1]
    VcPost=VPost[2]
    IaPost=IPost[0]
    IbPost=IPost[1]
    IcPost=IPost[2]
    #Calculo de valores base

    Vbase=(abs(Va)+abs(Vb)+abs(Vc))/3.0;
    Ibase=(abs(Ia)+abs(Ib)+abs(Ic))/3.0;
    Sbase=(abs(Va*Ia.conjugate())+abs(Vb*Ib.conjugate())+abs(Vc*Ic.conjugate()))/3.0;
    Zbase=(abs(Va/Ia)+abs(Vb/Ib)+abs(Vc/Ic))/3.0;

    #Conección del circuito
        #Creacion de nodos
    Nodos = []

    for i in range(len(TaNodos) - 1):
        Nodos.append(Nodo(TaNodos[i + 1][0], TaNodos[i + 1][1], TaNodos[i + 1][2]))

    #print(Nodos[0].id)

        #Creacion de lineas
    Lineas=[]

    for i in range(len(TaLineas) - 1):
        Lineas.append(Olinea(TaLineas[i+1][0], TaLineas[i+1][1], TaLineas[i+1][2], TaLineas[i+1][3], TaLineas[i+1][4], TaLineas[i+1][5], TaLineas[i+1][6], TaLineas[i+1][7], TaLineas[i+1][8]))

    #print Lineas[2].nodo1
        #Coneccion de nodos
    for i in range(len(Lineas)):
        Nodos[Lineas[i].nodo2-1].ant = Lineas[i].nodo1
        Nodos[Lineas[i].nodo1-1].sig.append(Lineas[i].nodo2)

        #Creacion de cargas
    Cargas=[]
    for i in range(len(TaCargas) - 1):
        Cargas.append(carga(TaCargas[i+1][0], TaCargas[i+1][1], TaCargas[i+1][2], TaCargas[i+1][3], TaCargas[i+1][4]))

    ##################################################################################
    #                                                                                #
    #                         FLUJO DE CARGA PREFALLA                                #
    #                                                                                #
    ##################################################################################

    #Variable que guardara el nodo principal

    princpal=0
    #Se busca el nodo principal
    for i in range(len(Nodos)):
        if Nodos[i].ant == 0:
            principal=i
            break

    #Calculo de corrientes
    #Calculo de corrientes de cargas

    for t in range(3):
        #inicializar corrientes
        for i in range(len(Lineas)):
            Lineas[i].I=np.matrix([[0], [0], [0]])
        for i in range(len(Cargas)):
            #Vector potencias de carga
            S=np.matrix([[complex(Cargas[i].P, Cargas[i].Q)/Sbase], [complex(Cargas[i].P, Cargas[i].Q)/Sbase], [complex(Cargas[i].P, Cargas[i].Q)/Sbase]])
            #Matriz tensiones
            V1=1/(3*Nodos[Cargas[i].nodo-1].ten[0])
            V2=1/(3*Nodos[Cargas[i].nodo-1].ten[1])
            V3=1/(3*Nodos[Cargas[i].nodo-1].ten[2])
            V=np.matrix([(V1[0,0] ,0 ,0), (0, V2[0,0], 0), (0, 0, V3[0,0])])
            Cargas[i].I=V*S
            Cargas[i].I=Cargas[i].I.conjugate()

        #######################################################################
        #                   Calculo de corrientes                             #
        #######################################################################

        fin = 0
        actual=principal
        siguiente=Nodos[principal].sig[0]-1
        final=Nodos[siguiente].sig[0]-1
        Linea1= 'NaN'
        Linea2='NaN'
        carga1='NaN'
        while fin == 0:
            #Buscar la linea entre el nodo actual y el siguiente
            for i in range(len(Lineas)):
                if Lineas[i].nodo2 == siguiente+1:
                    Linea1=i
                    break
            error=VerificarLinea(Linea1, siguiente + 1)
            if error:
                return;
            #Buscar la linea entre el nodo siguiente y el nodo final
            for i in range(len(Lineas)):
                if Lineas[i].nodo2 == final+1:
                    Linea2=i
                    break
            error=VerificarLinea(Linea2, final + 1)
            if error:
                return;
            #Se verifica que la linea 2 no se haya verificado y que le nodo final tenga mas nodos
            #conectados
            if Lineas[Linea2].ver == 0 and len(Nodos[final].sig) != 0 and Nodos[final].ver == 0 and Nodos[siguiente].ver == 0:
                actual = siguiente
                siguiente = final
                for i in Nodos[siguiente].sig:
                    if Nodos[i-1].ver == 0:
                        final=i - 1
                        break
            #Se verifica que la linea 2 no se haya verificado y que le nodo final no tenga mas nodos
            #conectados (linea conectada a un nodo final)
            elif Lineas[Linea2].ver == 0 and len(Nodos[final].sig) == 0 and  Nodos[final].ver == 0 and Nodos[siguiente].ver == 0:
                #Verifico si el nodo final tiene carga conectada
                I=np.matrix([[0],[0],[0]])
                carga1='NaN'
                for i in range(len(Cargas)):
                    if Cargas[i].nodo == final +1:
                        carga1=i
                        break
                if carga1 != 'NaN':
                    Lineas[Linea2].I=Cargas[carga1].I
                else:
                    Lineas[Linea2].I=I
                Lineas[Linea2].ver=1
                Nodos[final].ver=1
                final1 = final
                final = 'NaN'
                for i in Nodos[siguiente].sig:
                    if Nodos[i-1].ver == 0:
                        final=i-1
                        break
                if final == 'NaN':
                    if Nodos[actual].ant != 0:
                        actual = Nodos[actual].ant-1
                        siguiente = Nodos[siguiente].ant-1
                        final=Nodos[final1].ant-1
                        Nodos[final].ver=1
                    else:
                        Nodos[siguiente].ver=1
                        final = Nodos[siguiente].sig[0]-1
            elif Lineas[Linea2].ver == 0 and len(Nodos[final].sig) != 0 and  Nodos[final].ver == 1 and Nodos[siguiente].ver == 0:
                #Calculo  las corrientes que entran al nodo final
                #Primero verifico si el nodo final tiene conectada una carga
                I=np.matrix([[0],[0],[0]])
                carga1='NaN'
                for i in range(len(Cargas)):
                    if Cargas[i].nodo == final +1:
                        carga1=i
                        break
                if carga1 != 'NaN':
                    I=I+Cargas[carga1].I
                for i in Nodos[final].sig:
                    for l in range(len(Lineas)):
                        if Lineas[l].nodo2 == i:
                            I=I+Lineas[l].I
                Lineas[Linea2].I=I
                Lineas[Linea2].ver=1
                final1=final
                final = 'NaN'
                for i in Nodos[siguiente].sig:
                    if Nodos[i-1].ver == 0:
                        final=i-1
                        break
                if final == 'NaN':
                    if Nodos[actual].ant != 0:
                        actual = Nodos[actual].ant-1
                        siguiente = Nodos[siguiente].ant-1
                        final=Nodos[final1].ant-1
                        Nodos[final1].ver=1
                    else:
                        Nodos[siguiente].ver=1
                        final = Nodos[siguiente].sig[0]-1
            elif Lineas[Linea2].ver == 1 and len(Nodos[final].sig) != 0 and  Nodos[final].ver == 1 and Nodos[siguiente].ver == 1:
                I=np.matrix([[0],[0],[0]])
                carga1='NaN'
                for i in range(len(Cargas)):
                    if Cargas[i].nodo == final +1:
                        carga1=i
                        break
                if carga1 != 'NaN':
                    I=I+Cargas[carga1].I
                for i in Nodos[siguiente].sig:
                    for l in range(len(Lineas)):
                        if Lineas[l].nodo2 == i:
                            I=I+Lineas[l].I
                Lineas[Linea1].I=I
                Lineas[Linea1].ver=1
            terminar = 0
            for i in range(len(Lineas)):
                if Lineas[i].ver == 0:
                    terminar = 0
                    break
                else:
                    terminar = 1
            if terminar == 1 and Lineas[Linea1].ver == 1:
                fin = 1
            elif terminar == 0 and Lineas[Linea1].ver == 1:
                print('error mientras calculaba corriente, prefalla, revise configuracion del circuito')
                return
            elif terminar == 0 and Lineas[Linea1].ver == 0:
                fin = 0
            else:
                print ('error desconocido')
                fin = 1

        for i in range(len(Nodos)):
            Nodos[i].ver=0
        for i in range(len(Lineas)):
            Lineas[i].ver=0
        #Calculo de tensiones
        #Nodos[principal].ten=np.matrix([[1], [1], [1]])
        Nodos[principal].ten=np.matrix([[Va/Vbase], [Vb/Vbase], [Vc/Vbase]])
        Nodos[principal].ver=1

        fin = 0
        actual=Nodos[principal].sig[0]
        n=0;
        #Lineas[0].I=np.matrix([[Ia/Ibase], [Ib/Ibase], [Ic/Ibase]])
        while fin == 0:
            if Nodos[actual-1].ver == 0:
                #Busco la linea que está conectada al nodo actual
                for i in range(len(Lineas)):
                    if Lineas[i].nodo2 == Nodos[actual-1].id:
                        LineaActual=i
                        break
                Nodos[actual-1].ten = Nodos[Nodos[actual-1].ant - 1].ten - (Lineas[LineaActual].D*(1/Zbase)*Lineas[LineaActual].Z*Lineas[LineaActual].I)
                Nodos[actual-1].ver = 1
            else:
                if len(Nodos[actual - 1].sig) > 0:
                    verificado=0
                    for i in Nodos[actual - 1].sig:
                        if Nodos[i - 1].ver == 0:
                            actual = i
                            verificado = 0
                            break
                        verificado = 1
                    if verificado == 1:
                        actual = Nodos[actual - 1].ant
                else:
                    actual = Nodos[actual-1].ant

            for m in range(len(Nodos)):
                if Nodos[m].ver == 0:
                    fin = 0
                    break
                else:
                    fin=1
        for m in range(len(Nodos)):
                Nodos[m].ver = 0

    ##################################################################################
    #                                                                                #
    #                    FIN FLUJO DE CARGA PREFALLA                                 #
    #                                                                                #
    ##################################################################################

    #print Lineas[0].I*Ibase*np.sqrt(2)
    #print np.abs(Lineas[0].I*Ibase*np.sqrt(2))
    #print np.angle(Lineas[0].I*Ibase*np.sqrt(2))
    ##################################################################################
    #                                                                                #
    #                         LOCALIZACIÓN DE FALLA                                  #
    #                                                                                #
    ##################################################################################

    #Agrupo la lineas que esten conectadas a un mismo nodo

    Circuito=[]
    LineaTemp=[]

    for i in range(len(Nodos)):
        for h in range(len(Lineas)):
            if Lineas[h].nodo1 == Nodos[i].id:
                LineaTemp.append(Lineas[h].id)
        Circuito.append([Nodos[i].id, LineaTemp])
        LineaTemp=[]

    #Nodo principal tendrá la misma tensión de la medición de la subestación durante falla
    Nodos[principal].tenPost[0]=VaPost
    Nodos[principal].tenPost[1]=VbPost
    Nodos[principal].tenPost[2]=VcPost

    actual= Nodos[principal].sig[0]-1

    #Busco la linea conectada al nodo principal y el nodo siguiente
    for i in range(len(Lineas)):
        if Lineas[i].nodo1 == Nodos[actual].ant and Lineas[i].nodo2 == Nodos[actual].id:
            LineaActual=i
            break

    #Igualo las corrientes de la linea inicial con las que se midieron en la subestación
    Lineas[LineaActual].IPost=np.matrix([[IaPost],[IbPost],[IcPost]])
    D=TipoDeFalla(Lineas[LineaActual], Nodos[principal], Tipo, Fase)



    #Activamos la casilla de verificación para decir que ya revisamos el nodo principal
    Nodos[principal].ver=1
    Lineas[LineaActual].ver=1


    #Nodo actual se inicializa en el principal
    actual=principal

    terminar = 0
    siguiente= 0

    if D > Lineas[LineaActual].D:
        while terminar == 0:
            LineaActual=[]
            LineaAnterior=[]
            Corriente=0
            LineasFin=0
            if Nodos[actual].ver == 0:
                #Verifico si todas las lineas que estan conectadas al nodo ya estan verificadas
                for i in range(len(Circuito)):
                    if Circuito[i][0] == actual + 1:
                        break
                if len(Circuito[i][1]) > 0:
                    for l in Circuito[i][1]:
                        if Lineas[l-1].ver == 1:
                            LineasFin=1
                        else:
                            LineasFin=0
                            LineaActual=l-1
                            break
                    if LineasFin == 0:
                        ###################################
                        #Calculo de corriente de postfalla#
                        ###################################
                        #Busco las otras lineas que estan conectadas al mismo nodo
                        for n in Circuito[i][1]:
                            if n != LineaActual+1:
                                #Sumo todas las corrientes de carga que no sean de la linea que estoy calculando
                                Corriente=Corriente+Lineas[n-1].I
                        #Busco la linea anterior que esta conectada al nodo actual
                        for o in range(len(Lineas)):
                            if Lineas[o].nodo1 == Nodos[actual].ant and Lineas[o].nodo2 == Nodos[actual].id:
                                LineaAnterior=o
                                break
                        Lineas[LineaActual].IPost=Lineas[LineaAnterior].IPost-Corriente*Ibase
                        ##########################################
                        #Calculo de Tension del nodo de postfalla#
                        ##########################################
                        Nodos[actual].tenPost= Nodos[Nodos[actual].ant - 1].tenPost - (Lineas[LineaAnterior].D*Lineas[LineaAnterior].Z*Lineas[LineaAnterior].IPost)
                        D=TipoDeFalla(Lineas[LineaActual], Nodos[actual], Tipo, Fase)
                        Lineas[LineaActual].ver=1
                        if D < Lineas[LineaActual].D and D > 0:
                            Nodos[Lineas[LineaActual].nodo2-1].ver=1
                            siguiente=Lineas[LineaActual].nodo2-1
                            Lineas[LineaActual].falla=1
                            Lineas[LineaActual].DFalla=D
                            if len(Nodos[siguiente].sig) != 0:
                                Nodos=VerificarNodos(siguiente, Nodos)
                            #actual=principal
                        elif D < 0:
                            Nodos[actual].ver=1
                    else:
                        Nodos[actual].ver=1
                else:
                    actual=Nodos[actual].ant

            else:
                for i in Nodos[actual].sig:
                    if len(Nodos[i-1].sig) == 0:
                        Nodos[i-1].ver=1
                for i in Nodos[actual].sig:
                    if Nodos[i-1].ver == 0 and len(Nodos[i-1].sig) != 0:
                        actual = Nodos[i-1].id-1
                        break
                    elif len(Nodos[i-1].sig) == 0:
                        Nodos[i-1].ver=1

            for m in range(len(Nodos)):
                if Nodos[m].ver == 0:
                    terminar = 0
                    break
                else:
                    terminar=1

    fallas=[]
    fallaN=[]
    for i in range(len(Lineas)):
        if Lineas[i].falla==1:
            fallaN.append(Lineas[i].DFalla)
            fallaN.append(Lineas[i].nodo1)
            fallaN.append(Lineas[i].nodo2)
            fallas.append(fallaN)
            fallaN=[]
            #print 'La falla se encuentra en el tramo ' + str(i+1)
            #print 'a una distancia de ' + str(Lineas[i].DFalla) +'Km del inicio del tramo'
    return fallas

def IndicadoresDeFalla(TaNodos, TaLineas, TaCargas, TaIndicadores, IndicadorActivo):
    #Conección del circuito
    #Creacion de nodos
    Nodos = []
    for i in range(len(TaNodos) - 1):
        Nodos.append(Nodo(TaNodos[i + 1][0], TaNodos[i + 1][1], TaNodos[i + 1][2]))

    #Creacion de lineas
    Lineas=[]
    for i in range(len(TaLineas) - 1):
        Lineas.append(Olinea(TaLineas[i+1][0], TaLineas[i+1][1], TaLineas[i+1][2], TaLineas[i+1][3], TaLineas[i+1][4], TaLineas[i+1][5], TaLineas[i+1][6], TaLineas[i+1][7], TaLineas[i+1][8]))

    #Coneccion de nodos
    for i in range(len(Lineas)):
        Nodos[Lineas[i].nodo2-1].ant = Lineas[i].nodo1
        Nodos[Lineas[i].nodo1-1].sig.append(Lineas[i].nodo2)

    #Creacion de cargas
    Cargas=[]
    for i in range(len(TaCargas) - 1):
        Cargas.append(carga(TaCargas[i+1][0], TaCargas[i+1][1], TaCargas[i+1][2], TaCargas[i+1][3], TaCargas[i+1][4]))

    #Creación de los indicadores
    for i in range(len(TaIndicadores)):
        for l in range(len(Lineas)):
            if Lineas[l].nodo1 == TaIndicadores[i][2] and Lineas[l].nodo2 == TaIndicadores[i][3]:
                Lineas[l].Indicador = 1
                Lineas[l].IdIndicador = TaIndicadores[i][0]
                Lineas[l].DisIndicador = TaIndicadores[i][4]
                Lineas[l].AliasIndicador = TaIndicadores[i][1]
    #Tramos posibles
    #Busco la linea que tiene los indicadores activos
    LineaActiva='NaN'
    for i in range(len(Lineas)):
        if Lineas[i].IdIndicador == IndicadorActivo:
            LineaActiva = i
    if LineaActiva == 'NaN':
        print('Error = No existe indicador ' + str(IndicadorActivo))
        return
    NodoInicial=Lineas[LineaActiva].nodo1-1
    NodoFinal=Lineas[LineaActiva].nodo2-1
    Nodos[NodoInicial].ver=1
    Lineas[LineaActiva].PosibleFalla=1
    #Busco las lineas que siguen despues de la línea activa para encontrar un indicador desactivo
    fin=0
    NodoTempIni="NaN"
    NodoTempFin="NaN"
    NodoTempIni=NodoFinal
    LineaTemp = "NaN"
    while fin == 0:
        if len(Nodos[NodoTempIni].sig) != 0:
            for i in Nodos[NodoTempIni].sig:
                if Nodos[i-1].ver == 0:
                    NodoTempFin = i-1
                for i in range(len(Lineas)):
                    if Lineas[i].nodo1 == NodoTempIni+1 and Lineas[i].nodo2 == NodoTempFin+1:
                        LineaTemp = i
                if Lineas[LineaTemp].Indicador == 1:
                    Lineas[LineaTemp].PosibleFalla = 1
                    Nodos[NodoTempFin].ver=1
                    Lineas[LineaTemp].ver=1
                elif Lineas[LineaTemp].Indicador == 0 and Lineas[LineaTemp].ver == 0:
                    Lineas[LineaTemp].ver=1
                    Lineas[LineaTemp].PosibleFalla = 1
                    NodoTempIni = NodoTempFin
                    break
                elif Lineas[LineaTemp].Indicador == 0 and Lineas[LineaTemp].ver == 1:
                    Nodos[NodoTempFin].ver=1
            termina = "NaN"
            for i in Nodos[NodoTempIni].sig:
                if  Nodos[i-1].ver == 0:
                    termina = "NaN"
                    break
                else:
                    termina = 1
            if termina == 1:
                NodoTempIni = Nodos[NodoTempIni].ant -1
            if NodoTempIni == NodoInicial:
                fin = 1
        else:
            fin = 1
    TramosFallaIndicadores=[]
    temp=[]
    for i in range(len(Lineas)):
        if Lineas[i].PosibleFalla == 1 and Lineas[i].Indicador == 1:
            if Lineas[i].nodo1 == NodoInicial+1 and Lineas[i].nodo2 == NodoFinal+1:
                temp.append(Lineas[i].nodo1)
                temp.append(Lineas[i].nodo2)
                temp.append(Lineas[i].DisIndicador)
                temp.append(Lineas[i].D)
                TramosFallaIndicadores.append(temp)
                temp=[]
            else:
                temp.append(Lineas[i].nodo1)
                temp.append(Lineas[i].nodo2)
                temp.append(0)
                temp.append(Lineas[i].DisIndicador)
                TramosFallaIndicadores.append(temp)
                temp=[]

        elif Lineas[i].PosibleFalla == 1 and Lineas[i].Indicador == 0 :
            temp.append(Lineas[i].nodo1)
            temp.append(Lineas[i].nodo2)
            temp.append(0)
            temp.append(Lineas[i].D)
            TramosFallaIndicadores.append(temp)
            temp=[]
    return TramosFallaIndicadores

#Función para filtrar la información de los indicadores y el algoritmo
def ComparacionIndicadoresAlgoritmo(fallas, TramosFallaIndicadores):

    for i in range(len(fallas)):
        ResultadoFinal = []
        for m in range(len(TramosFallaIndicadores)):
            if fallas[i][1] == TramosFallaIndicadores[m][0] and fallas[i][2] == TramosFallaIndicadores[m][1]:
                if fallas[i][0] >= TramosFallaIndicadores[m][2] and fallas[i][0] <= TramosFallaIndicadores[m][3]:
                    ResultadoFinal.append(fallas[i])
        if len(ResultadoFinal) == 0:
            print('Error: La información de los indicadores no coincide con el algoritmo')
            return
        else:
            return ResultadoFinal




#Parametros de las lineas:
R0 = 0.3864
R1 = 0.01273
L0 = 4.1264 * (10 ** -3)*2*np.pi*60
L1 = 0.9337 * (10 ** -3)*2*np.pi*60


#Mediciones subestación:
#Voltajes
Va = ( 1.1578e+04 - 4.7880e+02j)/np.sqrt(2)
Vb = ( -6.2035e+03 - 9.7872e+03j)/np.sqrt(2)
Vc = (-5.3742e+03 + 1.0266e+04j)/np.sqrt(2)
Vpre=[Va, Vb, Vc]
#Corrientes:
Ia = (3.6308 - 0.2224j)/np.sqrt(2)
Ib = (-2.0080 - 3.0332j)/np.sqrt(2)
Ic = (-1.6228 + 3.2556j)/np.sqrt(2)
Ipre=[Ia, Ib, Ic]

#Mediciones post falla
VaPost = (3.5184e+03 - 2.2067e+02j)/np.sqrt(2)
VbPost = (-6.2138e+03 - 9.7490e+03j)/np.sqrt(2)
VcPost = (-5.3818e+03 + 1.0303e+04j)/np.sqrt(2)
VPost=[VaPost, VbPost, VcPost]

IaPost= ( 10.1433 -59.7008j)/np.sqrt(2)
IbPost= (-2.2671 - 2.9620j)/np.sqrt(2)
IcPost= (-1.8801 + 3.3466j)/np.sqrt(2)
IPost=[IaPost, IbPost, IcPost]

#Tablas de configuración

TaNodos = [["ID", "Nombre", "Troncal"],
       [1, "B1", 1],
       [2, "B2", 1],
       [3, "B3", 1],
       [4, "B4", 1],
       [5, "B5", 0],
       [6, "B6", 0],
       [7, "B7", 1]]
#print len(TaNodos)

TaLineas = [["ID", "Nombre", "Nodo1", "Nodo2", "R0", "R1", "L0", "L1", "Distancia"],
          [1, "Linea1", 1, 2, R0, R1, L0, L1, 30],
          [2, "Linea2", 2, 3, 2*R0, R1, 2*L0, L1, 15],
          [3, "Linea3", 3, 4, 2*R0, 2*R1, 2*L0, 2*L1, 10],
          [4, "Linea4", 2, 5, R0, 2*R1, L0, 2*L1, 40],
          [5, "Linea5", 3, 6, 2*R0, R1, L0, 2*L1, 20],
          [6, "Linea6", 4, 7, R0, 2*R1, 2*L0, L1, 19]]

TaCargas = [["ID", "Nodo", "Nombre", "P", "Q"],
          [1, 2, "C2", 8*10**3, 100],
          [2, 3, "C3", 1.5*8*10**3, 2*100],
          [3, 4, "C4", 8*10**3, 2*100],
          [4, 5, "C5", 8*10**3, 1.5*100],
          [5, 6, "C6", 1.5*8*10**3, 100],
          [6, 7, "C7", 2*8*10**3, 2*100]]

TaIndicadores=[["ID", "Nombre", "Nodo1", "Nodo2", "Distancia"],
                [1, 'I1', 2, 3, 1],
                [2, 'I2', 2, 5, 2],
                [3, 'I3', 3, 6, 3],
                [4, 'I4', 4, 7, 2]]


fallas = Localizacion(Vpre, Ipre,VPost, IPost, TaNodos, TaLineas, TaCargas, 0, 0)
print(fallas)
TramosFallaIndicadores = IndicadoresDeFalla(TaNodos, TaLineas, TaCargas, TaIndicadores, 2)
print(TramosFallaIndicadores)
ResultadoFinal = ComparacionIndicadoresAlgoritmo(fallas, TramosFallaIndicadores)
print(ResultadoFinal)







##########################################################################
# ejemplo 2
##########################################################################
'''
TaNodos = [["ID", "Nombre", "Troncal"],
       [1, "B1", 1],
       [2, "B2", 1],
       [3, "B3", 1],
       [4, "B4", 1],
       [5, "B5", 0],
       [6, "B6", 0],
       [7, "B7", 1]]
#print len(TaNodos)

TaLineas = [["ID", "Nombre", "Nodo1", "Nodo2", "R0", "R1", "L0", "L1", "Distancia"],
          [1, "Linea1", 1, 2, R0, R1, L0, L1, 30],
          [2, "Linea2", 2, 3, R0, R1, L0, L1, 15],
          [3, "Linea3", 3, 4, R0, R1, L0, L1, 10],
          [4, "Linea4", 2, 5, R0, R1, L0, L1, 8],
          [5, "Linea5", 3, 6, R0, R1, L0, L1, 20],
          [6, "Linea6", 4, 7, R0, R1, L0, L1, 19]]

TaCargas = [["ID", "Nodo", "Nombre", "P", "Q"],
          [1, 2, "C2", 8*10**3, 100],
          [2, 3, "C3", 8*10**3, 100],
          [3, 4, "C4", 8*10**3, 100],
          [4, 5, "C5", 8*10**3, 100],
          [5, 6, "C6", 8*10**3, 100],
          [6, 7, "C7", 8*10**3, 100]]


TaCargas=[]


TaCargas = [["ID", "Nodo", "Nombre", "P", "Q"],
          [1, 2, "C2", 8*10**3, 100],
          [2, 3, "C3", 8*10**3, 100],
          [3, 4, "C4", 8*10**3, 100]]

'''
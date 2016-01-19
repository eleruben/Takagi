import math
import numpy as np
import matplotlib.pyplot as pl
import cmath

"""
#Variable t que guarda los valores de tiempo de una onda sinusoidal de 60Hz

t=np.arange(0,1.0/60,1.0/(60*32))

#Velocidad angular para la frecuencia fundamental de 60Hz

w=2*math.pi*(60);

#Senal de entrada

#v=500*np.exp(-t/(0.01))+300*np.sin(w*t)+5*np.cos(3*w*t)+3*np.cos(5*w*t);
v = 800 * np.exp(-t / (0.5)) + 300 * np.sin(w * t) + 60 * np.sin(3 * w * t) + 300 * np.cos(5 * w * t)

#Cantidad de muestras
m=len(t);
"""

def Lsq5(t, v):

    #Frecuencia fundamental
    w=2*math.pi*(60);
    m=len(t)

    # ===== MATRIZ DE COEFICIENTES CONOCIDOS =====
    #La matriz esta compuesta por 7 columnas, la columna A solo tiene valores de unos
    #la columna B tiene los valores de la funcion sin(wt)
    #la columna c tiene los valores de la funcion cos(wt)
    #la columan D tiene los valores de la funcion sin(3wt)
    #la columan E tiene los valores de la funcion cos(3wt)
    #la columna F tiene los valores de la variable de tiempo t
    #y la columna G tiene los valores de la variable de tiempo t^2
    #No encontramos la forma de concatenar columnas, por lo tanto creamos la matriz
    #con filas y luego transponemos la matriz

    A=np.ones((1,m));  #a1
    B=t;                    #a2
    C=np.cos(w*t);          #a3
    D=np.cos(2*w*t);        #a4
    E=np.cos(3*w*t);        #a5
    F=np.cos(4*w*t);        #a6
    G=np.cos(5*w*t);        #a7
    H=np.sin(w*t);          #a8
    I=np.sin(2*w*t);        #a9
    J=np.sin(3*w*t);        #a10
    K=np.sin(4*w*t);        #a11
    L=np.sin(5*w*t);        #a12


    M=np.vstack((A,B,C,D,E,F,G,H,I,J,K,L));

    M=M.T; #Transponemos la matriz

    #Hallamos la matriz pseudo-inversa de M

    M_p=np.linalg.pinv(M);

    #Multiplicamos matricialmente la matriz pseudo-inversa y el vector de muestras v

    k=np.dot(M_p,v);

    #Calculamos la magnitud del fasor de la componente fundamental y su fase


    Fasor=complex(k[7],k[2])
    [Mag, Fase]=cmath.polar(Fasor)

    #print (Fasor, Mag, Fase)
    return (Fasor, Mag, Fase)

    #mag=math.sqrt(k[2]**2+k[7]**2);     #magnitud
    #theta=math.acos(k[7]/mag);          #Fase


    #print (mag)
    #print (theta)


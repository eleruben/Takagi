"""
An example of how to interact with the plotting canvas by connecting
to move and click events
"""
from __future__ import print_function
import sys
import matplotlib.pyplot as plt
import numpy as np

import claseComtrade as cm

iniFalla=0
iniPre=0
uno=True
dos=False
#finFalla=0

def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y

    if event.inaxes:
        ax = event.inaxes  # the axes instance
        #print('data coords %f %f' % (event.xdata, event.ydata))
        plt.ion()
        plt.clf()
        plt.plot(A,'g',label='A')
        plt.plot(B,'r',label='B')
        plt.plot(C,'y',label='C')
        plt.legend()  # Creamos la caja con la leyenda
        
        #plt.draw()
        plt.axvspan(event.xdata,event.xdata+32, alpha = 0.25)


def on_click(event):
    # get the x and y coords, flip y from top to bottom
    x, y = event.x, event.y
    if event.button == 1:
        if event.inaxes is not None:
            print('data coords %f %f' % (event.xdata, event.ydata))
            print(iniPre)
            '''if (iniPre==0):
                iniPre=event.xdata
                plt.suptitle(u'Seleccione el ciclo de falla')  # Ponemos un titulo superior
            else:
                iniFalla=event.xdata
                plt.close(fig)'''
            #uno=False
            #print(uno)
            
            


def analisis_grafica(carpeta,nombre):
    fig = plt.figure()
    ax = plt.subplot(111)
    
    #prueba=cm.comtrade(carpeta, nombre)
    #prueba.config()
    #prueba.extraerDatos()
    
    #A=prueba.oscilografia[:,11]
    #B=prueba.oscilografia[:,10]
    #C=prueba.oscilografia[:,9]
    
    
    plt.plot(A,'g',label='A')
    plt.plot(B,'r',label='B')
    plt.plot(C,'y',label='C')
    plt.suptitle(u'Seleccione el ciclo prefalla')  # Ponemos un titulo superior
    plt.legend()  # Creamos la caja con la leyenda
    
    binding_id = plt.connect('motion_notify_event', on_move)
    plt.connect('button_press_event', on_click)
    
    '''if "test_disconnect" in sys.argv:
        print("disconnecting console coordinate printout...")
        plt.disconnect(binding_id)'''
    
    
    #plt.ion()  # Ponemos el modo interactivo
    #plt.axvspan(-0.5,0.5, alpha = 0.25)
    plt.show()
    
''''t = np.arange(0.0, 1.0, 0.01)
s = np.sin(2*np.pi*t)
fig, ax = plt.subplots()
#plt.plot(t,s)'''

carpeta="C:\Users\NECSOFT\workspace\Prueba1\principal\CODIGO ENTREGA"
nombre="15062257"

prueba=cm.comtrade(carpeta, nombre)
prueba.config()
prueba.extraerDatos()

A=prueba.oscilografia[:,11]
B=prueba.oscilografia[:,10]
C=prueba.oscilografia[:,9]

analisis_grafica(carpeta,nombre)

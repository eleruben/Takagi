"""
An example of how to interact with the plotting canvas by connecting
to move and click events
"""
from __future__ import print_function
import sys
import matplotlib.pyplot as alt
import numpy as np

import claseComtrade as cm

'''iniFalla=0
iniPre=0
uno=True
dos=False
#finFalla=0'''


class graficas(object):
    #Constructor de clase comtrade
    def __init__(self, carpeta, nombre, oscilografia):
    #def __init__(self, carpeta, nombre):
        self.carpeta=carpeta
        self.nombre=nombre
        self.iniFalla=0
        self.iniPre=0
        self.uno=True
        self.dos=False
        self.A=oscilografia[:,11]
        self.B=oscilografia[:,10]
        self.C=oscilografia[:,9]
        self.fig = alt.figure(2)
        #self.ax = alt.subplot(111)
        self.ax = self.fig.add_subplot(1,1,1)



    def analisis_grafica(self):
        
        
        #prueba=cm.comtrade(carpeta, nombre)
        #prueba.config()
        #prueba.extraerDatos()
        
        #A=prueba.oscilografia[:,11]
        #B=prueba.oscilografia[:,10]
        #C=prueba.oscilografia[:,9]
        
        
        alt.plot(self.A,'g',label='A')
        alt.plot(self.B,'r',label='B')
        alt.plot(self.C,'y',label='C')
        alt.suptitle(u'Seleccione el ciclo prefalla')  # Ponemos un titulo superior
        alt.legend()  # Creamos la caja con la leyenda
        
        binding_id = alt.connect('motion_notify_event', on_move)
        alt.connect('button_press_event', on_click)
        
        '''if "test_disconnect" in sys.argv:
            print("disconnecting console coordinate printout...")
            plt.disconnect(binding_id)'''
        
        
        #plt.ion()  # Ponemos el modo interactivo
        #plt.axvspan(-0.5,0.5, alpha = 0.25)
        alt.show()
        
''''t = np.arange(0.0, 1.0, 0.01)
s = np.sin(2*np.pi*t)
fig, ax = plt.subplots()
#plt.plot(t,s)'''
    
    

def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y

    if event.inaxes:
        ax = event.inaxes  # the axes instance
        #print('data coords %f %f' % (event.xdata, event.ydata))
        alt.ion()
        alt.clf()
        alt.plot(obyeyo.A,'g',label='A')
        alt.plot(obyeyo.B,'r',label='B')
        alt.plot(obyeyo.C,'y',label='C')
        alt.legend()  # Creamos la caja con la leyenda
        
        #plt.draw()
        alt.axvspan(event.xdata,event.xdata+32, alpha = 0.25)


def on_click(event):
    # get the x and y coords, flip y from top to bottom
    x, y = event.x, event.y
    if event.button == 1:
        if event.inaxes is not None:
            print('data coords %f %f' % (event.xdata, event.ydata))
            
            if (obyeyo.iniPre==0):
                obyeyo.iniPre=event.xdata
                alt.suptitle(u'Seleccione el ciclo de falla')  # Ponemos un titulo superior
            else:
                obyeyo.iniFalla=event.xdata
                alt.close(obyeyo.fig)
            #uno=False
            #print(uno)




carpeta="C:\Users\NECSOFT\workspace\Prueba1\principal\CODIGO ENTREGA"
nombre="15062257"

prueba=cm.comtrade(carpeta, nombre)
prueba.config()
prueba.extraerDatos()

#A=prueba.oscilografia[:,11]
#B=prueba.oscilografia[:,10]
#C=prueba.oscilografia[:,9]

obyeyo=graficas(carpeta, nombre,prueba.oscilografia)

obyeyo.analisis_grafica()
#analisis_grafica(carpeta,nombre)

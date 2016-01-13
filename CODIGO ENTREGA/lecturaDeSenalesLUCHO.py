# -*- coding: utf-8 -*-
import claseComtrade as cm
import LSQ_quintoLUCHO as lsq
import math
import cmath

#Funcion Verificar, permite ver si una senhal corresponde con los criterios para
#decir si esta tiene una falla. Los criterios son los siguientes:
    #Estabilidad en la magnitud de la senhal durante la primera parte de la misma.
    #Inestabilidad en las magnitudes durante la aparicion de una falla
    #Estabilidad en la magnitud de la senhal durante la parte de posfalla.
    #La magnitud del fasor en el punto de prefalla debe ser menor que el fasor
    #del punto de posfalla, con una diferencia de al menos 40 amperios.



def Verificar(tiempo, senal):
    Magn=[];
    Difn=[];
    etapa=1;
    pre=0;
    iniPre=0;
    iniFalla=0;
    #Calculo de las magnitudes de los fasores de la señal
    for j in range(len(senal)-31):
        [Fasor, Mag, Fase]=lsq.Lsq5(tiempo[j:j+31], senal[j:j+31]);
        Magn.append(Mag);

        #Inicio del proceso de verificación, cada vez que cumple con algún criterio
        #avanza de etapa.

    for j in range(len(Magn)-3):
        dif = math.fabs(Magn[j+3]-Magn[j]);
        #Estabilidad en prefalla
        if etapa == 1:
            if dif < 2:
                pre = pre + 1;

                if iniPre == 0:
                    iniPre = j + 10;

                if pre == 20:
                    etapa = 2;
                    pre = 0;

            else:
                pre = 0;
                iniPre = 0;

        #Inestabilidad en el cambio de prefalla a posfalla
        elif etapa == 2:
            if dif < 1:
                pre=0;

            else:
                pre = pre + 1;
                if pre == 20:
                    etapa = 3;
                    pre = 0;

        #Estabilidad durante posfalla
        elif etapa == 3:
            if dif < 2:
                pre = pre + 1;
                if iniFalla == 0:
                    iniFalla = j + 10;

                if pre == 20:
                    etapa = 4;
                    pre = 0;

            else:
                pre = 0;
                iniFalla = 0;

        #Magnitud de posfalla mayor que prefalla
        elif etapa == 4:
            if math.fabs(Magn[iniFalla]-Magn[iniPre]) > 40:
                etapa = 5;
            else:
                etapa = 0;


    if etapa == 5:
        sirve = 1;
    else:
        sirve = 0;
    
    return(sirve, iniPre, iniFalla, Difn)


#Ejemplo: Se lee un comtrade y se mira una señal. La función verificar solo sirve
#para mirar el comportamiento de las señales de corriente. En el comtrade, las
#señales de corriente vienen desde el canal 9, organizados de la siguiente manera:
    #Canal 9: Corriente fase C
    #Canal 10: Corriente fase B
    #Canal 11: Corriente fase A
    #Canal 12: Correinte neutro
'''carpeta="/home/alcaucil/Documentos/Labe/codigo/Takagi/python/Comtrade/LeerComtrade/archivos/"
nombre="15061451"

prueba=cm.comtrade(carpeta, nombre)
prueba.config()
prueba.extraerDatos()'''

#La función regresa la variable sirve. Si sirve es igual a 0, la señal no sirve,
#si es 1, si sirve, además retorna el punto para hallar el fasor de prefalla y posfalla.

'''[sirve, iniPre, iniFalla, Difn]=Verificar(prueba.oscilografia[:,0],prueba.oscilografia[:,11])

print (sirve, iniPre, iniFalla)'''




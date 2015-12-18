#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import time
import serial
import numpy as np
import matplotlib.pyplot as plt

# Iniciando conexi?n serial
arduinoPort = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
flagCharacter = '?'

# Retardo para establecer la conexi?n serial
time.sleep(1.8)

for curva in range(150):

    arduinoPort.flushInput()

    arduinoPort.write(flagCharacter)

    Voltaje=[];
    TiempoVoltaje=[];
    Corriente=[];
    TiempoCorriente=[];

    for i in range(2500):
        Corriente.append(arduinoPort.readline())
        TiempoCorriente.append(arduinoPort.readline())
        Voltaje.append(arduinoPort.readline())
        TiempoVoltaje.append(arduinoPort.readline())
        #getSerialValue = arduinoPort.read()
        #getSerialValue = arduinoPort.read(5)


    #for i in range(1,4999):
     #   Voltaje[i] = float(Voltaje[i].strip("\n\r"))
      #  TiempoVoltaje[i] = float(TiempoVoltaje[i].strip("\n\r"))

    del Corriente[0]
    del Voltaje[0]
    del TiempoCorriente[0]
    del TiempoVoltaje[0]

    #del Corriente[1]
    #del Voltaje[1]
    #del TiempoCorriente[1]
    #del TiempoVoltaje[1]
    """
    plt.figure(1)
    plt.subplot(221)
    plt.title("Voltaje contra corriente")
    plt.plot(Voltaje,Corriente,"b");
    plt.subplot(222)
    plt.title("Curva de la Corriente")
    plt.plot(Corriente,TiempoCorriente, "b");
    plt.subplot(223)
    plt.title("Curva de Tension")
    plt.plot(Voltaje, TiempoVoltaje,  "b");
    plt.show()
    """

    Carpeta="/home/alcaucil/Documentos/Proyectos/python/Ejemplos/"
    Datos=open(Carpeta+str(curva)+"Datos.csv", "w+")

    for n in range(0, 2499):
        Datos.write(Voltaje[n].strip("\n\r"))
        Datos.write("\t")
        Datos.write(TiempoVoltaje[n].strip("\n\r"))
        Datos.write("\t")
        Datos.write(Corriente[n].strip("\n\r"))
        Datos.write("\t")
        Datos.write(TiempoCorriente[n].strip("\n\r"))
        Datos.write("\n")

    Datos.close()

# Cerrando puerto serial
arduinoPort.close()
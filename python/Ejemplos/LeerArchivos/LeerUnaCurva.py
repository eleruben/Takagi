#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import time
import serial
import numpy as np
import matplotlib.pyplot as plt

# Iniciando conexi?n serial
arduinoPort = serial.Serial('/dev/ttyACM0',115200, timeout=1)
flagCharacter = '?'

Voltaje=[];
TiempoVoltaje=[];
Corriente=[];
TiempoCorriente=[];
Potencia=[];

# Retardo para establecer la conexi?n serial
time.sleep(1.8)
arduinoPort.write(flagCharacter)
arduinoPort.flushInput()
hora=time.strftime("%H:%M:%S")

for i in range(5000):
    Corriente.append(arduinoPort.readline())
    while(Corriente[0] == ''):
        del Corriente[0]
        Corriente.append(arduinoPort.readline())

    TiempoCorriente.append(arduinoPort.readline())
    Voltaje.append(arduinoPort.readline())
    TiempoVoltaje.append(arduinoPort.readline())
    #getSerialValue = arduinoPort.read()
    #getSerialValue = arduinoPort.read(5)


# Cerrando puerto serial
arduinoPort.close()

for i in range(0,5000):
    Voltaje[i] = float(Voltaje[i].strip("\n\r")) * 0.0276085
    TiempoVoltaje[i] = float(TiempoVoltaje[i].strip("\n\r")) / 1000000
    Corriente[i] = float(Corriente[i].strip("\n\r")) *   0.01963486108 #0.002138772
    TiempoCorriente[i] = float(TiempoCorriente[i].strip("\n\r")) / 1000000


for i in range(0,5000):
    Potencia.append(Voltaje[i]*Corriente[i])

plt.figure(1)
plt.subplot(221)
plt.title("Voltaje contra corriente")
plt.plot(Voltaje,Corriente,"b");
plt.subplot(223)
plt.title("Curva de la Corriente")
plt.plot(TiempoCorriente, Corriente,"b");
plt.subplot(222)
plt.title("Curva de Tension")
plt.plot(TiempoVoltaje, Voltaje, "b");
plt.subplot(224)
plt.title("Curva de Potencia")
plt.plot(TiempoVoltaje, Potencia, "b")
plt.show()

Carpeta="/home/alcaucil/Documentos/Proyectos/python/Ejemplos/"
Datos=open(Carpeta + "DatosNuevos.csv", "w+")

Datos.write(hora)
Datos.write("\n")
Datos.write("Voltaje")
Datos.write("\t")
Datos.write("Tiempo V")
Datos.write("\t")
Datos.write("Corriente")
Datos.write("\t")
Datos.write("Tiempo I")
Datos.write("\n")

for n in range(0, 5000):
    Datos.write(str(Voltaje[n]))
    Datos.write("\t")
    Datos.write(str(TiempoVoltaje[n]))
    Datos.write("\t")
    Datos.write(str(Corriente[n]))
    Datos.write("\t")
    Datos.write(str(TiempoCorriente[n]))
    Datos.write("\n")

Datos.close()
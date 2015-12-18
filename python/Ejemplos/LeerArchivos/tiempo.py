#import time
import datetime
import os

def CrearArchivo (tiempo):
    fecha = str(tiempo.day) + str(tiempo.month) + str(tiempo.year)
    hora = str(tiempo.hour) + str(tiempo.min) + str(tiempo.second)
    carpeta = os.getcwd()
    archivo=open(carpeta + "lectura" + fecha + "-" + hora + ".csv", "w+")
    #archivo.write("hola")
    print archivo
    CrearColumnas(archivo)
    return archivo

def CrearColumnas (archivo):
    archivo.write("Peso")
    archivo.write("\t")
    archivo.write("Fecha")
    archivo.write("\t")
    archivo.write("Hora")
    archivo.write("\t")
    archivo.write("Balanza")
    archivo.write("\r")
    archivo.write("\n")

#tiempo=time.strftime("%H:%M:%S")
x=datetime.datetime.now()

carpeta = os.getcwd()
#carpeta = os.curdir

print carpeta

#print tiempo
print ("%s:%s:%s.%s"%(x.hour, x.minute, x.second, x.microsecond))
print x

#archivo = CrearArchivo(x)
#print archivo

print str(x.second)

cadena = "   Hola"

z = len(cadena)
cadena=cadena.replace(" ","")
d = len(cadena)

print z
print d
print cadena
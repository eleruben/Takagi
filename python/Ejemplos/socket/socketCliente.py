import socket
import os #Libreria que permite saber el directorio actual
#import SocketServer
import datetime #Libreria para ver la hora del computador

def CrearArchivo (tiempo):
    fecha = str(tiempo.day) + "-" + str(tiempo.month) + "-" + str(tiempo.year) + "_"
    hora = str(tiempo.hour) + ":" + str(tiempo.minute) + ":" + str(tiempo.second)
    carpeta = os.getcwd()
    archivo=open(carpeta + "/lectura" + fecha + "-" + hora + ".csv", "w+")
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
    archivo.write("\n")

HOST = '192.168.0.102'    # The remote host
PORT = 5000              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

tiempo=datetime.datetime.now() #Variable que guarda fecha y hora que registra el pc
                            #para crear el primer archivo que guarda los datos
archivo = CrearArchivo(tiempo) #Crea el archivo inicial de escritura



while True:
    rcv = ''
    rcv = s.recv(15)
    print (rcv)
    rcv=rcv.replace(" ","")

    print (rcv)
    tiempo=datetime.datetime.now() #Variable que guarda fecha y hora que registra el pc
    fecha = str(tiempo.day) + "-" + str(tiempo.month) + "-" + str(tiempo.year)
    hora = str(tiempo.hour) + ":" + str(tiempo.minute) + ":" + str(tiempo.second)
    if tiempo.min == 0 and tiempo.second == 0: #Cuando inicie una nueva hora, se crea un archivo nuevo
        archivo.close()
        archivo = CrearArchivo(tiempo)

    archivo.write(str(rcv))
    archivo.write("\t")
    archivo.write(fecha)
    archivo.write("\t")
    archivo.write(hora)
    archivo.write("\t")
    archivo.write(str(1))
    archivo.write("\r")
    archivo.write("\n")

    #repr(rcv)
s.close()

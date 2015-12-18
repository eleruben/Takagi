# -*- coding: utf-8 -*-
import numpy as np
import random as rn
import matplotlib.pyplot as plt

def invertir(binario):
    lista=[]
    cadena=""
    for i in range(len(binario)):
        lista.append(binario[i])
        if lista[i] == "1":
            lista[i] = "0"
        elif lista[i] == "0":
            lista[i] = "1"
        else:
            lista[i] = "error"
    for i in range(len(lista)):
        cadena = cadena + lista[i]
    return(cadena)
def ConvBinUnsig2Dec(numero):
    valor = int(numero, 2)
    return(valor)
def ConvBinSig2Dec(numero):
    if numero[0] == '1':
        valor = int(numero, 2)
        valor = bin(valor - 1)[2:]
        valor = invertir(valor)
        negativo = int(valor, 2)*-1
        return negativo
    else:
        valor = ConvBinUnsig2Dec(numero)
        return valor

class Comtrade(object):

    def __init__(self, carpeta, nombre):
        self.carpeta=carpeta
        self.nombre=nombre
        self.dato={
            "id":{
                "station_name":"",
                "rec_dev_id":"",
                "rev_year":""
                },
            "ch":{
                "TT":"",
                "NA":"",
                "ND":""
                },
            "AnCh":{
                },
            "DCh":{
                },
            "lf":"",
            "samp":{
                "nrates":"",
                "samples":{
                    }
                },
            "date-time-init":{
                "dd":"",
                "mm":"",
                "yyyy":"",
                "hh":"",
                "ss":""
                },
            "date-time-end":{
                "dd":"",
                "mm":"",
                "yyyy":"",
                "hh":"",
                "ss":""
                },
            "file-type":"",
            "timemult":""
            }
    def leer(self):
        self.archivo = open(self.carpeta+self.nombre+".CFG", "r")
        self.byte = self.archivo.read(1)
        while self.byte != ",":
            self.dato["id"]["station_name"]=self.dato["id"]["station_name"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        while self.byte != ",":
            self.dato["id"]["rec_dev_id"]=self.dato["id"]["rec_dev_id"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        while self.byte != "\n":
            self.dato["id"]["rev_year"]=self.dato["id"]["rev_year"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        while self.byte != ",":
            self.dato["ch"]["TT"]=self.dato["ch"]["TT"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        while self.byte != ",":
            self.dato["ch"]["NA"]=self.dato["ch"]["NA"]+self.byte
            self.byte = self.archivo.read(1)
        self.dato["ch"]["NA"]=self.dato["ch"]["NA"].replace("A","")
        self.byte = self.archivo.read(1)
        while self.byte != "\n":
            self.dato["ch"]["ND"]=self.dato["ch"]["ND"]+self.byte
            self.byte = self.archivo.read(1)
        self.dato["ch"]["ND"]=self.dato["ch"]["ND"].replace("D","")
        self.byte = self.archivo.read(1)
        valor =""
        for i in range(int(self.dato["ch"]["NA"])):
            fin=0
            self.dato["AnCh"]["a"+str(i+1)]=[]
            while fin == 0:
                while self.byte != ",":
                    valor=valor+self.byte
                    self.byte = self.archivo.read(1)
                    if self.byte == "\n":
                        valor=valor.replace("\r","")
                        fin=1
                        break
                #print valor
                self.dato["AnCh"]["a"+str(i+1)].append(valor)
                valor=""
                self.byte=self.archivo.read(1)
        for i in range(int(self.dato["ch"]["ND"])):
            fin=0
            self.dato["AnD"]["a"+str(i+1)]=[]
            while fin == 0:
                while self.byte != ",":
                    valor=valor+self.byte
                    self.byte = self.archivo.read(1)
                    if self.byte == "\n":
                        valor=valor.replace("\r","")
                        fin=1
                        break
                #print valor
                self.dato["AnD"]["a"+str(i+1)].append(valor)
                valor=""
                self.byte=self.archivo.read(1)
        self.archivo.close()


carpeta="/home/alcaucil/Documentos/Proyectos/python/Comtrade/LeerComtrade/0311214040281/"
nombre="15061634"

f=Comtrade(carpeta, nombre)
f.leer()


archivoEscritura="formato.txt"

comtrade=open(f.carpeta+f.nombre+".DAT", "rb")
formato=open(carpeta+archivoEscritura, "w+")
formato.close()

byte=comtrade.read(1)
comtrade.seek(0)
if len(byte) > 0:
    fin=0
    b=1
    while fin == 0:
        nuevo=np.ones((1,int(f.dato["ch"]["NA"])+2))
        e=0
        cursor = comtrade.tell()
        cursor = cursor + 3
        dato = ""
        for i in range(4):
            comtrade.seek(cursor)
            byte=comtrade.read(1)
            byte = "{0:08b}".format(ord(byte))
            dato=dato + byte
            cursor=cursor -1
        dato=int(dato, 2)
        formato=open(carpeta+archivoEscritura, "a")
        formato.write(str(dato))
        nuevo[0][e]=dato
        e+=1
        formato.write(" ")
        formato.close()
        dato = ""
        cursor=cursor+8
        for i in range(4):
            comtrade.seek(cursor)
            byte=comtrade.read(1)
            byte = "{0:08b}".format(ord(byte))
            dato=dato + byte
            cursor=cursor -1
        dato=int(dato, 2)
        formato=open(carpeta+archivoEscritura, "a")
        formato.write(str(dato))
        nuevo[0][e]=dato
        e+=1
        formato.close()
        cursor=cursor+6
        dato=""
        for i in range(int(f.dato["ch"]["NA"])):
            for j in range(2):
                comtrade.seek(cursor+1)
                byte = comtrade.read(1)
                if len(byte) == 0:
                    fin = 1
                    print "fin"
                comtrade.seek(cursor)
                byte = comtrade.read(1)
                byte = "{0:08b}".format(ord(byte))
                dato = dato+byte
                cursor=cursor -1
            dato=ConvBinSig2Dec(dato)
            dato=float(dato)*float(f.dato["AnCh"]["a"+str(i+1)][5])
            formato=open(carpeta+archivoEscritura, "a")
            formato.write(" ")
            formato.write(str(dato))
            nuevo[0][e]=dato
            e+=1
            formato.close()
            dato=""
            cursor = cursor + 4
        formato=open(carpeta+archivoEscritura, "a")
        formato.write("\n")
        formato.close()
        byte=comtrade.read(1)
        if b == 1:
            oscilo = nuevo
            b= 0
        else:
            oscilo= np.vstack([oscilo, nuevo])
    plt.figure(1)
    plt.subplot(411)
    plt.plot(oscilo[0:,0],oscilo[0:,2],"b");
    plt.hold(True)
    plt.plot(oscilo[0:,0],oscilo[0:,3],"r");
    plt.hold(True)
    plt.plot(oscilo[0:,0],oscilo[0:,4],"y");
    plt.subplot(412)
    plt.plot(oscilo[0:,0],oscilo[0:,5],"b");
    plt.hold(True)
    plt.plot(oscilo[0:,0],oscilo[0:,6],"r");
    plt.hold(True)
    plt.plot(oscilo[0:,0],oscilo[0:,7],"y");
    plt.subplot(413)
    plt.plot(oscilo[0:,0],oscilo[0:,8],"b");
    plt.hold(True)
    plt.plot(oscilo[0:,0],oscilo[0:,9],"r");
    plt.hold(True)
    plt.plot(oscilo[0:,0],oscilo[0:,10],"y");
    plt.subplot(414)
    plt.plot(oscilo[0:,0],oscilo[0:,11],"b");
    plt.show()

else:
    print ("No hay datos")

comtrade.close()



# -*- coding: utf-8 -*-
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
        while self.byte != "\n":
            self.dato["lf"]=self.dato["lf"]+self.byte
            self.byte=self.archivo.read(1)
        print self.byte
        self.byte=self.archivo.read(1)
        while self.byte != "\n":
            self.dato["samp"]["nrates"]=self.dato["samp"]["nrates"]+self.byte
            self.byte=self.archivo.read(1)
        self.byte=self.archivo.read(1)
        #for i in range(int(self.dato["samp"]["nrates"])):
            #self.datos["samp"]["samples"]["s"+str(i+1)]=[]

        self.archivo.close()

carpeta="/home/alcaucil/Documentos/Proyectos/python/Comtrade/LeerComtrade/0311214040281/"
nombre="15061554"


f=Comtrade(carpeta, nombre)
f.leer()
print f.dato["AnCh"]["a1"]
print f.dato["lf"]
print f.dato["samp"]["nrates"]



























"""def invertir(binario):
    lista=[]
    print binario
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

config={
    "Id" : {"station_name":  "NOJA-RC10 0311214040281",
            "rec_dev_id" : "0311214040281",
            "rev_year" : "1999"},
    "Ch" : {"TT" : "10",
            "##A": "10",
            "##D" : "0"}
    "A1" : {}
    }

print config["Identificacion"]["station_name"]

config = {}
config["id"]={}

print config


for i in range(10):
    print "canal"+str(i)"""



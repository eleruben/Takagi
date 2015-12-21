# -*- coding: utf-8 -*-
import numpy as np
import random as rn
import matplotlib.pyplot as plt
import xlwt
import xlrd

class comtrade(object):

    def __init__(self, carpeta, nombre):
        self.carpeta=carpeta
        self.nombre=nombre

    def invertir(self,binario):
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
    def ConvBinUnsig2Dec(self, numero):
        valor = int(numero, 2)
        return(valor)
    def ConvBinSig2Dec(self, numero):
        if numero[0] == '1':
            valor = int(numero, 2)
            valor = bin(valor - 1)[2:]
            valor = self.invertir(valor)
            negativo = int(valor, 2)*-1
            return negativo
        else:
            valor = self.ConvBinUnsig2Dec(numero)
            return valor

    def parametrosConfig(self):
        self.cfg={
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
                "samples":[
                    ]
                },
            "date-time-init":{
                "dd":"",
                "mm":"",
                "yyyy":"",
                "hh":"",
                "min":"",
                "ss":""
                },
            "date-time-trigger":{
                "dd":"",
                "mm":"",
                "yyyy":"",
                "hh":"",
                "min":"",
                "ss":""
                },
            "file-type":"",
            "timemult":""
            }

    def config(self):
        self.parametrosConfig()
        self.archivo = open(self.carpeta+"/"+self.nombre+".CFG", "r")
        self.byte = self.archivo.read(1)
        #Lectura del nombre del dispositivo
        while self.byte != ",":
            self.cfg["id"]["station_name"]=self.cfg["id"]["station_name"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        #Lectura de id del dispositivo
        while self.byte != ",":
            self.cfg["id"]["rec_dev_id"]=self.cfg["id"]["rec_dev_id"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        #Lectura de aÃ±o de revisiÃ³n de protocolo comtrade IEEE
        while self.byte != "\n":
            self.cfg["id"]["rev_year"]=self.cfg["id"]["rev_year"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        #Inicio de lectura de cantidad de canales leÃ­dos tanto anÃ¡logos como digitales
        while self.byte != ",":
            self.cfg["ch"]["TT"]=self.cfg["ch"]["TT"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        #Inicio de lectura de cantidad de canales anÃ¡logos
        while self.byte != ",":
            self.cfg["ch"]["NA"]=self.cfg["ch"]["NA"]+self.byte
            self.byte = self.archivo.read(1)
        self.cfg["ch"]["NA"]=self.cfg["ch"]["NA"].replace("A","")
        self.byte = self.archivo.read(1)
        #Fin de lectura de cantidad de canales anÃ¡logos
        #Inicio de lectura de cantidad de canales digitales
        while self.byte != "\n":
            self.cfg["ch"]["ND"]=self.cfg["ch"]["ND"]+self.byte
            self.byte = self.archivo.read(1)
        self.cfg["ch"]["ND"]=self.cfg["ch"]["ND"].replace("D","")
        self.byte = self.archivo.read(1)
        valor =""
        #Fin de lectura de cantidad de canales digitales
        #Inicio de lectura de canales anÃ¡logos
        for i in range(int(self.cfg["ch"]["NA"])):
            fin=0
            self.cfg["AnCh"]["a"+str(i+1)]=[]
            while fin == 0:
                while self.byte != ",":
                    valor=valor+self.byte
                    self.byte = self.archivo.read(1)
                    if self.byte == "\n":
                        valor=valor.replace("\r","")
                        fin=1
                        break
                self.cfg["AnCh"]["a"+str(i+1)].append(valor)
                valor=""
                self.byte=self.archivo.read(1)
        #Fin de lectura de canÃ¡les anÃ¡logos
        #Lectura canÃ¡les digitales
        for i in range(int(self.cfg["ch"]["ND"])):
            fin=0
            self.cfg["AnD"]["a"+str(i+1)]=[]
            while fin == 0:
                while self.byte != ",":
                    valor=valor+self.byte
                    self.byte = self.archivo.read(1)
                    if self.byte == "\n":
                        valor=valor.replace("\r","")
                        fin=1
                        break
                self.cfg["AnD"]["a"+str(i+1)].append(valor)
                valor=""
                self.byte=self.archivo.read(1)
        #Fin de lectura de los canales digitales
        #Inicio de lectura de frecuencia de la seÃ±al
        while self.byte != "\n":
            self.cfg["lf"]=self.cfg["lf"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        #Inicio de lectura de nÃºmero de tasas de muestreo
        while self.byte != "\n":
            self.cfg["samp"]["nrates"]=self.cfg["samp"]["nrates"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        #Inicio de lectura de las diferentes tasas de muestreo
        b=1
        for i in range(int(self.cfg["samp"]["nrates"])):
            nuevo = np.ones((1,2))
            valor=""
            while self.byte != ",":
                valor=valor+self.byte
                self.byte = self.archivo.read(1)
            nuevo[0,0]=valor
            valor=""
            self.byte = self.archivo.read(1)
            while self.byte != "\n":
                valor=valor+self.byte
                self.byte = self.archivo.read(1)
            nuevo[0,1]=valor
            self.byte = self.archivo.read(1)
            if b == 1:
                self.cfg["samp"]["samples"]=nuevo
                b=0
            else:
                self.cfg["samp"]["samples"]=np.vstack([self.cfg["samp"]["samples"],nuevo])
        valor = ""
        while self.byte != "/":
            valor = valor + self.byte
            self.byte = self.archivo.read(1)
            print self.byte

        self.cfg["date-time-init"]["dd"]=valor
        self.byte = self.archivo.read(1)
        valor = ""
        while self.byte != "/":
            valor = valor + self.byte
            self.byte = self.archivo.read(1)
        self.cfg["date-time-init"]["mm"]=valor
        self.byte = self.archivo.read(1)
        valor = ""
        while self.byte != ",":
            valor = valor + self.byte
            self.byte = self.archivo.read(1)
        self.cfg["date-time-init"]["yyyy"]=valor
        self.byte = self.archivo.read(1)
        valor = ""
        while self.byte != ":":
            valor = valor + self.byte
            self.byte = self.archivo.read(1)
        self.cfg["date-time-init"]["hh"]=valor
        self.byte = self.archivo.read(1)
        valor = ""
        while self.byte != ":":
            valor = valor + self.byte
            self.byte = self.archivo.read(1)
        self.cfg["date-time-init"]["min"]=valor
        self.byte = self.archivo.read(1)
        valor = ""
        while self.byte != "\n":
            valor = valor + self.byte
            self.byte = self.archivo.read(1)
        self.cfg["date-time-init"]["ss"]=valor
        self.byte = self.archivo.read(1)
        valor = ""
        self.archivo.close()

    def extraerDatos(self):

        comtrade=open(self.carpeta+"/"+self.nombre+".DAT", "rb")

        byte=comtrade.read(1)
        comtrade.seek(0)
        if len(byte) > 0:
            fin=0
            b=1
            muestra=1
            muestreo = 0

            while fin == 0:
                nuevo=np.ones((1,int(self.cfg["ch"]["NA"])+3))
                e=1
                if b==1:
                    nuevo[0,0]=0
                else:
                    nuevo[0,0]=self.oscilografia[muestra-2, 0]+1/(self.cfg["samp"]["samples"][muestreo][0])
                muestra+=1
                #print b
                #print nuevo[0,0]
                if muestra > self.cfg["samp"]["samples"][muestreo][1]:
                    muestreo += 1
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
                nuevo[0][e]=dato
                e+=1
                dato = ""
                cursor=cursor+8
                for i in range(4):
                    comtrade.seek(cursor)
                    byte=comtrade.read(1)
                    byte = "{0:08b}".format(ord(byte))
                    dato=dato + byte
                    cursor=cursor -1
                dato=int(dato, 2)
                nuevo[0][e]=dato
                e+=1
                cursor=cursor+6
                dato=""
                for i in range(int(self.cfg["ch"]["NA"])):
                    for j in range(2):
                        comtrade.seek(cursor+1)
                        byte = comtrade.read(1)
                        if len(byte) == 0:
                            fin = 1
                        comtrade.seek(cursor)
                        byte = comtrade.read(1)
                        byte = "{0:08b}".format(ord(byte))
                        dato = dato+byte
                        cursor=cursor -1
                    dato=self.ConvBinSig2Dec(dato)
                    dato=float(dato)*float(self.cfg["AnCh"]["a"+str(i+1)][5])
                    nuevo[0][e]=dato
                    e+=1
                    dato=""
                    cursor = cursor + 4
                byte=comtrade.read(1)
                if b == 1:
                    self.oscilografia = nuevo
                    b= 0
                else:
                    self.oscilografia= np.vstack([self.oscilografia, nuevo])

    def exportTXT(self):
        archivoEscritura="formato.txt"
        formato=open(self.carpeta+"/"+archivoEscritura, "w+")
        formato.close()
        for i in range(len(self.oscilografia[0:])):
            for j in range(len(self.oscilografia[i,0:])):
                formato=open(self.carpeta+archivoEscritura, "a")
                dato=str(self.oscilografia[i][j])
                dato=dato.replace(".", ",")
                formato.write(dato)
                formato.write(" ")
                formato.close()
            formato=open(self.carpeta+archivoEscritura, "a")
            formato.write("\n")
            formato.close()

    def excel(self):
        wb=xlwt.Workbook()
        for i in range(int(self.cfg["ch"]["NA"])):
            ws = wb.add_sheet(self.cfg["AnCh"]["a"+str(i+1)][1],cell_overwrite_ok=True)
            fila=0
            columna=0
            for j in range(len(self.oscilografia[0:,1])):
                if columna < 32:
                    ws.write(fila,columna+1,self.oscilografia[j,1])
                    ws.write(fila+1,columna+1,self.oscilografia[j,0])
                    ws.write(fila+2,columna+1,self.oscilografia[j,i+3])
                    columna+=1
                else:
                    fila+=4
                    columna=0
                    ws.write(fila,columna+1,self.oscilografia[j,1])
                    ws.write(fila+1,columna+1,self.oscilografia[j,0])
                    ws.write(fila+2,columna+1,self.oscilografia[j,i+3])
                    columna+=1
            fila=0
            for l in range(len(self.oscilografia[0:,1])/32):
                ws.write(fila,0,"Muestra")
                ws.write(fila+1,0,"Tiempo")
                ws.write(fila+2,0,self.cfg["AnCh"]["a"+str(i+1)][1])
                fila+=4
        wb.save(self.carpeta+'example.xls')

    def excelRudas(self):
        wb=xlwt.Workbook()
        ws = wb.add_sheet("Comtrade",cell_overwrite_ok=True)
        ws.write(0,0,"Muestra")
        ws.write(0,1,"Tiempo(ms)")
        ws.write(0,2,"Hora")
        ws.write(0,3,"Min")
        ws.write(0,4,"Seg")
        columna=5
        for i in range(int(self.cfg["ch"]["NA"])):
            nom=self.cfg["AnCh"]["a"+str(i+1)][1]
            if nom != "Vs" and nom != "Vr" and nom != "Vt":
                ws.write(0,columna,self.cfg["AnCh"]["a"+str(i+1)][1])
                columna+=1
        for i in range(len(self.oscilografia[0:,1])):
            ws.write(i+1,0,self.oscilografia[i,1])
            ws.write(i+1,1,float(self.oscilografia[i,0])*1000)
            ws.write(i+1,2,int(self.cfg["date-time-init"]["hh"]))
            ws.write(i+1,3,int(self.cfg["date-time-init"]["min"]))
            ws.write(i+1,4,float(self.cfg["date-time-init"]["ss"])+float(self.oscilografia[i,0]))
            columna=4
            for j in range(int(self.cfg["ch"]["NA"])):
                nom=self.cfg["AnCh"]["a"+str(j+1)][1]
                if nom != "Vs" and nom != "Vr" and nom != "Vt":
                    ws.write(i+1,columna+1,self.oscilografia[i,j+3])
                    columna+=1
        wb.save(self.carpeta+"/"+self.nombre+".xls")
    def excelRudas2(self):
        wb=xlwt.Workbook()
        ws = wb.add_sheet("Comtrade",cell_overwrite_ok=True)
        ws.write(0,0,"Muestra")
        ws.write(0,1,"Tiempo(ms)")
        ws.write(0,2,"Hora")
        ws.write(0,3,"Min")
        ws.write(0,4,"Seg")
        columna=5
        for i in range(int(self.cfg["ch"]["NA"])):
            nom=self.cfg["AnCh"]["a"+str(i+1)][1]
            ws.write(0,columna,self.cfg["AnCh"]["a"+str(i+1)][1])
            columna+=1
        for i in range(len(self.oscilografia[0:,1])):
            ws.write(i+1,0,self.oscilografia[i,1])
            ws.write(i+1,1,float(self.oscilografia[i,0])*1000)
            ws.write(i+1,2,int(self.cfg["date-time-init"]["hh"]))
            ws.write(i+1,3,int(self.cfg["date-time-init"]["min"]))
            ws.write(i+1,4,float(self.cfg["date-time-init"]["ss"])+float(self.oscilografia[i,0]))
            columna=4
            for j in range(int(self.cfg["ch"]["NA"])):
                nom=self.cfg["AnCh"]["a"+str(j+1)][1]
                ws.write(i+1,columna+1,self.oscilografia[i,j+3])
                columna+=1
        wb.save(self.carpeta+"/"+self.nombre+".xls")
    #def dividirDatos(self):


<<<<<<< HEAD
carpeta="/home/alcaucil/Descargas/oscilografias/ultimas/"
nombre="70010171"
#OBJETO DE LA CLASE COMTRADE
=======
carpeta=r"C:\Users\NECSOFT\Documents\Labe\Takagi\Takagi\python\Comtrade\LeerComtrade\0311214040281"
nombre=r"14082605"

>>>>>>> origin/master
prueba=comtrade(carpeta, nombre)
prueba.config()
prueba.extraerDatos()
prueba.exportTXT()
prueba.excelRudas2()
print prueba.cfg["date-time-init"]
#prueba.dividirDatos()
"""
print prueba.cfg["AnCh"]["a1"][1]

plt.figure(1)
plt.subplot(331)
plt.plot(prueba.oscilografia[0:31,0],prueba.oscilografia[0:31,5],"b");
plt.subplot(332)
plt.plot(prueba.oscilografia[32:63,0],prueba.oscilografia[32:63,5],"b");
plt.subplot(333)
plt.plot(prueba.oscilografia[64:95,0],prueba.oscilografia[64:95,5],"b");
plt.subplot(334)
plt.plot(prueba.oscilografia[96:127,0],prueba.oscilografia[96:127,5],"b");
plt.subplot(335)
plt.plot(prueba.oscilografia[128:159,0],prueba.oscilografia[128:159,5],"b");
plt.subplot(336)
plt.plot(prueba.oscilografia[160:191,0],prueba.oscilografia[160:191,5],"b");
plt.subplot(337)
plt.plot(prueba.oscilografia[192:223,0],prueba.oscilografia[192:223,5],"b");
plt.subplot(338)
plt.plot(prueba.oscilografia[224:255,0],prueba.oscilografia[224:255,5],"b");
plt.subplot(339)
plt.plot(prueba.oscilografia[256:287,0],prueba.oscilografia[256:287,5],"b");

plt.figure(2)
plt.plot(prueba.oscilografia[0:,0],prueba.oscilografia[0:,5],"b")


plt.show()
"""

# -*- coding: utf-8 -*-
import numpy as np
import random as rn
import matplotlib.pyplot as plt
import xlwt
import xlrd
import os.path

class comtrade(object):
    #Constructor de clase comtrade
    def __init__(self, carpeta, nombre):
        self.carpeta=carpeta
        self.nombre=nombre
        self.parametrosConfig()
        self.arreglo=[]
        self.oscilografia=[]
    #Funcion que retorna el inverso de un numero binario
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

    #Funcion que convierte ????
    def ConvBinUnsig2Dec(self, numero):
        valor = int(numero, 2)
        return(valor)

    #Funcion que convierte ???
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

    #Funcion que inicializa los diccionarios de datos
    #con valores por defecto
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



    ####////////////////////////////////////////////////////////////////////////////
    ####////////////////////////////////////////////////////////////////////////////
    ####//////////////////self.archivo va a contener el archivo .CFG////////////////
    ####////////////////////////////////////////////////////////////////////////////
    ####////////////////////////////////////////////////////////////////////////////
    ####////////////////////////////////////////////////////////////////////////////

        
    #Funcion que lee los valores de el archivo CFG generado por en el formato comtrade
    def config(self):
        #Invocacion de la funcion de inicializacion de los parametros
        #self.parametrosConfig()
        self.archivo = open(self.carpeta+u"/"+self.nombre+".CFG", "r")
        #self.archivo = open(self.carpeta+"/"+self.nombre, "r")
        #self.archivo = open('14082603.CFG', "r")

        #comtrade=open(self.carpeta+self.nombre+".CFG", "rb")
        self.byte = self.archivo.read(1)
        #Lectura del nombre del dispositivo caracter a caracter hasta que se encuentre el
        #caracter ","
        while self.byte != ",":
            self.cfg["id"]["station_name"]=self.cfg["id"]["station_name"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        #Lectura de id del dispositivo caracter a caracter hasta que se encuentre el
        #caracter ","
        while self.byte != ",":
            self.cfg["id"]["rec_dev_id"]=self.cfg["id"]["rec_dev_id"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        #Lectura de año de revisión de protocolo comtrade IEEE caracter a caracter hasta
        #que se encuentre el salto de linea
        while self.byte != "\n":
            self.cfg["id"]["rev_year"]=self.cfg["id"]["rev_year"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        #Inicio de lectura de cantidad de canales leídos tanto análogos como digitales caracter
        #a caracter hasta que se encuentre el caracter ","
        while self.byte != ",":
            self.cfg["ch"]["TT"]=self.cfg["ch"]["TT"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        #Inicio de lectura de cantidad de canales análogos caracter a caracter hasta que se encuentre el
        #caracter ","
        while self.byte != ",":
            self.cfg["ch"]["NA"]=self.cfg["ch"]["NA"]+self.byte
            self.byte = self.archivo.read(1)
        self.cfg["ch"]["NA"]=self.cfg["ch"]["NA"].replace("A","")
        self.byte = self.archivo.read(1)
        #Fin de lectura de cantidad de canales análogos
        
        #Inicio de lectura de cantidad de canales digitales caracter a caracter hasta que se encuentre el
        #salto de linea
        while self.byte != "\n":
            self.cfg["ch"]["ND"]=self.cfg["ch"]["ND"]+self.byte
            self.byte = self.archivo.read(1)
        self.cfg["ch"]["ND"]=self.cfg["ch"]["ND"].replace("D","")
        self.byte = self.archivo.read(1)
        valor =""
        #Fin de lectura de cantidad de canales digitales
        
        #Inicio de lectura de canales análogos caracter a caracter, separados por el caracter "," hasta que
        #se encuentre el caracter salto de linea
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
        #Fin de lectura de canáles análogos
                
        #Lectura canáles digitales caracter a caracter, separados por el caracter "," hasta que
        #se encuentre el caracter salto de linea
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
                
        #Inicio de lectura de frecuencia de la señal caracter a caracter hasta que se encuentre el
        #salto de linea
        while self.byte != "\n":
            self.cfg["lf"]=self.cfg["lf"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        
        #Inicio de lectura de número de tasas de muestreo caracter a caracter hasta que se encuentre el
        #salto de linea
        while self.byte != "\n":
            self.cfg["samp"]["nrates"]=self.cfg["samp"]["nrates"]+self.byte
            self.byte = self.archivo.read(1)
        self.byte = self.archivo.read(1)
        
        #Inicio de lectura de las diferentes tasas de muestreo la cantidad de veces de tasas
        #de muestreo
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
            #print self.byte

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


    ####////////////////////////////////////////////////////////////////////////////
    ####////////////////////////////////////////////////////////////////////////////
    ####//////////////////comtrade va a contener el archivo .DAT////////////////////
    ####////////////////////////////////////////////////////////////////////////////
    ####////////////////////////////////////////////////////////////////////////////
    ####////////////////////////////////////////////////////////////////////////////

    #Funcion que lee los valores de el archivo DAT generado por en el formato comtrade
    #y los guarda en self.oscilografia
    def extraerDatos(self):

        comtrade=open(self.carpeta+u"/"+self.nombre+".DAT", "rb")

        byte=comtrade.read(1)
        #Coloca el apuntador en la posicion inicial
        comtrade.seek(0)
        #self.oscilografia es un arreglo que contiene los datos reportados en el comtrade
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

    #Funcion que exporta los datos de self.oscilografia a un archivo de texto plano txt
    def exportTXT(self):
        archivoEscritura="formato.txt"
        formato=open(self.carpeta+u"/"+archivoEscritura, "w+")
        formato.close()
        for i in range(len(self.oscilografia[0:])):
            for j in range(len(self.oscilografia[i,0:])):
                formato=open(self.carpeta+u"/"+archivoEscritura, "a")
                dato=str(self.oscilografia[i][j])
                dato=dato.replace(".", ",")
                formato.write(dato)
                formato.write(" ")
                formato.close()
            formato=open(self.carpeta+u"/"+archivoEscritura, "a")
            formato.write("\n")
            formato.close()
    
    #Funcion que exporta los datos de self.oscilografia a un archivo excel, esto es util para la opcion de exportar
    #los datos a un archivo excel
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
        wb.save(self.carpeta+u"/"+self.nombre+'.xls')

    #Funcion que exporta los datos de self.oscilografia a un archivo excel, esto es util para la opcion de exportar
    #los datos a un archivo excel
    def excelRudas(self,carpeta,nombre):
        self.carpeta=carpeta
        self.nombre=nombre
        wb=xlwt.Workbook()
        ws = wb.add_sheet("Comtrade "+self.nombre,cell_overwrite_ok=True)
        ws.write(0,0,"Muestra")
        ws.write(0,1,"Tiempo(ms)")
        ws.write(0,2,"Hora")
        ws.write(0,3,"Min")
        ws.write(0,4,"Seg")
        columna=5
        for i in range(int(self.cfg["ch"]["NA"])):
            nom=self.cfg["AnCh"]["a"+str(i+1)][1]
            if nom != "Vs" and nom != "Vr" and nom != "Vt":
                #Indica el nombre de las columnas de corriente y voltaje desde el archivo
                #self.cfg
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
                    #Proceso para llenar la tabla de excel en el siguiente orden:
                    #Va, Vb, Vc, Ia, Ib, Ic e In
                    ws.write(i+1,columna+1,self.oscilografia[i,j+3])
                    columna+=1
        #wb.save(self.carpeta+u"/"+self.nombre+".xls")
        wb.save(self.carpeta+u"/"+self.nombre)

        
    def excelRudas2(self,carpeta,nombre):
        self.carpeta=carpeta
        self.nombre=nombre
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
        #wb.save(self.carpeta+u"/"+self.nombre+".xls")
        wb.save(self.carpeta+u"/"+self.nombre)
    #def dividirDatos(self):

    def extraerListas(self):
        for i in range(len(self.oscilografia[0:,1])):
            self.temporal=[]
            for j in range(int(self.cfg["ch"]["NA"])):
                nom=self.cfg["AnCh"]["a"+str(j+1)][1]
                if nom != "Vs" and nom != "Vr" and nom != "Vt":
                    #Proceso para llenar un arreglo en el siguiente orden:
                    #Va, Vb, Vc, Ia, Ib, Ic e In
                    #ws.write(i+1,columna+1,self.oscilografia[i,j+3])
                    self.temporal.append(self.oscilografia[i,j+3])
                    #columna+=1
            self.arreglo.append(self.temporal)
        #return(arreglo)


#carpeta="/home/alcaucil/Descargas/oscilografias/ultimas/"
carpeta="C:\Users\NECSOFT\Documents\GitHub\Prueba\Takagi\python\Comtrade\LeerComtrade\archivos"
nombre="14082603"
#OBJETO DE LA CLASE COMTRADE
#prueba=comtrade(carpeta, nombre)
#prueba.config()

#prueba.extraerDatos()
#prueba.exportTXT()
#prueba.excelRudas2()
#print prueba.cfg["date-time-init"]
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

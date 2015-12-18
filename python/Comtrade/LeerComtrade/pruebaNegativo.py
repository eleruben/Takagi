carpeta="/home/alcaucil/Documentos/Proyectos/python/Comtrade/LeerComtrade/0311214040281/"
archivoLectura="15042801.DAT"
archivoEscritura="formato1.txt"

comtrade=open(carpeta+archivoLectura, "rb")
escribir=open(carpeta+archivoEscritura, "w+")
dato=""

cursor = 26861

for i in range(10):
            for j in range(2):
                print cursor
                comtrade.seek(cursor+1)
                byte = comtrade.read(1)
                if len(byte) == 0:
                    fin = 1
                    print "fin"
                comtrade.seek(cursor)
                byte = comtrade.read(1)
                byte= str("{0:08b}".format(ord(byte)))
                dato = dato + byte
                print (dato)
                cursor=cursor -1
            magnitudDato = int(dato[1:],2)
            if dato[0] == "1":
                magnitudDato = magnitudDato * -1
            print magnitudDato
            formato=open(carpeta+archivoEscritura, "a")
            formato.write(",")
            formato.write(str(magnitudDato))
            formato.close()
            dato=""
            cursor = cursor + 4





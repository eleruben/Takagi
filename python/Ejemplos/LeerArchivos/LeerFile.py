# -*- coding: utf-8 -*-

#Crear Archivo
DatosX = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
DatosY = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
Carpeta="/home/alcaucil/Documentos/Proyectos/python/Ejemplos/"
Datos=open(Carpeta + "Datos.csv", "w+")


print DatosX[1]

for n in range(0, 9):
    Datos.write(str(DatosX[n]))
    Datos.write("\t")
    Datos.write(str(DatosY[n]))
    Datos.write("\n")
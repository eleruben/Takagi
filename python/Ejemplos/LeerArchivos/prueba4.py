import numpy as np

archivo=open("/home/alcaucil/Documentos/Proyectos/python/Ejemplos/DatosNuevos.csv", "a")
final=archivo.tell()

print final

archivo.close()

"""

for i in range(len(datos)):
    if i < 3:
        datos2.append(np.median(datos[i:(i+3)]))
    elif i > 2 and i < (len(datos)-3):
        datos2.append(np.median(datos[i-3:i+3]))
    else:
        datos2.append(np.median(datos[i-3:]))

print datos2"""
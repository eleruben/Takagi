import claseComtrade

dirname="C:\Users\NECSOFT\Desktop\deteccion de fallas\CODIGO ENTREGA"
filename="14082603"

prueba=claseComtrade.comtrade(dirname, filename)
prueba.config()
prueba.extraerDatos()
#print(prueba.oscilografia[12])

arreglo=[]
for i in range(len(prueba.oscilografia[0:,1])):
    temporal=[]
    for j in range(int(prueba.cfg["ch"]["NA"])):
        nom=prueba.cfg["AnCh"]["a"+str(j+1)][1]
        if nom != "Vs" and nom != "Vr" and nom != "Vt":
            #Proceso para llenar la tabla de excel en el siguiente orden:
            #Va, Vb, Vc, Ia, Ib, Ic e In
            #ws.write(i+1,columna+1,self.oscilografia[i,j+3])
            temporal.append(prueba.oscilografia[i,j+3])
            #columna+=1
    arreglo.append(temporal)

print(arreglo)

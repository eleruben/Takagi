import xlrd
import networkx as nx
import matplotlib.pyplot as plt

import matplotlib.colors as colors
import matplotlib.cm as cmx
import os
print os.getcwd()

##########################################################################
#                CODIGO PARA IMPLEMENTACION VERTICAL DE LOS NODOS        #
##########################################################################


#se extraen los valores del circuito de una tabla de excel
#libro = xlrd.open_workbook("C:\Users\Ricardo\Documents\deteccion de fallas/Modelo circuito.xls")

def Grafos():
    Ext1=[]
    Ext2=[]
    Distancia=[]
    #Abre el archivo de excel en donde esta el modelo del circuito, este archivo debe estar
    #en la misma carpeta que el archivo que se esta ejecutando
    libro = xlrd.open_workbook(str(os.getcwd())+"\Modelo circuito.xlsX")
    #libro = xlrd.open_workbook("C:\Users\NECSOFT\Desktop\deteccion de fallas\Modelo circuito.xlsX")
    for r in range(int(libro.nsheets)):
        if libro.sheet_by_index(r).name == "Consecutivo":
        #if libro.sheet_by_index(r).name == "Prueba":
            p = r
    pest = libro.sheet_by_index(p)
    for i in range(pest.ncols):
        for j in range(pest.nrows):
            if i==0 and j!=0: Ext1.append(str(pest.cell_value(rowx=j, colx=i)))
            if i==1 and j!=0: Ext2.append(str(pest.cell_value(rowx=j, colx=i)))
            if i==3 and j!=0: Distancia.append(pest.cell_value(rowx=j, colx=i))
    #se crea el grafo y se define el tipo de dato que va a ser
    Grafo = nx.Graph()
    #se recorre todo la lista de los datos de la primera columna
    for i in range(len(Ext1)):
        print("i va en "+str(i))
        #Caso en el que se adicionan los dos primeros nodos y se establece un
        #camino entre ellos
        if i==0:
            Grafo.add_node(Ext1[i],pos=(0,0),acumulado=0)
            Grafo.add_node(Ext2[i],pos=(0,Distancia[i]),acumulado=Distancia[i])
            Grafo.add_edge(Ext1[i],Ext2[i],length=Distancia[i])

        else:
            #Es necesario conocer cual de los nodos ya esta agregado al grafo y continuar
            #el camino, en el caso de los ramales es necesario conocer la arista del nodo
            #que conduzca al origen, para asi poder calcular el acumulado de la distancia
            #al ramal
            for j in range(len(Grafo.nodes())):
                #se verifica que la arista que se va a agregar este conectada al ramal
                #por solo uno de sus nodos
                temporal=0
                ac=0
                length=nx.get_edge_attributes(Grafo,'length')
                #Acumulado es un atributo del nodo que se obtiene de sumar todos las longitudes
                #del trayecto al nodo origen
                acumulado=nx.get_node_attributes(Grafo,'acumulado')
                pos=nx.get_node_attributes(Grafo,'pos')
                desviacion=0
                ##Se evaluan los dos caso para descartar que se agregue el nodo el diferente orden
                if Ext1[i] in Grafo.nodes() and Ext2[i] not in Grafo.nodes():
                    ##En el caso de las ramas se necesita conocer la posicion del
                    ##nodo al que esta asociado
                    if len(Grafo.neighbors(Ext1[i]))==2:
                        #Caso en que se agrega una rama estando dos en linea en la linea base #0
                        if(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]==0) and (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0] == 0):
                            Grafo.add_node(Ext2[i],pos=(Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        #Caso en que se agrega una nueva rama a la izquierda #1
                        elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]<0) or (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0]<0):
                            Grafo.add_node(Ext2[i],pos=(-Distancia[i]+pos[Ext1[i]][0],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        #Caso en que se agrega una nueva rama a la derecha #2
                        elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]>0) or (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0]>0):
                            Grafo.add_node(Ext2[i],pos=(Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                    if len(Grafo.neighbors(Ext1[i]))==3:
                        print("los vecinos de "+str(Ext1[i])+" son "+str(Grafo.neighbors(Ext1[i])))
                        #Caso en que se agrega una nueva rama a la izquierda, los nodos alineados en Y son 1 y 2 #0
                        if(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]==0) and (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0] == 0):
                            print("cas1")
                            Grafo.add_node(Ext2[i],pos=(-Distancia[i]+pos[Ext1[i]][0],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        #Caso en que se agrega una nueva rama a la izquierda, los nodos alineados en Y son 2 y 3 #0
                        elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0]==0) and (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[2]][0] == 0):
                            print("cas2")
                            Grafo.add_node(Ext2[i],pos=(-Distancia[i]+pos[Ext1[i]][0],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        #Caso en que se agrega una nueva rama a la izquierda, los nodos alineados en Y son 1 y 3 #0
                        elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]==0) and (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[2]][0] == 0):
                            print("cas3")
                            Grafo.add_node(Ext2[i],pos=(-Distancia[i]+pos[Ext1[i]][0],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        #Caso en que se agrega una nueva rama abajo, los nodos alineados en X son 1 y 2 #1
                        elif(pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[0]][1]==0) and (pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[1]][1] == 0):
                            print("cas4")
                            Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],pos[Ext1[i]][1]-Distancia[i]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        #Caso en que se agrega una nueva rama abajo, los nodos alineados en X son 2 y 3 #1
                        elif(pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[1]][1]==0) and (pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[2]][1] == 0):
                            print("cas5")
                            Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],pos[Ext1[i]][1]-Distancia[i]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        #Caso en que se agrega una nueva rama abajo, los nodos alineados en X son 1 y 3 #1
                        elif(pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[0]][1]==0) and (pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[2]][1] == 0):
                            print("cas6")
                            Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],pos[Ext1[i]][1]-Distancia[i]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        
                        #Grafo.add_node(Ext2[i],pos=(-Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                    if len(Grafo.neighbors(Ext1[i]))==1:
                        #Caso en que el vecino este agregado por abajo, se agrega hacia arriba #0
                        if(pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[0]][1]>0):
                            print("caso1-1 "+str(Ext2[i]))
                            Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],Distancia[i]+pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        #Caso en que el vecino este agregado por arriba, se agrega por la izquierda #1
                        elif(pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[0]][1]<0):
                            print("caso1-2 "+str(Ext2[i]))
                            Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0]+Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        #Caso en que el vecino este agregado por izquierda, se agrega hacia arriba #2
                        elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]<0):
                            print("caso1-3 "+str(Ext2[i]))
                            Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],Distancia[i]+pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        #Caso en que el vecino este agregado por derecha, se agrega hacia arriba #3
                        elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]>0):
                            print("caso1-4 "+str(Ext2[i]))
                            Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],Distancia[i]+pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])                            
                            
                            
                        
                    Grafo.add_edge(Ext1[i],Ext2[i],length=Distancia[i])
                    break

                ####REVISARRRRR caso de 3 
                if Ext2[i] in Grafo.nodes() and Ext1[i] not in Grafo.nodes():
                    if len(Grafo.neighbors(Ext2[i]))==2:
                        #Caso en que se agrega una rama estando dos en linea en la linea base #0
                        if(pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[0]][0]==0) and (pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[1]][0] == 0):
                            Grafo.add_node(Ext1[i],pos=(Distancia[i],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                        #Caso en que se agrega una nueva rama a la izquierda #1
                        elif(pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[0]][0]<0) or (pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[1]][0]<0):
                            Grafo.add_node(Ext1[i],pos=(-Distancia[i]+pos[Ext2[i]][0],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                        #Caso en que se agrega una nueva rama a la derecha #2
                        elif(pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[0]][0]>0) or (pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[1]][0]>0):
                            Grafo.add_node(Ext1[i],pos=(Distancia[i],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                        
                    if len(Grafo.neighbors(Ext2[i]))==3:
                        print("los vecinos de "+str(Ext1[i])+" son "+str(Grafo.neighbors(Ext2[i])))
                        Grafo.add_node(Ext1[i],pos=(-Distancia[i],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                    if len(Grafo.neighbors(Ext2[i]))==1:
                        Grafo.add_node(Ext1[i],pos=(pos[Ext2[i]][0],Distancia[i]+acumulado[Ext2[i]]),acumulado=acumulado[Ext2[i]]+Distancia[i])

                    Grafo.add_edge(Ext1[i],Ext2[i],length=Distancia[i])
                    break



            acumulado=nx.get_node_attributes(Grafo,'acumulado')    
            length=nx.get_edge_attributes(Grafo,'length')
            #Grafo.add_node(Ext2[i],pos=(Distancia[i],1))
            #length=nx.get_edge_attributes(Grafo,'length')
            #print ("se va a agregar camino entre "+Ext1[i]+" "+Ext2[i])
            #Grafo.add_edge(Ext1[i],Ext2[i],length=Distancia[i])
            #print(length.keys())
            length=nx.get_edge_attributes(Grafo,'length')
            pos=nx.get_node_attributes(Grafo,'pos')
        
    pos=nx.get_node_attributes(Grafo,'pos')
    return Grafo


##Funcion en la cual se ubican los puntos de falla dependiendo de su distancia
##al nodo origen
def punto_falla(Grafo,distancia):
    #####REVISAR CASO EN QUE LA FALLA CAE EN UN NODO
    #Variable utilizada para verificar que la distancia ingresada se encuentra por dentro del circuito
    #dentro=False
    #lista_mayores=[]
    #Se extrae la lista de acumulados de todos los nodos para comparar la posible distancia a la que puede
    #localizarse la falla
    afuera=True
    acumulado=nx.get_node_attributes(Grafo,'acumulado')
    pos=nx.get_node_attributes(Grafo,'pos')
    for nodo in acumulado.keys():
        #Se revisa cual de los nodos tiene mayor distancia a la falla
        if acumulado[nodo]<distancia:
            for n in Grafo.neighbors(nodo):
                #Entra cuando la distancia se encuentre en esta arista
                if acumulado[n]>distancia:
                    print("el tramo esta entre "+str(nodo)+" y "+str(n))
                    print("la distancia de el anterior x es "+str(pos[nodo][0]))
                    print("la distancia de el anterior y es "+str(pos[nodo][1]))
                    print("la distancia de el despues x es "+str(pos[n][0]))
                    print("la distancia de el despues y es "+str(pos[n][1]))
                    #la coordenada diferente se le suma el acumulado del menor mas la distancia
                    if (pos[n][0]-pos[nodo][0]==0) and (pos[n][1]-pos[nodo][1]>0):
                        #Se debe agregar en la coordenada Y hacia arriba
                        Grafo.add_node('Falla'+str(nodo)+"-"+str(n),pos=(pos[n][0],pos[nodo][1]+(distancia-acumulado[nodo])),acumulado=distancia,color=1.0)
                        afuera=False
                    elif (pos[n][0]-pos[nodo][0]==0) and (pos[n][1]-pos[nodo][1]<0):
                        #Se debe agregar en la coordenada Y hacia abajo
                        Grafo.add_node('Falla'+str(nodo)+"-"+str(n),pos=(pos[n][0],pos[nodo][1]-(distancia-acumulado[nodo])),acumulado=distancia,color=2.0)
                        afuera=False
                    elif (pos[n][1]-pos[nodo][1]==0) and (pos[n][0]-pos[nodo][0]<0):
                        #Se debe agregar en la coordenada X hacia derecha
                        Grafo.add_node('Falla'+str(nodo)+"-"+str(n),pos=(pos[nodo][0]-(distancia-acumulado[nodo]),pos[n][1]),acumulado=distancia,color=3.0)
                        afuera=False
                    elif (pos[n][1]-pos[nodo][1]==0) and (pos[n][0]-pos[nodo][0]>0):
                        #Se debe agregar en la coordenada X hacia izquierda
                        Grafo.add_node('Falla'+str(nodo)+"-"+str(n),pos=(pos[nodo][0]+(distancia-acumulado[nodo]),pos[n][1]),acumulado=distancia,color=4.0)
                        afuera=False
    if afuera:
        print("LA DISTANCIA DE FALLA NO ESTA EN EL CIRCUITO")
    return Grafo      


def imprimir_grafo(Grafo):
    pos=nx.get_node_attributes(Grafo,'pos')
    color=nx.get_node_attributes(Grafo,'color')

    ###PRUEBA DE COLOR EN LOS GRAFOS
    val_map = {'B4': 1.0,
               'B1': 0.5714285714285714,
               'RamaB5': 0.0}

    #values = [val_map.get(node, 0) for node in Grafo.nodes()]
    values = [color.get(node, 50) for node in Grafo.nodes()]
    # Color mapping
    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=max(values))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)


    f = plt.figure(1)
    ax = f.add_subplot(1,1,1)

    for label in val_map:
        ax.plot([0],[0],color=scalarMap.to_rgba(val_map[label]),label=label)
        

    #values = [val_map.get(node, 30) for node in Grafo.nodes()]

    f.set_facecolor('w')
    #plt.legend(loc='best')


    f.tight_layout()

    #nx.draw(Grafo, cmap=plt.get_cmap('jet'), node_color=values)

    ###se dibuja el grafo normal
    #nx.draw(Grafo,pos)
    
    ###se dibuja el grafo con etiquetas
    #nx.draw_networkx(Grafo,pos, arrows=True, with_labels=True,node_color=color)
    #nx.draw_networkx(Grafo,pos, arrows=True, with_labels=True,node_color=values)
    wins=dict.fromkeys(Grafo.nodes(),0.0)
    nodesize=[wins[v]*50 for v in Grafo]
    
    nx.draw_networkx_nodes(Grafo,pos,node_size=nodesize,node_color='r',alpha=0.4)

    nx.draw_networkx_labels(Grafo,pos,fontsize=14)
    #nx.draw_networkx_labels(Grafo,pos,labels)
    #nx.draw_networkx(Grafo,pos, arrows=False, with_labels=True,node_color=values,ax=ax)
    plt.savefig("GrafoCaminos.png")
    plt.axis('off')
    plt.show()


    
retorno=Grafos()
distancia=12
imprimible=punto_falla(retorno,distancia)
imprimir_grafo(imprimible)

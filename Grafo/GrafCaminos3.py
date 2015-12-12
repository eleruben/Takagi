import xlrd
import networkx as nx
import matplotlib.pyplot as plt

import matplotlib.colors as colors
import matplotlib.cm as cmx

##########################################################################
#                CODIGO PARA IMPLEMENTACION VERTICAL DE LOS NODOS        #
##########################################################################


#se extraen los valores del circuito de una tabla de excel
#libro = xlrd.open_workbook("C:\Users\Ricardo\Documents\deteccion de fallas/Modelo circuito.xls")

def Grafos():
    Ext1=[]
    Ext2=[]
    Distancia=[]
    libro = xlrd.open_workbook("C:\Users\NECSOFT\Desktop\deteccion de fallas\Modelo circuito.xlsX")
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
                #acumulado=nx.get_edge_attributes(Grafo,'acumulado')
                acumulado=nx.get_node_attributes(Grafo,'acumulado')
                pos=nx.get_node_attributes(Grafo,'pos')
                desviacion=0
                if Ext1[i] in Grafo.nodes() and Ext2[i] not in Grafo.nodes():
                    '''for n in Grafo.neighbors(Ext1[i]):
                        #Se elige cual de las configuraciones de claves tiene
                        #la conexion del nodo conectado al grafo
                        ##########################REVISAR YA QUE LOS VECINOS SON SECUENCIALES####
                        #if (n,Ext1[i]) in length.keys():
                        if (n,Ext1[i]) in length.keys():
                            temporal=length[n,Ext1[i]]
                            ac=acumulado[n,Ext1[i]]
                        else:
                            temporal=length[Ext1[i],n]
                            ac=acumulado[Ext1[i],n]
                        #Se elige el nodo que tenga menor acumuladovalor de longitud
                        if acumulado[Ext1[i]]temporal < longitud:
                            longitud=temporal'''
                    ##en el caso de las ramas se necesita conocer la posicion del
                    ##nodo al que esta asociado
                    print ("se va a agregar nodo EXT2 "+Ext2[i])
                    if len(Grafo.neighbors(Ext1[i]))==2:
                        #se necesita pos['B4'][0]
                        Grafo.add_node(Ext2[i],pos=(Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                        print("el nodo "+str(Ext1[i])+" tiene 2 vecinos")
                    if len(Grafo.neighbors(Ext1[i]))==3:
                        Grafo.add_node(Ext2[i],pos=(-Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                    if len(Grafo.neighbors(Ext1[i]))==1:

                        #################
                        print("el que esta conectado es: "+str(Ext1[i]))
                        Grafo.add_node(Ext2[i],pos=(desviacion,Distancia[i]+acumulado[Ext1[i]]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                    #Grafo.add_edge(Ext1[i],Ext2[i],length=Distancia[i], acumulado=Distancia[i]+ac)
                    Grafo.add_edge(Ext1[i],Ext2[i],length=Distancia[i])
                    break
                if Ext2[i] in Grafo.nodes() and Ext1[i] not in Grafo.nodes():
                    '''for n in Grafo.neighbors(Ext2[i]):
                        if (n,Ext2[i]) in length.keys():
                            temporal=length[n,Ext2[i]]
                            ac=acumulado[n,Ext2[i]]
                        else:
                            temporal=length[Ext2[i],n]
                            ac=acumulado[Ext2[i],n]
                        if temporal < longitud:
                            longitud=temporal'''
                    print ("se va a agregar nodo EXT1 "+Ext1[i])
                    if len(Grafo.neighbors(Ext2[i]))==2:
                        print("rama a distancia "+str(pos[Ext2[i]][0]))
                        Grafo.add_node(Ext1[i],pos=(Distancia[i],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                        print("el nodo "+str(Ext2[i])+" tiene 2 vecinos")
                    if len(Grafo.neighbors(Ext2[i]))==3:
                        Grafo.add_node(Ext1[i],pos=(-Distancia[i],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                    if len(Grafo.neighbors(Ext1[i]))==1:
                        Grafo.add_node(Ext1[i],pos=(desviacion,Distancia[i]+acumulado[Ext2[i]]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                
                    #Grafo.add_node(Ext1[i],pos=(Distancia[i]+ac,desviacion))
                    Grafo.add_edge(Ext1[i],Ext2[i],length=Distancia[i], acumulado=Distancia[i]+ac)
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
            print("longitudes "+str(length))
            print("posiciones "+str(pos))
            print("acumulados "+str(acumulado))
        
   
    #print("valor x de b4 "+str(pos['B4'][0]))
    #print("valor y de b4 "+str(pos['B4'][1]))
    #print("el acumulado de la distancia en la rama B4 es "+str(acumulado[('RamaB4','B4')]))
    pos=nx.get_node_attributes(Grafo,'pos')


    ###PRUEBA DE COLOR EN LOS GRAFOS
    val_map = {'B4': 1.0,
               'B1': 0.5714285714285714,
               'RamaB5': 0.0}

    values = [val_map.get(node, 0) for node in Grafo.nodes()]
    # Color mapping
    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=max(values))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)


    f = plt.figure(1)
    ax = f.add_subplot(1,1,1)

    for label in val_map:
        ax.plot([0],[0],color=scalarMap.to_rgba(val_map[label]),label=label)
        

    values = [val_map.get(node, 30) for node in Grafo.nodes()]

    f.set_facecolor('w')
    plt.legend(loc='best')


    f.tight_layout()

    #nx.draw(Grafo, cmap=plt.get_cmap('jet'), node_color=values)

    ###se dibuja el grafo normal
    #nx.draw(Grafo,pos)
    
    ###se dibuja el grafo con etiquetas
    #nx.draw_networkx(Grafo,pos=nx.spring_layout(Grafo), arrows=True, with_labels=True)
    nx.draw_networkx(Grafo,pos, arrows=False, with_labels=True,node_color=values,ax=ax)
    plt.savefig("GrafoCaminos.png")
    plt.axis('off')
    plt.show()
    return Grafo


    #nx.write_graphml(Grafo,'GrafoCaminos.graphml')
def punto_falla(Grafo,distancia):
    #Variable utilizada para verificar que la distancia ingresada se encuentra por dentro del circuito
    dentro=False
    lista_mayores=[]
    #Se extrae la lista de acumulados de todos los nodos para comparar la posible distancia a la que puede
    #localizarse la falla
    acumulado=nx.get_node_attributes(Grafo,'acumulado')
    for nodo in acumulado.keys():
        #Se revisa cual de los nodos tiene mayor distancia a la falla
        if acumulado[nodo]>distancia:
            dentro=True
            print("los nodos mayores son: "+str(nodo))
            lista_mayores.append(nodo)
    for i in range(len(lista_mayores)):
        for j in range(len(lista_mayores)):
            if not (i==j):
                lista1=nx.shortest_path (Grafo, 'B1', lista_mayores[i])
                lista2=nx.shortest_path (Grafo, 'B1', lista_mayores[j])
                print("la interseccion de "+str(lista_mayores[i])+" con "+str(lista_mayores[j]))
                print((set(lista1).intersection(lista2)))
            #Ciclo utilizado para recorrer los vecinos
                ##menores longitudes y que esten contenidos en otros
            ##tomar los menores y calcular comparar la distancia contra el acumulado del vecino????

            #for n in Grafo.neighbors(nodo)
        ####/////////////////////REVISAR CASO QUE LA DISTANCIA ESTE EN UN NODO    
    if not (dentro):
        print("la distancia ingresada en mayor que la mayor distancia del circuito")

        
    #Grafo.add_node(Ext1[i],pos=(Distancia[i],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])




    
retorno=Grafos()
distancia=21.5
punto_falla(retorno,distancia)

import xlrd
import networkx as nx
import matplotlib.pyplot as plt

import matplotlib.colors as colors
import matplotlib.cm as cmx
import os

import sqlite3 as sq3

##########################################################################
#                CODIGO PARA IMPLEMENTACION VERTICAL DE LOS NODOS        #
##########################################################################

class claseCircuito(object):
    
    def __init__(self, nombre):
        base_datos=nombre+".s3db"
        """ Establece la conexion con la base de datos
        y ejecuta las consultas solicitadas en la interfaz.
        Si no existe la tabla, la crea.
        Inserta datos de prueba """
        base = os.path.exists(base_datos)
        conexion = sq3.connect(base_datos)
        self.cursor = conexion.cursor()
        self.Grafos()
    
    def Grafos(self):
        
       
        
        self.cursor.execute('''DROP VIEW IF EXISTS X;''')
        self.cursor.execute('''
            CREATE VIEW X AS SELECT Nombre,Troncal,DISTANCIA,R0,R1,X0,X1  
            FROM Nodos a, Lineas b  
            WHERE a.Id_Nodo=b.Id_Nodo1;''')        
        self.cursor.execute("SELECT * FROM X;")
        registros = self.cursor.fetchall()
        Ext1=[]
        Ext2=[]
        Troncal=[]
        Distancia=[]
        tablaR0=[]
        tablaR1=[]
        tablaX0=[]
        tablaX1=[]
        ####Es necesaria la equivalencia de los nombres con el identificador del nodo???REVISAR
        for i in range(len(registros)):
            Ext2.append(str(registros[i][0]))            
            Troncal.append(registros[i][1])
            Distancia.append(registros[i][2])
            tablaR0.append(registros[i][3])
            tablaR1.append(registros[i][4])
            tablaX0.append(registros[i][5])
            tablaX1.append(registros[i][6])
        
        self.cursor.execute('''DROP VIEW IF EXISTS Y;''')
        self.cursor.execute('''
            CREATE VIEW Y AS SELECT Nombre
            FROM Nodos a, Lineas b  
            WHERE a.Id_Nodo=b.Id_Nodo2;''')        
        self.cursor.execute("SELECT * FROM Y;")
        registros = self.cursor.fetchall()
        for i in range(len(registros)):
            Ext1.append(str(registros[i][0]))            
                    
        '''print('Ext1'+str(Ext1))
        print('Ext2'+str(Ext2))
        print('Distancia'+str(Distancia))
        print('Troncal'+str(Troncal))'''
        
        
        '''#Abre el archivo de excel en donde esta el modelo del circuito, este archivo debe estar
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
                if i==3 and j!=0: Distancia.append(pest.cell_value(rowx=j, colx=i))'''
        #se crea el grafo y se define el tipo de dato que va a ser
        Grafo = nx.Graph()
        #se recorre todo la lista de los datos de la primera columna
        for i in range(len(Ext1)):
            #Caso en el que se adicionan los dos primeros nodos y se establece un
            #camino entre ellos
            if i==0:
                Grafo.add_node(Ext1[i],pos=(0,0),acumulado=0,troncal=Troncal[0])
                Grafo.add_node(Ext2[i],pos=(0,Distancia[i]),acumulado=Distancia[i],troncal=Troncal[0])
                Grafo.add_edge(Ext1[i],Ext2[i],length=Distancia[i],R0=tablaR0[i],R1=tablaR1[i],X0=tablaX0[i],X1=tablaX1[i])
    
            else:
                #Es necesario conocer cual de los nodos ya esta agregado al grafo y continuar
                #el camino, en el caso de los ramales es necesario conocer la arista del nodo
                #que conduzca al origen, para asi poder calcular el acumulado de la distancia
                #al ramal
                for j in range(len(Grafo.nodes())):
                    #se verifica que la arista que se va a agregar este conectada al ramal
                    #por solo uno de sus nodos
                    
                    #Acumulado es un atributo del nodo que se obtiene de sumar todos las longitudes
                    #del trayecto al nodo origen
                    acumulado=nx.get_node_attributes(Grafo,'acumulado')
                    pos=nx.get_node_attributes(Grafo,'pos')
                    troncal=nx.get_node_attributes(Grafo,'troncal')
                    R0=nx.get_node_attributes(Grafo,'R0')
                    R1=nx.get_node_attributes(Grafo,'R1')
                    X0=nx.get_node_attributes(Grafo,'X0')
                    X1=nx.get_node_attributes(Grafo,'X1')
                    desviacion=0
                    ##Se evaluan los dos caso para descartar que se agregue el nodo el diferente orden
                    if Ext1[i] in Grafo.nodes() and Ext2[i] not in Grafo.nodes():
                        ##En el caso de las ramas se necesita conocer la posicion del
                        ##nodo al que esta asociado
    
                        if len(Grafo.neighbors(Ext1[i]))==2:
                            #Caso en que se agrega una rama estando dos en linea en la linea base #0
                            if(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]==0) and (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0] == 0):
                                Grafo.add_node(Ext2[i],pos=(Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i],troncal=Troncal[i])
                            #Caso en que se agrega una nueva rama a la izquierda #1
                            elif((pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]<0) or (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0]<0)) and (troncal[Ext1[i]]==0):
                                Grafo.add_node(Ext2[i],pos=(-Distancia[i]+pos[Ext1[i]][0],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i],troncal=Troncal[i])
                            #Caso en que se agrega una nueva rama a la derecha #2
                            elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]>0) or (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0]>0):
                                Grafo.add_node(Ext2[i],pos=(Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i],troncal=Troncal[i])
                            #Caso en que se agrega una troncal a la linea base habiendo agregado antes una rama
                            elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]==0) and (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0]<0):
                                Grafo.add_node(Ext2[i],pos=(Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i],troncal=Troncal[i])
                            #elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0]==0) and (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]<0):
                            elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0]==0) and troncal[Ext1[i]]==1:
                                Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],Distancia[i]+pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i],troncal=Troncal[i])
    
                        if len(Grafo.neighbors(Ext1[i]))==3:
                            
                            #Caso en que se agrega una nueva rama a la izquierda, los nodos alineados en Y son 1 y 2 #0
                            if(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]==0) and (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0] == 0):
                                Grafo.add_node(Ext2[i],pos=(-Distancia[i]+pos[Ext1[i]][0],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                            #Caso en que se agrega una nueva rama a la izquierda, los nodos alineados en Y son 2 y 3 #0
                            elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[1]][0]==0) and (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[2]][0] == 0):
                                Grafo.add_node(Ext2[i],pos=(-Distancia[i]+pos[Ext1[i]][0],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                            #Caso en que se agrega una nueva rama a la izquierda, los nodos alineados en Y son 1 y 3 #0
                            elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]==0) and (pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[2]][0] == 0):
                                Grafo.add_node(Ext2[i],pos=(-Distancia[i]+pos[Ext1[i]][0],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                            #Caso en que se agrega una nueva rama abajo, los nodos alineados en X son 1 y 2 #1
                            elif(pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[0]][1]==0) and (pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[1]][1] == 0):
                                Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],pos[Ext1[i]][1]-Distancia[i]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                            #Caso en que se agrega una nueva rama abajo, los nodos alineados en X son 2 y 3 #1
                            elif(pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[1]][1]==0) and (pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[2]][1] == 0):
                                Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],pos[Ext1[i]][1]-Distancia[i]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                            #Caso en que se agrega una nueva rama abajo, los nodos alineados en X son 1 y 3 #1
                            elif(pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[0]][1]==0) and (pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[2]][1] == 0):
                                Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],pos[Ext1[i]][1]-Distancia[i]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                            
                        if len(Grafo.neighbors(Ext1[i]))==1:
                            
                            #Caso en que el vecino este agregado por abajo, se agrega hacia arriba #0
                            if(pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[0]][1]>0):
                                #Caso en que se este agregando una rama a un nodo troncal, se agrega por la derecha 
                                if(Troncal[i] == 0):
                                    Grafo.add_node(Ext2[i],pos=(Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i],troncal=Troncal[i])
                                elif(Troncal[i] == 1):
                                    Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],Distancia[i]+pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i],troncal=Troncal[i])
                            #Caso en que el vecino este agregado por arriba, se agrega por la izquierda #1
                            elif(pos[Ext1[i]][1]-pos[Grafo.neighbors(Ext1[i])[0]][1]<0):
                                Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0]+Distancia[i],pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                            #Caso en que el vecino este agregado por izquierda, se agrega hacia arriba #2
                            elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]<0):
                                Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],Distancia[i]+pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])
                            #Caso en que el vecino este agregado por derecha, se agrega hacia arriba #3
                            elif(pos[Ext1[i]][0]-pos[Grafo.neighbors(Ext1[i])[0]][0]>0):
                                Grafo.add_node(Ext2[i],pos=(pos[Ext1[i]][0],Distancia[i]+pos[Ext1[i]][1]),acumulado=acumulado[Ext1[i]]+Distancia[i])                            
         
                        Grafo.add_edge(Ext1[i],Ext2[i],length=Distancia[i],R0=tablaR0[i],R1=tablaR1[i],X0=tablaX0[i],X1=tablaX1[i])
                        break
    
                    '''if Ext2[i] in Grafo.nodes() and Ext1[i] not in Grafo.nodes():
    
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
                            
                            #Caso en que se agrega una nueva rama a la izquierda, los nodos alineados en Y son 1 y 2 #0
                            if(pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[0]][0]==0) and (pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[1]][0] == 0):
                                Grafo.add_node(Ext1[i],pos=(-Distancia[i]+pos[Ext2[i]][0],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                            #Caso en que se agrega una nueva rama a la izquierda, los nodos alineados en Y son 2 y 3 #0
                            elif(pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[1]][0]==0) and (pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[2]][0] == 0):
                                Grafo.add_node(Ext1[i],pos=(-Distancia[i]+pos[Ext2[i]][0],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                            #Caso en que se agrega una nueva rama a la izquierda, los nodos alineados en Y son 1 y 3 #0
                            elif(pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[0]][0]==0) and (pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[2]][0] == 0):
                                Grafo.add_node(Ext1[i],pos=(-Distancia[i]+pos[Ext2[i]][0],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                            #Caso en que se agrega una nueva rama abajo, los nodos alineados en X son 1 y 2 #1
                            elif(pos[Ext2[i]][1]-pos[Grafo.neighbors(Ext2[i])[0]][1]==0) and (pos[Ext2[i]][1]-pos[Grafo.neighbors(Ext2[i])[1]][1] == 0):
                                Grafo.add_node(Ext1[i],pos=(pos[Ext2[i]][0],pos[Ext2[i]][1]-Distancia[i]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                            #Caso en que se agrega una nueva rama abajo, los nodos alineados en X son 2 y 3 #1
                            elif(pos[Ext2[i]][1]-pos[Grafo.neighbors(Ext2[i])[1]][1]==0) and (pos[Ext2[i]][1]-pos[Grafo.neighbors(Ext2[i])[2]][1] == 0):
                                Grafo.add_node(Ext1[i],pos=(pos[Ext2[i]][0],pos[Ext2[i]][1]-Distancia[i]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                            #Caso en que se agrega una nueva rama abajo, los nodos alineados en X son 1 y 3 #1
                            elif(pos[Ext2[i]][1]-pos[Grafo.neighbors(Ext2[i])[0]][1]==0) and (pos[Ext2[i]][1]-pos[Grafo.neighbors(Ext2[i])[2]][1] == 0):
                                Grafo.add_node(Ext1[i],pos=(pos[Ext2[i]][0],pos[Ext2[i]][1]-Distancia[i]),acumulado=acumulado[Ext2[i]]+Distancia[i])
    
                        if len(Grafo.neighbors(Ext2[i]))==1:
    
                            #Caso en que el vecino este agregado por abajo, se agrega hacia arriba #0
                            if(pos[Ext2[i]][1]-pos[Grafo.neighbors(Ext2[i])[0]][1]>0):
                                Grafo.add_node(Ext1[i],pos=(pos[Ext2[i]][0],Distancia[i]+pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                                print('se agrega Ext1'+str(Ext1[i]))
                            #Caso en que el vecino este agregado por arriba, se agrega por la izquierda #1
                            elif(pos[Ext2[i]][1]-pos[Grafo.neighbors(Ext2[i])[0]][1]<0):
                                Grafo.add_node(Ext1[i],pos=(pos[Ext2[i]][0]+Distancia[i],pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                            #Caso en que el vecino este agregado por izquierda, se agrega hacia arriba #2
                            elif(pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[0]][0]<0):
                                Grafo.add_node(Ext1[i],pos=(pos[Ext2[i]][0],Distancia[i]+pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])
                            #Caso en que el vecino este agregado por derecha, se agrega hacia arriba #3
                            elif(pos[Ext2[i]][0]-pos[Grafo.neighbors(Ext2[i])[0]][0]>0):
                                Grafo.add_node(Ext1[i],pos=(pos[Ext2[i]][0],Distancia[i]+pos[Ext2[i]][1]),acumulado=acumulado[Ext2[i]]+Distancia[i])                            
    
                        Grafo.add_edge(Ext1[i],Ext2[i],length=Distancia[i])
                        break'''
    
        return Grafo
    
    
    ##Funcion en la cual se ubican los puntos de falla dependiendo de su distancia
    ##al nodo origen
    def punto_falla(self,Grafo,distancia):
        
        #Variable utilizada para verificar que la distancia ingresada se encuentra por dentro del circuito
        afuera=True
        color=nx.get_node_attributes(Grafo,'color')
        acumulado=nx.get_node_attributes(Grafo,'acumulado')
        pos=nx.get_node_attributes(Grafo,'pos')
        troncal=nx.get_node_attributes(Grafo,'troncal')
        #Se extrae la lista de acumulados de todos los nodos para comparar la posible distancia a la que puede
        #localizarse la falla
        for nodo in acumulado.keys():
            if(acumulado[nodo]==distancia):
                Grafo.add_node('Falla'+str(nodo),pos=(pos[nodo][0],pos[nodo][1]),acumulado=distancia,color=4.0)
                #color[nodo]='b'
                #print("los colores son :"+str(color))
            
            #Se revisa cual de los nodos tiene mayor distancia a la falla
            if acumulado[nodo]<distancia:
                for n in Grafo.neighbors(nodo):
                    #Entra cuando la distancia se encuentre en esta arista
                    if acumulado[n]>distancia:
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
    
    
    def imprimir_grafo(self,Grafo):
        pos=nx.get_node_attributes(Grafo,'pos')
        #print("las posiciones son "+str(pos))
        etiquetas={}
        for n in pos.keys():
            #print(str(n)+" tiene "+str(pos[n][0]))
            etiquetas[n]=[pos[n][0]+0.5,pos[n][1]+0.5]
        #print("la posicion de las etiquetas son "+str(etiquetas))
            
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
        
        nx.draw_networkx_nodes(Grafo,pos,node_size=100,node_color=values,alpha=1.0)
        nx.draw_networkx_edges(Grafo,pos,alpha=0.4,node_size=0,width=1,edge_color='k')
        nx.draw_networkx_labels(Grafo,etiquetas,fontsize=14)
        ax.set_title('Click to zoom')
        #nx.draw_networkx_labels(Grafo,pos,labels)
        #nx.draw_networkx(Grafo,pos, arrows=False, with_labels=True,node_color=values,ax=ax)
        
        #plt.savefig("GrafoCaminos.png")
        #plt.axis('off')
        plt.show()
    
        
        
    #retorno=Grafos()
    #distancia=13
    #imprimible=punto_falla(retorno,distancia)
    #imprimir_grafo(imprimible)

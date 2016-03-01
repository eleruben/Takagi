import sqlite3 as sq3
import os
import yacopi

class baseDatos(object):
    #Constructor de clase base de datos
    def __init__(self, nombre):        
        base_datos=nombre+".s3db"
        """ Establece la conexion con la base de datos
        y ejecuta las consultas solicitadas en la interfaz.
        Si no existe la tabla, la crea.
        Inserta datos de prueba """
        base = os.path.exists(base_datos)
        conexion = sq3.connect(base_datos)
        self.cursor = conexion.cursor()
        
    
    def tablaNodos(self):
        sql="SELECT Nombre FROM Nodos"
        self.cursor.execute(sql)
        registros = self.cursor.fetchall()
        
        Ext1=[]
        for i in range(len(registros)):
            Ext1.append(str(registros[i][0]))
          
        return Ext1
    
    def consultaId(self,nombre):
        self.cursor.execute('''SELECT Id_Nodo FROM Nodos WHERE Nombre=?;''', (str(nombre),))
        registros = str(self.cursor.fetchone())
        registros=registros.lstrip('(')
        registros=registros.rstrip(')')
        registros=registros.rstrip(',')
        return registros
    
    def consultaNodo(self,nombre):
        
        #sql='''SELECT Nombre,Troncal FROM Nodos WHERE Id_Nodo=?;''', (str(nombre),)
        #self.cursor.execute(sql,nombre)
        self.cursor.execute('''SELECT Nombre,Troncal FROM Nodos WHERE Nombre=?;''', (str(nombre),))
        registros = self.cursor.fetchall()
        return registros
    
    def consultaLineas(self,nombre):
        #primero consultar el nombre del nodo y ponerlo en la consulta
        #sql='''SELECT Id_Nodo1,R0,R1,X0,X1,DISTANCIA FROM Lineas WHERE Id_Nodo2=?;''', (str(nombre),)
        
        
        self.cursor.execute('''SELECT Id_Nodo FROM Nodos WHERE Nombre=?;''', (str(nombre),))
        nombre=str(self.cursor.fetchone())
        nombre=nombre.lstrip('(')
        nombre=nombre.rstrip(')')
        nombre=nombre.rstrip(',')
        self.cursor.execute('''DROP VIEW IF EXISTS aa;''')
        self.cursor.execute('''
        CREATE VIEW aa AS SELECT Id_Nodo2,Nombre,R0,R1,X0,X1,DISTANCIA  
        FROM Nodos a, Lineas b  
        WHERE a.Id_Nodo=b.Id_Nodo1''')
        self.cursor.execute("SELECT Nombre,R0,R1,X0,X1,DISTANCIA FROM aa WHERE Id_Nodo2=?;", (str(nombre),))
        #self.cursor.execute("SELECT Nombre,R0,R1,X0,X1,DISTANCIA FROM aa")
        registros = self.cursor.fetchall()
        return registros
    
    def consultaCargas(self,nombre):
        #sql='''SELECT ALIAS,P,Q FROM Cargas WHERE Id_Nodo=?;''', (str(nombre),)
        self.cursor.execute('''SELECT Id_Nodo FROM Nodos WHERE Nombre=?;''', (str(nombre),))
        nombre=str(self.cursor.fetchone())
        nombre=nombre.lstrip('(')
        nombre=nombre.rstrip(')')
        nombre=nombre.rstrip(',')
        
        self.cursor.execute('''SELECT ALIAS,P,Q FROM Cargas WHERE Id_Nodo=?;''', (str(nombre),))
        registros = self.cursor.fetchall()
        return registros
    
    def consultaVecinos(self,nombre):
        #primero consultar el nombre del nodo y ponerlo en la consulta
        #sql='''SELECT Id_Nodo1,R0,R1,X0,X1,DISTANCIA FROM Lineas WHERE Id_Nodo2=?;''', (str(nombre),)
        
        
        self.cursor.execute('''SELECT Id_Nodo FROM Nodos WHERE Nombre=?;''', (str(nombre),))
        nombre=str(self.cursor.fetchone())
        nombre=nombre.lstrip('(')
        nombre=nombre.rstrip(')')
        nombre=nombre.rstrip(',')
        self.cursor.execute('''DROP VIEW IF EXISTS aa;''')
        self.cursor.execute('''
        CREATE VIEW aa AS SELECT Id_Nodo2,Nombre,R0,R1,X0,X1,DISTANCIA  
        FROM Nodos a, Lineas b  
        WHERE a.Id_Nodo=b.Id_Nodo1''')
        self.cursor.execute("SELECT Nombre FROM aa WHERE Id_Nodo2=?;", (str(nombre),))
        registros = self.cursor.fetchall()
        
        Ext1=[]
        for i in range(len(registros)):
            Ext1.append(str(registros[i][0]))
        return Ext1
    
    def consultaTablaNodos(self,tabla):
        sql="SELECT * FROM Nodos"
        self.cursor.execute(sql)
        registros = self.cursor.fetchall()
        for i in registros:
            tabla.append([i[0],str(i[1]),i[2]])
        #print (registros)
        return tabla
    
    def consultaTablaLineas(self,tabla):
        
        TaLineas = [["ID", "Nombre", "Nodo1", "Nodo2", "R0", "R1", "L0", "L1", "Distancia"]]
        sql="SELECT * FROM Lineas"
        self.cursor.execute(sql)
        registros = self.cursor.fetchall()
        for i in registros:
            tabla.append([i[0],'a',i[2],i[1],i[3],i[4],i[5],i[6],i[7]])
            print([i[0],'',i[2],i[1],i[3],i[4],i[5],i[6],i[7]])
        #print (registros)
        return tabla
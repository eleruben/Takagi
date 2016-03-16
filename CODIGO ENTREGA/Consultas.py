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
        return tabla
    
    def consultaTablaLineas(self,tabla):
        
        
        sql="SELECT * FROM Lineas"
        self.cursor.execute(sql)
        registros = self.cursor.fetchall()
        for i in registros:
            tabla.append([i[0],'Linea'+str(i[0]),i[2],i[1],i[3],i[4],i[5],i[6],i[7]])
        return tabla
    
    def consultaTablaCargas(self,tabla):
        
        TaCargas = [["ID", "Nodo", "Nombre", "P", "Q"]]
        sql="SELECT * FROM Cargas"
        self.cursor.execute(sql)
        registros = self.cursor.fetchall()
        for i in registros:
            tabla.append([i[0],i[1],str(i[2]),i[3],i[4]])
        return tabla
    
    def consultaTablaIndicadores(self,tabla):
        
        TaIndicadores = [["ID", "Nombre", "Nodo1", "Nodo2", "Distancia"]]
        sql="SELECT * FROM Indicadores"
        self.cursor.execute(sql)
        registros = self.cursor.fetchall()
        for i in registros:
            tabla.append([i[0],str(i[3]),i[1],i[2],i[4]])
        return tabla
    
    def consultaIdIndicadores(self,nombre):
        self.cursor.execute('''SELECT Id_indicador FROM Indicadores WHERE Nombre=?;''', (str(nombre),))
        registros = str(self.cursor.fetchone())
        registros=registros.lstrip('(')
        registros=registros.rstrip(')')
        registros=registros.rstrip(',')
        return registros
    
    
    def consultaIndicadores(self):
        sql="SELECT NOMBRE FROM Indicadores"
        self.cursor.execute(sql)
        registros = self.cursor.fetchall()
        
        Ext1=[]
        for i in range(len(registros)):
            Ext1.append(str(registros[i][0]))
        return Ext1
    
    def consultaNodos1Indicadores(self):
        
        self.cursor.execute('''DROP VIEW IF EXISTS ind;''')
        self.cursor.execute('''
        CREATE VIEW ind AS SELECT Id_Nodo2,Nombre  
        FROM Nodos a, Lineas b  
        WHERE a.Id_Nodo=b.Id_Nodo2''')
        self.cursor.execute("SELECT Nombre FROM ind;")
        registros = self.cursor.fetchall()
        
        Ext1=[]
        for i in range(len(registros)):
            if str(registros[i][0]) not in Ext1:
                Ext1.append(str(registros[i][0]))
        return Ext1
    
    
    def consultaNodos2Indicadores(self,nodo):
        
        self.cursor.execute('''DROP VIEW IF EXISTS vecino;''')
        self.cursor.execute('''
        CREATE VIEW vecino AS SELECT Id_Nodo1,Id_Nodo2,Nombre  
        FROM Nodos a, Lineas b  
        WHERE a.Id_Nodo=b.Id_Nodo1''')
        self.cursor.execute("SELECT Nombre FROM vecino WHERE Id_Nodo2=?;", (str(nodo),))
        registros = self.cursor.fetchall()
        
        Ext1=[]
        for i in range(len(registros)):
            if str(registros[i][0]) not in Ext1:
                Ext1.append(str(registros[i][0]))
        return Ext1
        
    
    
import sqlite3 as sq3
import os
import wx
 
class Modelo(object):
    def __init__(self, base_datos="yacopi.s3db"):
        """ Establece la conexion con la base de datos
        y ejecuta las consultas solicitadas en la interfaz.
        Si no existe la tabla, la crea.
        Inserta datos de prueba """
        base = os.path.exists(base_datos)
        self.conexion = sq3.connect(base_datos)
        if not base:
            self.crearTabla()
 
    def insertar(self, d1):
        """ Inserta un nuevo registro en la base de datos
        y retorna la nueva clave primaria asignada
        automaticamente por SQLite. el parametro d1
        debe contener los valores de las columna codigo
        descripcion y valor. """
        cursor = self.conexion.cursor()
        N=[d1[0],d1[1]]
        sql = '''INSERT INTO Nodos (Nombre, Troncal) VALUES (?, ?);'''
        cursor.execute(sql, N)
        nuevaID = cursor.lastrowid
        L=[d1[2],d1[3],d1[4],d1[5],d1[6],d1[7],nuevaID]
        sql = '''UPDATE Lineas set Id_Nodo2 = ?, R0 =?, R1 =?, X0 =?,X1 =?, DISTANCIA = ?  where Id_Nodo1=?;'''
        cursor.execute(sql, L)
        C=[d1[9],d1[10],nuevaID]
        sql = '''UPDATE Cargas set POTENCIA=?, FACTOR=?  where Id_Nodo=?;'''
        cursor.execute(sql, C)
        self.conexion.commit()
        cursor.close()
        return nuevaID
 
    def actualizar(self, d2):
        """ Actualiza los datos de un registro existente.
        Es necesario proporcionar la id del registro
        junto con los valores de las otras columnas
        en el parametro d2. """
        cursor = self.conexion.cursor()
        N=[d2[0],d2[1],d2[11]]
        sql = '''UPDATE Nodos set Nombre=?, Troncal=? where Id_Nodo=?;'''
        cursor.execute(sql, N)
        L=[d2[2],d2[3],d2[4],d2[5],d2[6],d2[7],d2[11]]
        sql = '''UPDATE Lineas set Id_Nodo2 = ?, R0 =?, R1 =?, X0 =?,X1 =?, DISTANCIA = ?  where Id_Nodo1=?;'''
        cursor.execute(sql, L)
        C=[d2[9],d2[10],d2[11]]
        sql = '''UPDATE Cargas set POTENCIA=?, FACTOR=?  where Id_Nodo=?;'''
        cursor.execute(sql, C)
        self.conexion.commit()
        cursor.close()
 
    def seleccionar(self, id=None):
        """ Selecciona registros en la base de datos """
        cursor = self.conexion.cursor()
        #sql1 = ' SELECT * FROM productos '
        #sql1 = ' SELECT * FROM Nodos '
        sql1 = '''CREATE VIEW IF NOT EXISTS h AS SELECT Id_Nodo1,Nombre, Troncal, Id_Nodo2,R0,R1,X0,X1,DISTANCIA,ALIAS,POTENCIA,FACTOR  
        FROM Nodos a, Lineas b, Cargas c  
        WHERE a.Id_Nodo=b.Id_Nodo1  
        AND a.Id_Nodo=c.Id_Nodo; '''
        
        sql2 = '''CREATE VIEW IF NOT EXISTS h AS SELECT Id_Nodo1,Nombre, Troncal, Id_Nodo2,R0,R1,X0,X1,DISTANCIA,ALIAS,POTENCIA,FACTOR  
        FROM Nodos a, Lineas b, Cargas c  
        WHERE a.Id_Nodo=b.Id_Nodo1  
        AND a.Id_Nodo=c.Id_Nodo
        AND a.Id_Nodo=?; '''
        if not id:
            cursor.execute(sql1)
            cursor.execute("SELECT * FROM h")
        else:
            #cursor.execute(sql2, (id,))
            cursor.execute(sql1)
            cursor.execute("SELECT * FROM h where Id_Nodo1=?;",(id,))
        registros = cursor.fetchall() # recupera todos los registros    
        cursor.close()
        return registros
 
    def eliminar(self, id):
        """ Elimina un registro de la base de datos """
        cursor = self.conexion.cursor()
        sql = '''DELETE FROM Nodos WHERE Id_Nodo=?;'''
        cursor.execute(sql, (id,))
        sql = '''DELETE FROM Lineas WHERE Id_Nodo1=?;'''
        cursor.execute(sql, (id,))
        sql = '''DELETE FROM Cargas WHERE Id_Nodo=?;''' 
        cursor.execute(sql, (id,))
        self.conexion.commit()
        cursor.close()
 
    def ejecutar_script(self,sql):
        """ Ejecuta varias sentencia SQL, sin retornar algun valor"""
        cursor = self.conexion.cursor()
        cursor.executescript(sql)
        self.conexion.commit()
        cursor.close()
        #cursor.Close
 
    def crearTabla(self):
        
        sql='''create table if not exists Nodos 
        (Id_Nodo INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Troncal INTEGER NOT NULL);
        
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B1', 1);
        
        create table if not exists Lineas
        (Id_linea INTEGER PRIMARY KEY AUTOINCREMENT,
        Id_Nodo1 INTEGER,
        Id_Nodo2 INTEGER,
        R0 FLOAT,
        R1 FLOAT,
        X0 FLOAT,
        X1 FLOAT,
        DISTANCIA FLOAT);
        
        create table if not exists Cargas
        (Id_carga INTEGER PRIMARY KEY AUTOINCREMENT,
        Id_Nodo INTEGER NOT NULL,
        ALIAS TEXT,
        POTENCIA TEXT,
        FACTOR TEXT);
        
        CREATE TRIGGER relacion_nodo_linea AFTER INSERT ON Nodos
        BEGIN
        INSERT INTO Lineas (Id_Nodo1) VALUES (new.Id_Nodo);
        END;
        
        CREATE TRIGGER relacion_nodo_carga AFTER INSERT ON Nodos
        BEGIN
        INSERT INTO Cargas (Id_Nodo,ALIAS) VALUES (new.Id_Nodo,new.Nombre);
        END;
        
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B2', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B3', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B4', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B5', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B6', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B7', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B8', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B9', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B10', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B11', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB2', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB3', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB4', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB5', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB6', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB7', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB8', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB9', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB10', 0);
        
        UPDATE Lineas set Id_Nodo2 = 1, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 0.26386  where Id_Nodo1=2;
        UPDATE Lineas set Id_Nodo2 = 2, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 9.910026  where Id_Nodo1=3;
        UPDATE Lineas set Id_Nodo2 = 3, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 3.09144  where Id_Nodo1=4;
        UPDATE Lineas set Id_Nodo2 = 4, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 7.97976  where Id_Nodo1=5;
        UPDATE Lineas set Id_Nodo2 = 5, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 2.97622  where Id_Nodo1=6;
        UPDATE Lineas set Id_Nodo2 = 6, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 3.41433  where Id_Nodo1=7;
        UPDATE Lineas set Id_Nodo2 = 7, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 1.495  where Id_Nodo1=8;
        UPDATE Lineas set Id_Nodo2 = 8, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 4.41558  where Id_Nodo1=9;
        UPDATE Lineas set Id_Nodo2 = 9, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 3.73037 where Id_Nodo1=10;
        UPDATE Lineas set Id_Nodo2 = 10, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 10.41391  where Id_Nodo1=11;
        UPDATE Lineas set Id_Nodo2 = 2, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 4.30171  where Id_Nodo1=12;
        UPDATE Lineas set Id_Nodo2 = 3, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 7.695292  where Id_Nodo1=13;
        UPDATE Lineas set Id_Nodo2 = 4, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 4.39497  where Id_Nodo1=14;
        UPDATE Lineas set Id_Nodo2 = 5, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 3.89705  where Id_Nodo1=15;
        UPDATE Lineas set Id_Nodo2 = 6, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 8.025209  where Id_Nodo1=16;
        UPDATE Lineas set Id_Nodo2 = 7, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 3.99747  where Id_Nodo1=17;
        UPDATE Lineas set Id_Nodo2 = 8, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 5.70753  where Id_Nodo1=18;
        UPDATE Lineas set Id_Nodo2 = 9, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 10.31599  where Id_Nodo1=19;
        UPDATE Lineas set Id_Nodo2 = 10, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 7.45101  where Id_Nodo1=20;
        
        UPDATE Cargas set POTENCIA='PB2', FACTOR='FB2'  where Id_Nodo=2;
        UPDATE Cargas set POTENCIA='PB3', FACTOR='FB3'  where Id_Nodo=3;
        UPDATE Cargas set POTENCIA='PB4', FACTOR='FB4'  where Id_Nodo=4;
        UPDATE Cargas set POTENCIA='PB5', FACTOR='FB5'  where Id_Nodo=5;
        UPDATE Cargas set POTENCIA='PB6', FACTOR='FB6'  where Id_Nodo=6;
        UPDATE Cargas set POTENCIA='PB7', FACTOR='FB7'  where Id_Nodo=7;
        UPDATE Cargas set POTENCIA='PB8', FACTOR='FB8'  where Id_Nodo=8;
        UPDATE Cargas set POTENCIA='PB9', FACTOR='FB9'  where Id_Nodo=9;
        UPDATE Cargas set POTENCIA='PB10', FACTOR='FB10'  where Id_Nodo=10;
        UPDATE Cargas set POTENCIA='PB11', FACTOR='FB11'  where Id_Nodo=11;
        UPDATE Cargas set POTENCIA='PRB2', FACTOR='FRB2'  where Id_Nodo=12;
        UPDATE Cargas set POTENCIA='PRB3', FACTOR='FRB3'  where Id_Nodo=13;
        UPDATE Cargas set POTENCIA='PRB4', FACTOR='FRB4'  where Id_Nodo=14;
        UPDATE Cargas set POTENCIA='PRB5', FACTOR='FRB5'  where Id_Nodo=15;
        UPDATE Cargas set POTENCIA='PRB6', FACTOR='FRB6'  where Id_Nodo=16;
        UPDATE Cargas set POTENCIA='PRB7', FACTOR='FRB7'  where Id_Nodo=17;
        UPDATE Cargas set POTENCIA='PRB8', FACTOR='FRB8'  where Id_Nodo=18;
        UPDATE Cargas set POTENCIA='PRB9', FACTOR='FRB9'  where Id_Nodo=19;
        UPDATE Cargas set POTENCIA='PRB10', FACTOR='FRB10'  where Id_Nodo=20;    
        
            
        '''
        print( 'lo llama')

        self.ejecutar_script(sql)
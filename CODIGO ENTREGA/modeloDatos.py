import sqlite3 as sq3
import os
import wx
 
class Modelo(object):    
    def __init__(self, nombre,tipo):
        base_datos=nombre+".s3db"
        """ Establece la conexion con la base de datos
        y ejecuta las consultas solicitadas en la interfaz.
        Si no existe la tabla, la crea.
        Inserta datos de prueba """
        
        #Variable tipo puede tomar 3 valores, 
        #tipo=0; cuando se crea un circuito en blanco (solo dos nodos conectados, b1 y b2)
        #tipo=1; cuanto se crea el circuito de yacopi
        #tipo=2; cuanto se crea el circuito del modelo de matlab
        if tipo==0:
            base = os.path.exists(base_datos)
            self.conexion = sq3.connect(base_datos)
            if not base:
                self.crearTabla()
                self.autollenadoNueva()
        elif tipo==1:
            base = os.path.exists(base_datos)
            self.conexion = sq3.connect(base_datos)
            if not base:
                self.crearTabla()
                self.autollenadoYacopi()
            
        elif tipo==2:
            base = os.path.exists(base_datos)
            self.conexion = sq3.connect(base_datos)
            if not base:
                self.crearTabla()
                self.autollenadoPrueba()
 
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
        sql = '''UPDATE Cargas set P=?, Q=?  where Id_Nodo=?;'''
        cursor.execute(sql, C)
        self.conexion.commit()
        cursor.close()
        return nuevaID
    
    def actualizar(self, d2,Normal):
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
        C=[d2[8],d2[9],d2[10],d2[11]] 
        if d2[8]!=None:
            if Normal:
                sql = '''UPDATE Cargas set ALIAS=?, P=?, Q=?  where Id_Nodo=?;'''
                cursor.execute(sql, C)
            else:
                C=[d2[8],d2[9],d2[10],d2[2]] 
                sql = '''UPDATE Cargas set ALIAS=?, P=?, Q=?  where Id_Nodo=?;'''
                cursor.execute(sql, C)
        self.conexion.commit()
        cursor.close()
 
    def seleccionar(self, id=None):
        """ Selecciona registros en la base de datos """
        cursor = self.conexion.cursor()
        #sql1 = ' SELECT * FROM productos '
        #sql1 = ' SELECT * FROM Nodos '
        sql1 = '''CREATE VIEW IF NOT EXISTS h AS SELECT Id_Nodo1,Nombre, Troncal, Id_Nodo2,R0,R1,X0,X1,DISTANCIA,ALIAS,P,Q  
        FROM Nodos a, Lineas b, Cargas c  
        WHERE a.Id_Nodo=b.Id_Nodo1  
        AND a.Id_Nodo=c.Id_Nodo; '''
        
        sql2 = '''CREATE VIEW IF NOT EXISTS h AS SELECT Id_Nodo1,Nombre, Troncal, Id_Nodo2,R0,R1,X0,X1,DISTANCIA,ALIAS,P,Q  
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
        
        
        
    def insertarIndicador(self, d1):
        """ Inserta un nuevo registro en la base de datos
        en la tabla Indicadores. """
        #datos1 = (Nodo1, Nodo2, NuevoIndicador,DistanciaIngresada)
        cursor = self.conexion.cursor()
        N=[d1[0],d1[1],d1[2],d1[3]]
        sql = '''INSERT INTO Indicadores (Id_Nodo1,Id_Nodo2,NOMBRE,DISTANCIA) VALUES (?, ?, ?, ?);'''
        cursor.execute(sql, N)
        self.conexion.commit()
        cursor.close()
    
    def eliminarIndicador(self, indicador):
        """ Elimina un indicador de la base de datos """
        cursor = self.conexion.cursor()
        #sql = '''DELETE FROM Indicador WHERE Nombre=?;'''
        cursor.execute('''DELETE FROM Indicadores WHERE Nombre=?;''', (str(indicador),))
        #cursor.execute(sql, (indicador,))
        self.conexion.commit()
        cursor.close()
    
    def eliminarNodoConIndicador(self, idNodo1,idVecino):
        """ Elimina un indicador de la base de datos """
        cursor = self.conexion.cursor()
        #sql = '''DELETE FROM Indicador WHERE Nombre=?;'''
        cursor.execute('''DELETE FROM Indicadores WHERE Id_Nodo1=? and Id_Nodo2=?;''', (str(idNodo1),str(idVecino),))
        #cursor.execute(sql, (indicador,))
        self.conexion.commit()
        cursor.close()
    
    #Se cargan los datos del circuito si este no ha sido creado
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
        P FLOAT,
        Q FLOAT);
        
        create table if not exists Indicadores
        (Id_indicador INTEGER PRIMARY KEY AUTOINCREMENT,
        Id_Nodo1 INTEGER,
        Id_Nodo2 INTEGER,
        NOMBRE TEXT,
        DISTANCIA FLOAT);
        
        CREATE TRIGGER relacion_nodo_linea AFTER INSERT ON Nodos
        BEGIN
        INSERT INTO Lineas (Id_Nodo1) VALUES (new.Id_Nodo);
        END;
        
        CREATE TRIGGER relacion_nodo_carga AFTER INSERT ON Nodos
        BEGIN
        INSERT INTO Cargas (Id_Nodo,ALIAS) VALUES (new.Id_Nodo,new.Nombre);
        END;
                   
        '''
        self.ejecutar_script(sql)
    
    #Se cargan los datos del circuito si este no ha sido creado
    def autollenadoYacopi(self):
        sql='''
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B1p', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B2', 1);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B2p', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B3', 1);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B3p', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B4', 1);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B4p', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B5', 1);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B5p', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B6', 1);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B6p', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B7', 1);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B7p', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B8', 1);

	    INSERT INTO Nodos (Nombre, Troncal) VALUES ('B8p', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B9', 1);

	    INSERT INTO Nodos (Nombre, Troncal) VALUES ('B9p', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B10', 1);

	    INSERT INTO Nodos (Nombre, Troncal) VALUES ('B10p', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B11', 1);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB2p', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB2', 0);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB3p', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB3', 0);
        
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB4p', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB4', 0);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB5p', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB5', 0);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB6p', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB6', 0);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB7p', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB7', 0);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB8p', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB8', 0);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB9p', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB7k', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB7kp', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB9', 0);

        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB10p', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('RB10', 0);

        
        UPDATE Lineas set Id_Nodo2 = 1, R0 =0.69609, R1 =0.3714, X0 =1.5611,X1 =0.58378, DISTANCIA = 0.224281  where Id_Nodo1=2;
        UPDATE Lineas set Id_Nodo2 = 2, R0 =0.83831, R1 =0.36938, X0 =1.3863,X1 =0.53144, DISTANCIA = 0.039579  where Id_Nodo1=3;
        
        UPDATE Lineas set Id_Nodo2 = 3, R0 =0.69609, R1 =0.3714, X0 =1.5611,X1 =0.58378, DISTANCIA = 8.4354  where Id_Nodo1=4;
        UPDATE Lineas set Id_Nodo2 = 4, R0 =0.83831, R1 =0.36938, X0 =1.3863,X1 =0.53144, DISTANCIA = 1.4886  where Id_Nodo1=5;
        
        UPDATE Lineas set Id_Nodo2 = 5, R0 =0.69609, R1 =0.3714, X0 =1.5611,X1 =0.58378, DISTANCIA = 2.6401  where Id_Nodo1=6;
        UPDATE Lineas set Id_Nodo2 = 6, R0 =0.83831, R1 =0.36938, X0 =1.3863,X1 =0.53144, DISTANCIA = 0.4659  where Id_Nodo1=7;
        
        UPDATE Lineas set Id_Nodo2 = 7, R0 =0.69609, R1 =0.3714, X0 =1.5611,X1 =0.58378, DISTANCIA = 6.85695  where Id_Nodo1=8;
        UPDATE Lineas set Id_Nodo2 = 8, R0 =0.83831, R1 =0.36938, X0 =1.3863,X1 =0.53144, DISTANCIA = 1.21005  where Id_Nodo1=9;
        
        UPDATE Lineas set Id_Nodo2 = 9, R0 =0.69609, R1 =0.3714, X0 =1.5611,X1 =0.58378, DISTANCIA = 2.4837  where Id_Nodo1=10;
        UPDATE Lineas set Id_Nodo2 = 10, R0 =0.83831, R1 =0.36938, X0 =1.3863,X1 =0.53144, DISTANCIA = 0.4383 where Id_Nodo1=11;



        UPDATE Lineas set Id_Nodo2 = 11, R0 =0.7339, R1 =0.55625, X0 =1.9162,X1 =0.48394, DISTANCIA = 2.89255  where Id_Nodo1=12;
        UPDATE Lineas set Id_Nodo2 = 12, R0 =0.7339, R1 =0.55625, X0 =1.7505,X1 =0.56677, DISTANCIA = 0.51045  where Id_Nodo1=13;

        UPDATE Lineas set Id_Nodo2 = 13, R0 =0.7339, R1 =0.55625, X0 =1.9162,X1 =0.48394, DISTANCIA = 1.25885  where Id_Nodo1=14;
        UPDATE Lineas set Id_Nodo2 = 14, R0 =0.7339, R1 =0.55625, X0 =1.7505,X1 =0.56677, DISTANCIA = 0.22215  where Id_Nodo1=15;

        UPDATE Lineas set Id_Nodo2 = 15, R0 =0.7339, R1 =0.55625, X0 =1.9162,X1 =0.48394, DISTANCIA = 3.7162  where Id_Nodo1=16;
        UPDATE Lineas set Id_Nodo2 = 16, R0 =0.7339, R1 =0.55625, X0 =1.7505,X1 =0.56677, DISTANCIA = 0.6558  where Id_Nodo1=17;

        UPDATE Lineas set Id_Nodo2 = 17, R0 =0.7339, R1 =0.55625, X0 =1.9162,X1 =0.48394, DISTANCIA = 3.1708145  where Id_Nodo1=18;
        UPDATE Lineas set Id_Nodo2 = 18, R0 =0.7339, R1 =0.55625, X0 =1.7505,X1 =0.56677, DISTANCIA = 0.5595555  where Id_Nodo1=19;

        UPDATE Lineas set Id_Nodo2 = 19, R0 =0.7339, R1 =0.55625, X0 =1.9162,X1 =0.48394, DISTANCIA = 8.8518235  where Id_Nodo1=20;
        UPDATE Lineas set Id_Nodo2 = 20, R0 =0.7339, R1 =0.55625, X0 =1.7505,X1 =0.56677, DISTANCIA = 1.5620865  where Id_Nodo1=21;
    


        UPDATE Lineas set Id_Nodo2 = 3, R0 =1.228, R1 =1.0503, X0 =1.9451,X1 =0.51284, DISTANCIA = 3.6564535  where Id_Nodo1=22;
        UPDATE Lineas set Id_Nodo2 = 22, R0 =1.228, R1 =1.0503, X0 =1.7794,X1 =0.59568, DISTANCIA = 0.6452565  where Id_Nodo1=23;

        UPDATE Lineas set Id_Nodo2 = 5, R0 =1.228, R1 =1.0503, X0 =1.9451,X1 =0.51284, DISTANCIA = 6.5409982  where Id_Nodo1=24;
        UPDATE Lineas set Id_Nodo2 = 24, R0 =1.228, R1 =1.0503, X0 =1.7794,X1 =0.59568, DISTANCIA = 1.1542938  where Id_Nodo1=25;

        UPDATE Lineas set Id_Nodo2 = 7, R0 =1.228, R1 =1.0503, X0 =1.9451,X1 =0.51284, DISTANCIA = 3.7357245  where Id_Nodo1=26;
        UPDATE Lineas set Id_Nodo2 = 26, R0 =1.228, R1 =1.0503, X0 =1.7794,X1 =0.59568, DISTANCIA = 0.6592455  where Id_Nodo1=27;

        UPDATE Lineas set Id_Nodo2 = 9, R0 =1.228, R1 =1.0503, X0 =1.9451,X1 =0.51284, DISTANCIA = 3.3124925  where Id_Nodo1=28;
        UPDATE Lineas set Id_Nodo2 = 28, R0 =1.228, R1 =1.0503, X0 =1.7794,X1 =0.59568, DISTANCIA = 0.5845575  where Id_Nodo1=29;

        UPDATE Lineas set Id_Nodo2 = 11, R0 =1.228, R1 =1.0503, X0 =1.9451,X1 =0.51284, DISTANCIA = 6.82142765  where Id_Nodo1=30;
        UPDATE Lineas set Id_Nodo2 = 30, R0 =1.228, R1 =1.0503, X0 =1.7794,X1 =0.59568, DISTANCIA = 1.20378135  where Id_Nodo1=31;

        UPDATE Lineas set Id_Nodo2 = 13, R0 =1.228, R1 =1.0503, X0 =1.9451,X1 =0.51284, DISTANCIA = 3.3978495  where Id_Nodo1=32;
        UPDATE Lineas set Id_Nodo2 = 32, R0 =1.228, R1 =1.0503, X0 =1.7794,X1 =0.59568, DISTANCIA = 0.5996205  where Id_Nodo1=33;

        UPDATE Lineas set Id_Nodo2 = 15, R0 =1.228, R1 =1.0503, X0 =1.9451,X1 =0.51284, DISTANCIA = 4.8514005  where Id_Nodo1=34;
        UPDATE Lineas set Id_Nodo2 = 34, R0 =1.228, R1 =1.0503, X0 =1.7794,X1 =0.59568, DISTANCIA = 0.8561295  where Id_Nodo1=35;

        UPDATE Lineas set Id_Nodo2 = 17, R0 =1.228, R1 =1.0503, X0 =1.9451,X1 =0.51284, DISTANCIA = 2.73785  where Id_Nodo1=36;
        UPDATE Lineas set Id_Nodo2 = 36, R0 =1.228, R1 =1.0503, X0 =1.7794,X1 =0.59568, DISTANCIA = 0.48315  where Id_Nodo1=37;
        UPDATE Lineas set Id_Nodo2 = 37, R0 =2.0795, R1 =1.9018, X0 =2.0182,X1 =0.586, DISTANCIA = 5.95  where Id_Nodo1=38;
        UPDATE Lineas set Id_Nodo2 = 38, R0 =2.0795, R1 =1.9018, X0 =1.8526,X1 =0.66883, DISTANCIA = 1.05  where Id_Nodo1=39;

        UPDATE Lineas set Id_Nodo2 = 19, R0 =1.228, R1 =1.0503, X0 =1.9451,X1 =0.51284, DISTANCIA = 6.33333585  where Id_Nodo1=40;
        UPDATE Lineas set Id_Nodo2 = 40, R0 =1.228, R1 =1.0503, X0 =1.7794,X1 =0.59568, DISTANCIA = 1.1176515  where Id_Nodo1=41;

        
        UPDATE Cargas set P=16588, Q=4838  where Id_Nodo=3;
        UPDATE Cargas set P=7334, Q=2139  where Id_Nodo=5;
        UPDATE Cargas set P=16064, Q=4685  where Id_Nodo=7;
        UPDATE Cargas set P=5122, Q=1494  where Id_Nodo=9;
        UPDATE Cargas set P=10244, Q=2988  where Id_Nodo=11;
        UPDATE Cargas set P=10244, Q=2988  where Id_Nodo=13;
        UPDATE Cargas set P=28636, Q=8352  where Id_Nodo=15;
        UPDATE Cargas set P=9429, Q=275  where Id_Nodo=17;
        UPDATE Cargas set P=10127, Q=2954  where Id_Nodo=19;
        UPDATE Cargas set P=6984, Q=2037  where Id_Nodo=21;

        UPDATE Cargas set P=6984, Q=2037  where Id_Nodo=23;
        UPDATE Cargas set P=7334, Q=2139  where Id_Nodo=25;
        UPDATE Cargas set P=16064, Q=4685  where Id_Nodo=27;
        UPDATE Cargas set P=5122, Q=1494  where Id_Nodo=29;
        UPDATE Cargas set P=10244, Q=2988  where Id_Nodo=31;
        UPDATE Cargas set P=10244, Q=2988  where Id_Nodo=33;
        UPDATE Cargas set P=28636, Q=8352  where Id_Nodo=35;
        UPDATE Cargas set P=9429, Q=275  where Id_Nodo=39;
        UPDATE Cargas set P=6984, Q=2037  where Id_Nodo=41;
    
        
        '''

        self.ejecutar_script(sql)
        
    def autollenadoNueva(self):
        sql='''
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B2', 1);
        
        
        UPDATE Lineas set Id_Nodo2 = 1, R0 =0.0, R1 =0.0, X0 =0.0,X1 =0.0, DISTANCIA = 5.0  where Id_Nodo1=2;
        
        UPDATE Cargas set P='0.0', Q='0.0'  where Id_Nodo=2;   
        
        '''

        self.ejecutar_script(sql)
    
    def autollenadoPrueba(self):
        sql='''
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B2', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B3', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B4', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B5', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B6', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B7', 1);
        
        UPDATE Lineas set Id_Nodo2 = 1, R0 =0.3864, R1 =0.01273, X0 =1.55561,X1 =0.35199, DISTANCIA = 30  where Id_Nodo1=2;
        UPDATE Lineas set Id_Nodo2 = 2, R0 =0.7728, R1 =0.01273, X0 =3.1112323,X1 =0.35199, DISTANCIA = 15  where Id_Nodo1=3;
        UPDATE Lineas set Id_Nodo2 = 3, R0 =0.7728, R1 =0.02546, X0 =3.1112323,X1 =0.70399, DISTANCIA = 10  where Id_Nodo1=4;
        UPDATE Lineas set Id_Nodo2 = 2, R0 =0.3864, R1 =0.02546, X0 =1.55561,X1 =0.70399, DISTANCIA = 40  where Id_Nodo1=5;
        UPDATE Lineas set Id_Nodo2 = 3, R0 =0.7728, R1 =0.01273, X0 =1.55561,X1 =0.70399, DISTANCIA = 20  where Id_Nodo1=6;
        UPDATE Lineas set Id_Nodo2 = 4, R0 =0.3864, R1 =0.02546, X0 =3.1112323,X1 =0.35199, DISTANCIA = 19  where Id_Nodo1=7;
    
        
        UPDATE Cargas set Alias='C2', P=8000, Q=100  where Id_Nodo=2;
        UPDATE Cargas set Alias='C3', P=12000.0, Q=200  where Id_Nodo=3;
        UPDATE Cargas set Alias='C4', P=8000, Q=200  where Id_Nodo=4;
        UPDATE Cargas set Alias='C5', P=8000, Q=150.0  where Id_Nodo=5;
        UPDATE Cargas set Alias='C6', P=12000.0, Q=100  where Id_Nodo=6;
        UPDATE Cargas set Alias='C7', P=16000, Q=200  where Id_Nodo=7;
        
        INSERT INTO Indicadores (NOMBRE,Id_Nodo1,Id_Nodo2, Distancia) VALUES ('I1', 2,3,1);
        INSERT INTO Indicadores (NOMBRE,Id_Nodo1,Id_Nodo2, Distancia) VALUES ('I2', 2,5,2);
        INSERT INTO Indicadores (NOMBRE,Id_Nodo1,Id_Nodo2, Distancia) VALUES ('I3', 3,6,3);
        INSERT INTO Indicadores (NOMBRE,Id_Nodo1,Id_Nodo2, Distancia) VALUES ('I4', 4,7,2);
        
        
        '''
        self.ejecutar_script(sql)
    
    def autollenadoPruebaSinIdentificadores(self):
        sql='''
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B2', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B3', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B4', 1);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B5', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B6', 0);
        INSERT INTO Nodos (Nombre, Troncal) VALUES ('B7', 1);
        
        UPDATE Lineas set Id_Nodo2 = 1, R0 =0.3864, R1 =0.01273, X0 =1.55561,X1 =0.35199, DISTANCIA = 30  where Id_Nodo1=2;
        UPDATE Lineas set Id_Nodo2 = 2, R0 =0.3864, R1 =0.01273, X0 =1.55561,X1 =0.35199, DISTANCIA = 15  where Id_Nodo1=3;
        UPDATE Lineas set Id_Nodo2 = 3, R0 =0.3864, R1 =0.01273, X0 =1.55561,X1 =0.35199, DISTANCIA = 10  where Id_Nodo1=4;
        UPDATE Lineas set Id_Nodo2 = 2, R0 =0.3864, R1 =0.01273, X0 =1.55561,X1 =0.35199, DISTANCIA = 8  where Id_Nodo1=5;
        UPDATE Lineas set Id_Nodo2 = 3, R0 =0.3864, R1 =0.01273, X0 =1.55561,X1 =0.35199, DISTANCIA = 20  where Id_Nodo1=6;
        UPDATE Lineas set Id_Nodo2 = 4, R0 =0.3864, R1 =0.01273, X0 =1.55561,X1 =0.35199, DISTANCIA = 19  where Id_Nodo1=7;
    
        
        UPDATE Cargas set Alias='C2', P=8000, Q=100  where Id_Nodo=2;
        UPDATE Cargas set Alias='C3', P=8000, Q=100  where Id_Nodo=3;
        UPDATE Cargas set Alias='C4', P=8000, Q=100  where Id_Nodo=4;
        UPDATE Cargas set Alias='C5', P=8000, Q=100  where Id_Nodo=5;
        UPDATE Cargas set Alias='C6', P=8000, Q=100  where Id_Nodo=6;
        UPDATE Cargas set Alias='C7', P=8000, Q=100  where Id_Nodo=7;
        
        '''
        self.ejecutar_script(sql)
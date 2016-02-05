import sqlite3 as sq3
import os
 
class Modelo(object):
    def __init__(self, base_datos="almacen.db"):
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
        sql = '''
              INSERT INTO productos (codigo, descripcion, valor)
              VALUES (?, ?, ?)
              '''
        cursor = self.conexion.cursor()
        cursor.execute(sql, d1)
        nuevaID = cursor.lastrowid
        self.conexion.commit()
        cursor.close()
        return nuevaID
 
    def actualizar(self, d2):
        """ Actualiza los datos de un registro existente.
        Es necesario proporcionar la id del registro
        junto con los valores de las otras columnas
        en el parametro d2. """
        sql = '''
              UPDATE productos Set codigo=?, descripcion=?, valor=?
              WHERE id=?
              '''
        cursor = self.conexion.cursor()
        cursor.execute(sql, d2)
        self.conexion.commit()
        cursor.close()
 
    def seleccionar(self, id=None):
        """ Selecciona registros en la base de datos """
        cursor = self.conexion.cursor()
        sql1 = ' SELECT * FROM productos '
        sql2 = sql1 + ' WHERE id = ?'
        if not id:
            cursor.execute(sql1)
        else:
            cursor.execute(sql2, (id,))
        registros = cursor.fetchall() # recupera todos los registros
        cursor.close()
        return registros
 
    def eliminar(self, id):
        """ Elimina un registro de la base de datos """
        sql = '''
              DELETE FROM productos
              WHERE id = ?
              '''
        cursor = self.conexion.cursor()
        cursor.execute(sql, (id,))
        self.conexion.commit()
        cursor.close()
 
    def ejecutar_script(self,sql):
        """ Ejecuta varias sentencia SQL, sin retornar algun valor"""
        cursor = self.conexion.cursor()
        cursor.executescript(sql)
        self.conexion.commit()
        #cursor.Close()
        cursor.Close
 
    def crearTabla(self):
        """ crea la tabla de la base de datos y los valores 
        por omision si aquella no existe aun """
        sql = '''
              CREATE TABLE productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo VARCHAR(8),
                descripcion VARCHAR(100),
                valor REAL(5, 2)
              );
 
        INSERT INTO productos (codigo, descripcion, valor)
        VALUES ('CDF45', 'Codificador de senales analogicas', '1450,00');
 
        INSERT INTO productos (codigo, descripcion, valor)
        VALUES ('MLD12', 'Molde para cubierta de lampara', '12,00' );
 
        INSERT INTO productos (codigo, descripcion, valor)
        VALUES ('TLV36', 'Televisor Hankey 36 pulgadas', '2450,25' );
 
        INSERT INTO productos (codigo, descripcion, valor)
        VALUES ('CMP09', 'Comprobador de continuidad LJK', '547,80' );
 
        INSERT INTO productos (codigo, descripcion, valor)
        VALUES ('TRJS015', 'Terraja SIM  15', '45,25');
        '''
        self.ejecutar_script(sql)
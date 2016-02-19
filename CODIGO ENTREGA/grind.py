#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import wx.grid as wxgrid
import modeloDatos
import modelo
 
class Rejilla(wxgrid.Grid):
    def __init__(self, parent):
        wxgrid.Grid.__init__(self, parent)
        self.CreateGrid(5, 12)
        self.crearColumnas()
        
 
    def columnas(self):
        """
        Define los atributos de las columnas
        Etiqueta, Tamaño, Tipo lectura, Presentador
        """
        return [
            ('Id', 65, True, wxgrid.GridCellNumberRenderer()),
            ('Nombre Nodo', 100, False, wxgrid.GridCellStringRenderer()),
            ('Troncal',50, False, wxgrid.GridCellStringRenderer()),
            ('Nodo Linea',70, False, wxgrid.GridCellStringRenderer()),
            ('R0',50, False, wxgrid.GridCellStringRenderer()),
            ('R1',50, False, wxgrid.GridCellStringRenderer()),
            ('X0',50, False, wxgrid.GridCellStringRenderer()),
            ('X1',50, False, wxgrid.GridCellStringRenderer()),
            ('Distancia',70, False, wxgrid.GridCellStringRenderer()),
            ('Alias',50, False, wxgrid.GridCellStringRenderer()),
            ('P',60, False, wxgrid.GridCellStringRenderer()),
            ('Q',50, False, wxgrid.GridCellStringRenderer())
           ]
 
    def crearColumnas(self):
        """ Establece atributos de las columnas de la rejilla """
        for ind, col in enumerate(self.columnas()):
            self.SetColLabelValue(ind, col[0])
            self.SetColSize(ind, col[1])
            atrib = wxgrid.GridCellAttr()
            atrib.SetReadOnly(col[2])
            atrib.SetRenderer(col[3])
            self.SetColAttr(ind, atrib)
 
class Ventana(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None,
        title = "Control rejilla y base de datos",
        size=(1000,200))
        panel = wx.Panel(self)
        self.grilla = Rejilla(panel)
        # Guardan el número de filas y columnas iniciales de la rejilla
        self.numFilas = self.grilla.GetNumberRows()
        self.numCols = self.grilla.GetNumberCols()
         
        sizerH = wx.BoxSizer(wx.HORIZONTAL)
        sizerV = wx.BoxSizer(wx.VERTICAL)
        sizerV.Add(self.grilla, 1, wx.EXPAND)
 
        self.crearBotones(panel,sizerH)
        sizerV.Add(sizerH, 0, wx.EXPAND)
        panel.SetSizer(sizerV)
        self.Center()
        self.modelo = modeloDatos.Modelo("yacopi")
 
    def datosBotones(self):
        """ Define el rótulo y el manejador de evento del botón """
        return (
                ('', ''), # un espaciador
                ('Guardar', self.guardarRegistro),
                ('Eliminar', self.eliminarRegistro),
                ('Mostrar todos', self.mostrarRegistros),
                ('Limpiar', self.limpiarRejilla),
                ('',''),
                ('Cerrar', self.cerrar),
                ('', '')
               )
 
    def crearBotones(self,panel,sizer):
        """ Crea y posiciona los botones de la interfaz """
        for etiqueta, manejador in self.datosBotones():
            # Si no existe etiqueta, añadir un espaciador
            # y continuar con la siguiente tupla
            if not etiqueta:
                sizer.Add((20, 20), 1, wx.EXPAND)
                continue
            boton = wx.Button(panel, -1, etiqueta)
            self.Bind(wx.EVT_BUTTON, manejador, boton)
            sizer.Add(boton, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM, 3)
 
    # Plantilla para los manejadores de evento de los botones
    def guardarRegistro(self, event):
        fila=[]
        # obtener el índice de la fila seleccionada. 
        fila = self.grilla.GetSelectedRows()[0]
        # desempaquetar los datos utilizando una comprensión de lista 
        id, nombre, troncal, linea,r0,r1,x0,x1,distancia,alias,potencia,facto = [self.grilla.GetCellValue(fila, col) 
                                      for col in xrange(self.numCols)] 
        datos1 = (nombre, troncal, linea,r0,r1,x0,x1,distancia,alias,potencia,facto) 
        # datos requeridos por insertar 
        datos2 = (nombre, troncal, linea,r0,r1,x0,x1,distancia,alias,potencia,facto, id) 
        # datos requeridos por actualizar 
        # si no existe el id, es un nuevo registro y se inserta 
        if not id: 
            id = self.modelo.insertar(datos1) 
        # si existe el id, el registro es actualizado 
        else: self.modelo.actualizar(datos2) 
        # mostrar el registro actualizado 
        self.refrescarRegistro(id, fila)
        #mostrarRegistros(self, event):
    
    def refrescarRegistro(self, id, fila):
        registro = self.modelo.seleccionar(id) 
        print('la id en refrescar es :'+str(id))
        print(registro)
        for dato in registro: 
            for col, valor in enumerate(dato): 
                    self.grilla.SetCellValue(fila, col, str(valor))
                    '''if col in (0, 3):self.grilla.SetCellValue(fila, col, str(valor)) 
                    else: self.grilla.SetCellValue(fila, col, 
                                                   valor.encode('utf-8'))'''
 
    def eliminarRegistro(self, event):
        #Se debe permitir eliminar solo los nodos ramales y que no sean nodo 2 de otro nodo
        ##REVISAR
        #Eliminacion solo de los ramales
        # Obtener el índice de la fila del registro 
        fila = self.grilla.GetSelectedRows()[0] 
        # Obtener la id del registro 
        id = self.grilla.GetCellValue(fila, 0)
        troncal = self.grilla.GetCellValue(fila, 2)
        print(troncal)
        if(int(troncal)==0):
            self.modelo.eliminar(id) 
            # Borrar la fila de la rejilla 
            self.grilla.DeleteRows(fila, 1)
        else:
            print("el nodo esta en la troncal y no se puede borrar")
 
    #Muestra los registros OK
    def mostrarRegistros(self, event):
        # Seleccionar todos los registros 
        registros = self.modelo.seleccionar() 
        difFilas = len(registros) - self.numFilas 
        if difFilas > 0: 
            self.grilla.AppendRows(difFilas) 
        elif difFilas < 0: 
            self,grilla.AppendRows(-difFilas) 
        for fila, dato in enumerate(registros): 
            for col, valor in enumerate(dato): 
                self.grilla.SetCellValue(fila, col, str(valor))
                '''if col not in (0, 3): 
                    self.grilla.SetCellValue(fila, col, 
                                             valor.encode('utf-8')) 
                else: self.grilla.SetCellValue(fila, col, str(valor))'''
        #self.grilla.Enable(False)
 
    def limpiarRejilla(self, event):
        difFilas = self.grilla.GetNumberRows() - self.numFilas 
        if difFilas > 0: 
            # Elimina difFilas filas después de la 5 
            self.grilla.DeleteRows(5,difFilas) 
        else: 
            self.grilla.AppendRows(-difFilas) 
        self.grilla.ClearGrid()
 
    def cerrar(self, event):
        self.conexion.close() 
        self.Close()
 
if __name__ == "__main__":
    app = wx.App()
    frame = Ventana().Show()
    app.MainLoop()
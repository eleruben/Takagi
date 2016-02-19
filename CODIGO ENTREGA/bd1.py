import wx
import sqlite3 as dbapi
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        MyPanel(self)
class MyPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        inventario = wx.StaticText(self, -1, u'Bienvenido Inventario: ', pos = (35,10))
        codigo = wx.StaticText(self, -1, 'Codigo: ', pos = (20,30))
        self.codigo_cuadro = wx.TextCtrl(self, -1, '', pos = (20,50))
        producto = wx.StaticText(self, -1, 'Producto: ', pos = (20,80))
        self.producto_cuadro = wx.TextCtrl(self, -1, '', pos = (20,100))
        costo = wx.StaticText(self, -1, 'Costo: ', pos = (20,130))     
        self.costo_cuadro = wx.TextCtrl(self, -1, '', pos = (20,150))
        guardar = wx.Button(self, -1, 'Guardar', pos = (20,180))
        buscar = wx.Button(self, -1, 'Buscar', pos = (20,210))
        salir = wx.Button(self, -1, 'Salir', pos = (20,240))
        guardar.Bind(wx.EVT_BUTTON, self.OnGuardar)
        buscar.Bind(wx.EVT_BUTTON, self.OnBuscar)
        salir.Bind(wx.EVT_BUTTON, self.OnSalir)
    def OnGuardar(self, evt):
        bd = dbapi.connect("formulario.dat")
        self.cursor = bd.cursor()
        #self.cursor.execute("DROP TABLE inv1")
        self.cursor.execute('''create table if not exists inv1 
        (Id INTEGER PRIMARY KEY AUTOINCREMENT,
        CODIGO_CUADRO TEXT NOT NULL,
        PRODUCTO_CUADRO TEXT NOT NULL)''')
        self.cursor.execute("INSERT INTO inv1 (CODIGO_CUADRO, PRODUCTO_CUADRO) VALUES ('FRESA', 15)")
        self.cursor.execute("INSERT INTO inv1 (CODIGO_CUADRO, PRODUCTO_CUADRO) VALUES ('papaya', 20)")
        bd.commit()
        self.cursor.close()
        bd.close()
        ingresodecodigo = self.codigo_cuadro.GetValue()
        dialogo = wx.MessageDialog(self, 'El producto %s, se ha guardado correctamente' % (ingresodecodigo), 'Informacion', wx.OK | wx.ICON_INFORMATION)
        dialogo.ShowModal()
        self.codigo_cuadro.Clear()
        self.producto_cuadro.Clear()
        self.costo_cuadro.Clear()
        dialogo.Destroy()
    def OnBuscar(self, evt):
        #from prueba import MyFrame2
        bd = dbapi.connect("formulario.dat")
        self.cursor = bd.cursor()
        criterio = '1'
        #self.cursor.execute("""SELECT * FROM inventario WHERE codigo_cuadro LIKE ('%%%s%%')""" %(criterio))
        #self.cursor.execute("""SELECT * FROM inv1 """ )
        self.cursor.execute("""SELECT * FROM inv1""")
        #print(self.cursor.fetchall())
        #print(self.cursor)
        for i in self.cursor:
            print "ID=",i[0]
            print "CODIGO_CUADRO",i[1]
            print "PRODUCTO_CUADRO",i[2]
        self.cursor.close()
        bd.close()
        
        
    def OnSalir(self, evt):
        bd = dbapi.connect("formulario.dat")
        self.cursor = bd.cursor()
        #self.cursor.execute("DROP TABLE inv1")
        self.cursor.execute("UPDATE inv1 set PRODUCTO_CUADRO = 45000.00 where ID=1")
        bd.commit()
        bd.close()
        #self.Parent.Close()
class App(wx.App):
    def OnInit(self):
        f = MyFrame(parent = None, title = u'Inventario', size = (200,400), pos = (320,150))
        f.Show()
        return True
aplicacion = App(0)
aplicacion.MainLoop()
import wx
import sqlite3
conn = sqlite3.connect('formulario.dat')
cur = conn.cursor()
cur.execute("""SELECT * FROM inventario""")
list = list(cur.fetchall())
index = range(len(list))
class App(wx.App):
    def OnInit(self):
        self.ventana = wx.Frame(parent = None, title = u'Resultados.', size = (200,400), pos = (320,150))
        panel = wx.Panel(self.ventana, -1)
        codigo = wx.StaticText(panel, -1, 'Codigo', pos = (20,30))
        self.codigocuadro = wx.TextCtrl(panel, -1, '', pos = (20, 50))
        self.codigocuadro.Bind(wx.EVT_TEXT, self.Buscar)
        return True
    def Buscar(self, evt):
        cur.execute("""SELECT * FROM inventario""")
        all = cur.fetchall()
        criterio = self.codigocuadro.GetValue()
        if criterio <> '':
            cur.execute("""SELECT * FROM inventario WHERE codigo_cuadro LIKE ('%%%s%%')""" %(criterio))
            items = cur.fetchall()
        else:
            items = []
aplicacion = App()
aplicacion.MainLoop()
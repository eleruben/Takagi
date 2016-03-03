import wx
 
#frame
class window (wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'Calculadora Basica en Python by Nefisco',size=(420,420))
       
        #presentacion
        a=wx.MessageDialog(None,'hola mundo! \n Soy una Calculadora \n mi creador es Nefisco','By Nefisco',style=wx.OK)
        b=a.ShowModal()
       
        #barra de menu
        status=self.CreateStatusBar()
        menu=wx.MenuBar()
        creditos=wx.Menu()
        contactos=wx.Menu()
        salir=wx.Menu()
 
        creditos.Append(wx.ID_ABOUT,'Creditos', 'Agradecimientos por Colaboracion')
        wx.EVT_MENU(self,wx.ID_ABOUT, self.creditos)
 
        contactos.Append(wx.ID_ADD, 'Contactar a Nefisco', 'Nesecitas Ayuda')
        wx.EVT_MENU(self,wx.ID_ADD, self.contactar)
 
        contactos.Append(wx.ID_APPLY, 'Paginas con contenido aceerca de Python', 'Mi Ayuda Durante los Tutoriales')
        wx.EVT_MENU(self,wx.ID_APPLY, self.paginas)
 
        salir.Append(wx.ID_EXIT,"Salir", "No te ballas tu eres Chevere XD")
        wx.EVT_MENU(self,wx.ID_EXIT, self.salir)
       
        menu.Append(creditos,'Creditos')
        menu.Append(contactos, 'Contactos')
        menu.Append(salir, 'Salir')
       
        self.SetMenuBar(menu)
 
        #botones
        suma = wx.Button(self, label = '+', pos = (100 - 60 - 15, 230), size = (60,25))
        resta = wx.Button(self, label = '-', pos = (200 - 60 - 15, 230), size = (60,25))
        multiplica = wx.Button(self, label = '*', pos = (300 - 60 - 15, 230), size = (60,25))
        divide = wx.Button(self, label = '/', pos = (400 - 60 - 15, 230), size = (60,25))
        limpia= wx.Button(self, label='Limpiar', pos=(250 - 60 - 15, 280),size=(60,25))
 
        #text box
        self.valor1 = wx.TextCtrl(self, pos = (10, 30), size = (400 - 120 - 15 - 10, 25), style=wx.TE_PROCESS_ENTER,value='Ingrese el Primer Valor')
        self.valor2 = wx.TextCtrl(self,  pos = (10, 100), size = (400 - 120 - 15 - 10, 25), style=wx.TE_PROCESS_ENTER,value='Ingrese el Segundo Valor')
        self.resultado = wx.TextCtrl(self,  pos = (10, 170), size = (400 - 120 - 15 - 10, 25),style=wx.TE_PROCESS_ENTER)
 
        #labels
        label1 = wx.StaticText(self,label='Valor 1', size = (400 - 120 - 15 - 10, 25),pos = (10, 8))
        label2 = wx.StaticText(self,label='Valor 2',size = (400 - 120 - 15 - 10, 25),pos = (10, 78))
        label3 = wx.StaticText(self,label='Resultado',size = (400 - 120 - 15 - 10, 25),pos = (10, 148))
        label4 = wx.StaticText(self,label='Made By Nefisco',size = (300 - 120 - 15 - 10, 25),pos = (10, 298))
     
        self.Show(True)
       
    #Eventos
 
    def creditos(self,event):#creditos
                     salir=wx.MessageDialog(None, 'desarrollado por Nefisco \n Colaborador 1: Jose Reyna (jobliz) \n Colaborador 2: Doreina Pena (dorex89)', 'Creditos',  style=wx.OK)
                     salir.ShowModal()
                     
 
    def salir(self,event):#Salir
                     salir=wx.MessageDialog(None, 'Chaup :,(','Salir', style=wx.OK)
                     salir.ShowModal()
                     self.Close(True)
 
    def contactar(self,event):#contactar a nefisco
                     salir=wx.MessageDialog(None,  'Miguelsediles@hotmail.com \n miguelasedilesdq@gmail.com \n@Nefisco','Contactar a Nefisco', style=wx.OK)
                     salir.ShowModal()
                     
 
    def paginas(self,event):#paginas python
                     salir=wx.MessageDialog(None, 'TheNewBoston.com \n Python.org \n wxpython.org','Paginas de Python', style=wx.OK)
                     salir.ShowModal()
 
app = wx.App()
a=window()
app.MainLoop()
 
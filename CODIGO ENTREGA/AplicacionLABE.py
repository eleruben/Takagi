import wx
import wx.xrc
import math
import matplotlib
import xlrd
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
import matplotlib.colors as colors
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

import os

import numpy as np



Ia=[]
Ib=[]
Ic=[]
In=[]
Va=[]
Vb=[]
Vc=[]

IA=0
IB=0
VA=0
VB=0

ia=[]
ib=[]
ic=[]
i1n=[]
va=[]
vb=[]
vc=[]
iprea=[]
ipreb=[]
iprec=[]
Ifase=[]
Ipre=[]


N=32
T1=np.arange(0,(N-1)*2*math.pi/N+0.001,2*math.pi/N)
#T1=0:2*math.pi/N:(N-1)*2*math.pi/N;
u=2*np.exp(np.multiply(1j,T1))/(math.sqrt(3)*N);


###########################################################################
##                          Class Aplicacion                              #
###########################################################################

class Aplicacion( wx.Frame ):

    def __init__( self):
        #Codigo que se ejecuta primero en la ejecucion del codigo
        wx.Frame.__init__ (self, None,-1, title = u"LOCALIZACION DE FALLAS EEC-LABE", pos = wx.DefaultPosition, size = wx.Size( 1024,750 ), style = wx.DEFAULT_FRAME_STYLE| wx.MAXIMIZE  )
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        #Funcion para crear el menu
        self.crear_menu()
        #Funcion para crear el panel
        self.crear_panel_main()
        #Extrae el directorio actual en el que se ejecuta el archivo
        self.actual = str(os.getcwd())


    def crear_menu(self):
	self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
	self.m_menubar1 = wx.MenuBar( 0 )
	#Contenedor del menu Bar Configuracion
	self.m_menu1 = wx.Menu()

	#Opcion de Importar archivo, la cual extrae la informacion del archivos comtrade,
	#tambien se le permite al usuario tener un acceso rapido con el comando "Ctrl - 0"
	self.m_menuItem1 = self.m_menu1.Append(-1, "&Importar\tCtrl-O", "Importar datos del archivo")
	self.Bind(wx.EVT_MENU, self.on_import_file, self.m_menuItem1)
	self.m_menu1.AppendSeparator()

	#Opcion de Exportar archivos, permite al usuario guardar los graficos de los datos de corriente y
	#tension, al igual que la ubicacion de la fala. Tambien permitira guardar los
	#datos de la falla en un formato xls, tambien se le permite al usuario tener un acceso
	#rapido con el comando "Ctrl - S"
	self.m_menuItem2 = self.m_menu1.Append(-1, "&Exportar\tCtrl-S", "Exportar archivos")
	#ESPACIO PARA EL EVENTO EXPORTAR
	self.m_menu1.AppendSeparator()

	#Opcion de Salir, permite al usuario salir de la aplicacion, se le permite al usuario
	#tener un acceso rapido con el comando "Ctrl - S"
	self.m_menuItem3 = self.m_menu1.Append(-1, "&Salir\tCtrl-X", "Salir")
	self.Bind(wx.EVT_MENU, self.salir, self.m_menuItem3)

		
	self.m_menubar1.Append( self.m_menu1, u"Configuracion" )
	#Contenedor del menu Bar Ayuda	
	self.m_menu2 = wx.Menu()
	#Opcion de Manual de uso
	self.m_menuItem = self.m_menu2.Append(-1, "&Manual de uso", "Manual de uso")
	#Opcion de Acerca de, la cual hacer el llamado a una ventana que indica
	#los datos de identificacion de la aplicacion
	self.m_menuItem5 = self.m_menu2.Append(-1, "&Acerca de ...", "Acerca de ...")
	self.Bind(wx.EVT_MENU, self.on_about, self.m_menuItem5)
	
		
	self.m_menubar1.Append( self.m_menu2, u"Ayuda" )
		
	self.SetMenuBar( self.m_menubar1 )

    def crear_panel_main(self):
        #BoxSizer 1 contiene los boxsizers 2 y 3 y esta dispuesto de forma horizontal
	bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
	#BoxSizer 2 contiene los boxsizers 6 y 14 y esta dispuesto de forma vertical
	bSizer2 = wx.BoxSizer( wx.VERTICAL )
	#BoxSizer 6 contiene los boxsizers 4 y 5 y esta dispuesto de forma horizontal
	bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
	#BoxSizer 4 contiene los nombres Tipo falla, Canal de falla y Distancia
	bSizer4 = wx.BoxSizer( wx.VERTICAL )
	#Espacio antes de Tipo de falla
        bSizer4.AddSpacer(7)

        #Objeto de tipo Static text que tiene por nombre Tipo de falla
	self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Tipo de falla", wx.DefaultPosition, wx.DefaultSize, 0 )
	self.m_staticText1.Wrap( -1 )
	self.m_staticText1.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
	bSizer4.Add( self.m_staticText1, 0, wx.ALL, 5 )
	
        #Espacio entre Tipo de falla y Canal de falla
	bSizer4.AddSpacer(8)

	#Objeto de tipo Static text que tiene por nombre Canal de falla
	self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Canal de falla", wx.DefaultPosition, wx.DefaultSize, 0 )
	self.m_staticText2.Wrap( -1 )
	self.m_staticText2.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
	bSizer4.Add( self.m_staticText2, 0, wx.ALL, 5 )

	#Espacio entre Canal de falla y Distancia
	bSizer4.AddSpacer(8)

	#Objeto de tipo Static text que tiene por nombre Distancia
	self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Distancia", wx.DefaultPosition, wx.DefaultSize, 0 )
	self.m_staticText3.Wrap( -1 )
	self.m_staticText3.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
	bSizer4.Add( self.m_staticText3, 0, wx.ALL, 5 )

	bSizer6.Add( bSizer4, 0, wx.EXPAND, 5 )

	#BoxSizer 5 contiene los datos asociados a el BoxSizer4, que se muestran cuando se importan los datos
	#de la falla
	bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
	self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
	self.m_textCtrl1.Enable( False )
	bSizer5.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
		
	self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
	self.m_textCtrl2.Enable( False )
	bSizer5.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
		
	self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
	self.m_textCtrl3.Enable( False )
	bSizer5.Add( self.m_textCtrl3, 0, wx.ALL, 5 )
		
	bSizer6.Add( bSizer5, 0, wx.EXPAND, 5 )
		
	bSizer2.Add( bSizer6, 0, wx.EXPAND, 5 )
	#BoxSizer 14 contiene el grafo de las fallas
	bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
	bSizer2.Add( bSizer14, 1, wx.EXPAND, 5 )
		
	bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
	bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
	bSizer12 = wx.BoxSizer( wx.VERTICAL )

	#BoxSizer 15 contiene los boxsizers 12 y 16 y esta dispuesto de forma horizontal	
	bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
	self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.dpi = 100

        #Figura que corresponde a la grafica de tensiones de falla del circuito
        self.fig1 = Figure((10.0, 3.0), dpi=self.dpi)
        self.canvas_voltaje = FigCanvas(self.m_panel1, -1, self.fig1)


        self.axes_voltaje = self.fig1.add_subplot(111)


        self.axes_voltaje.set_xlabel('t')
        self.axes_voltaje.set_ylabel('V(t)')



        
	bSizer15.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5)
	
	#BoxSizer 12 contiene el panel y los checkboxs
	bSizer12.Add( bSizer15, 1, wx.EXPAND, 5 )
	#BoxSizer 16 contiene los checkbox de la figura de tension
	bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
	self.m_checkBox1 = wx.CheckBox( self, wx.ID_ANY, u"FASE A", wx.DefaultPosition, wx.DefaultSize, 0 )
	self.ColourPickerCtrl1= wx.ColourPickerCtrl( self,wx.ID_ANY, wx.GREEN, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
	self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseAvoltaje, self.ColourPickerCtrl1)
	self.Bind(wx.EVT_CHECKBOX, self.on_faseA_voltaje, self.m_checkBox1)
	bSizer16.Add( self.m_checkBox1, 0, wx.ALL, 5 )
	bSizer16.Add( self.ColourPickerCtrl1, 0, wx.ALL, 5 )
		
	self.m_checkBox2 = wx.CheckBox( self, wx.ID_ANY, u"FASE B", wx.DefaultPosition, wx.DefaultSize, 0 )
	self.ColourPickerCtrl2= wx.ColourPickerCtrl( self,wx.ID_ANY, wx.BLUE, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
	self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseBvoltaje, self.ColourPickerCtrl2)
	self.Bind(wx.EVT_CHECKBOX, self.on_faseB_voltaje, self.m_checkBox2)
	bSizer16.Add( self.m_checkBox2, 0, wx.ALL, 5 )
	bSizer16.Add( self.ColourPickerCtrl2, 0, wx.ALL, 5 )
		
	self.m_checkBox3 = wx.CheckBox( self, wx.ID_ANY, u"FASE C", wx.DefaultPosition, wx.DefaultSize, 0 )
	self.ColourPickerCtrl3= wx.ColourPickerCtrl( self,wx.ID_ANY, wx.RED, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
	self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseCvoltaje, self.ColourPickerCtrl3)
	self.Bind(wx.EVT_CHECKBOX, self.on_faseC_voltaje, self.m_checkBox3)
	bSizer16.Add( self.m_checkBox3, 0, wx.ALL, 5 )
	bSizer16.Add( self.ColourPickerCtrl3, 0, wx.ALL, 5 )
		
		
	bSizer12.Add( bSizer16, 0, wx.EXPAND, 5)
		
		
	bSizer3.Add( bSizer12,1, wx.EXPAND, 5 )
		
	bSizer13 = wx.BoxSizer( wx.VERTICAL )
	
	bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
	self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        #Figura que corresponde a la grafica de corrientes de falla del circuito
	self.fig2 = Figure((10.0, 3.0), dpi=self.dpi)
        self.canvas_corriente = FigCanvas(self.m_panel2, -1, self.fig2)

        self.axes_corriente = self.fig2.add_subplot(111)
        self.axes_corriente.set_xlabel('t')
        self.axes_corriente.set_ylabel('I(t)')

	
	
	
	bSizer17.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
	
		
	bSizer13.Add( bSizer17, 1, wx.EXPAND, 5 )
	bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
	self.m_checkBox4 = wx.CheckBox( self, wx.ID_ANY, u"FASE A", wx.DefaultPosition, wx.DefaultSize, 0 )
	self.ColourPickerCtrl4= wx.ColourPickerCtrl( self,wx.ID_ANY, wx.GREEN, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
	self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseAcorriente, self.ColourPickerCtrl4)
	self.Bind(wx.EVT_CHECKBOX, self.on_faseA_corriente, self.m_checkBox4)
	bSizer18.Add( self.m_checkBox4, 0, wx.ALL, 5 )
	bSizer18.Add( self.ColourPickerCtrl4, 0, wx.ALL, 5 )
		
	self.m_checkBox5 = wx.CheckBox( self, wx.ID_ANY, u"FASE B", wx.DefaultPosition, wx.DefaultSize, 0 )
	self.ColourPickerCtrl5= wx.ColourPickerCtrl( self,wx.ID_ANY, wx.BLUE, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
	self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseBcorriente, self.ColourPickerCtrl5)
	self.Bind(wx.EVT_CHECKBOX, self.on_faseB_corriente, self.m_checkBox5)
	bSizer18.Add( self.m_checkBox5, 0, wx.ALL, 5 )
	bSizer18.Add( self.ColourPickerCtrl5, 0, wx.ALL, 5 )
		
	self.m_checkBox6 = wx.CheckBox( self, wx.ID_ANY, u"FASE C", wx.DefaultPosition, wx.DefaultSize, 0 )
	self.ColourPickerCtrl6= wx.ColourPickerCtrl( self,wx.ID_ANY, wx.RED, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
	self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseCcorriente, self.ColourPickerCtrl6)
	self.Bind(wx.EVT_CHECKBOX, self.on_faseC_corriente, self.m_checkBox6)
	bSizer18.Add( self.m_checkBox6, 0, wx.ALL, 5 )
	bSizer18.Add( self.ColourPickerCtrl6, 0, wx.ALL, 5 )
		
		
		
	bSizer13.Add( bSizer18, 0, wx.EXPAND, 5 )
		
		
	bSizer3.Add( bSizer13, 0, wx.EXPAND, 5 )
		
		
	bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )
		
		
	self.SetSizer( bSizer1 )
	self.Layout()


    def dibujar_voltaje(self):
        self.axes_voltaje.clear()
        self.axes_voltaje.set_xlabel('t')
        self.axes_voltaje.set_ylabel('V(t)')
        if (self.m_checkBox1.IsChecked()):
            self.axes_voltaje.plot(va,color= self.ColourPickerCtrl1.GetColour().GetAsString(wx.C2S_HTML_SYNTAX))
        if (self.m_checkBox2.IsChecked()):
            self.axes_voltaje.plot(vb,color= self.ColourPickerCtrl2.GetColour().GetAsString(wx.C2S_HTML_SYNTAX))
        if (self.m_checkBox3.IsChecked()):
            self.axes_voltaje.plot(vc,color= self.ColourPickerCtrl3.GetColour().GetAsString(wx.C2S_HTML_SYNTAX))
        self.m_textCtrl1.SetValue("Monofasica")
        self.m_textCtrl2.SetValue("C")
        #self.m_textCtrl1.IsModified(False)

        self.canvas_voltaje.draw()


    def dibujar_corriente(self):
        self.axes_corriente.clear()
        self.axes_corriente.set_xlabel('t')
        self.axes_corriente.set_ylabel('I(t)')
        if (self.m_checkBox4.IsChecked()):
            self.axes_corriente.plot(ia,color= self.ColourPickerCtrl4.GetColour().GetAsString(wx.C2S_HTML_SYNTAX))
        if (self.m_checkBox5.IsChecked()):
            self.axes_corriente.plot(ib,color= self.ColourPickerCtrl5.GetColour().GetAsString(wx.C2S_HTML_SYNTAX))
        if (self.m_checkBox6.IsChecked()):
            self.axes_corriente.plot(ic,color= self.ColourPickerCtrl6.GetColour().GetAsString(wx.C2S_HTML_SYNTAX))
        self.canvas_corriente.draw()

    def on_colourFaseAvoltaje(self, event):
        self.dibujar_voltaje()

    def on_colourFaseBvoltaje(self, event):
        self.dibujar_voltaje()

    def on_colourFaseCvoltaje(self, event):
        self.dibujar_voltaje()

    def on_colourFaseAcorriente(self, event):
        self.dibujar_corriente()

    def on_colourFaseBcorriente(self, event):
        self.dibujar_corriente()

    def on_colourFaseCcorriente(self, event):
        self.dibujar_corriente()

    def on_faseA_voltaje(self, event):
        self.dibujar_voltaje()

    def on_faseB_voltaje(self, event):
        self.dibujar_voltaje()

    def on_faseC_voltaje(self, event):
        self.dibujar_voltaje()

    def on_faseA_corriente(self, event):
        self.dibujar_corriente()

    def on_faseB_corriente(self, event):
        self.dibujar_corriente()

    def on_faseC_corriente(self, event):
        self.dibujar_corriente()

    def on_import_file(self, event):
        # Podemos crear un evento extra para abrir un fichero de texto
        """ Abrir un fichero"""
        #print self.actual
        self.dirname = self.actual
        # Abrimos una ventana de dialogo de fichero para seleccionar algun fichero
        dlg = wx.FileDialog(self, "Elige un fichero", self.dirname, "", "*.xls", wx.OPEN)
        # Si se selecciona alguno => OK
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()   # Guardamos el nombre del fichero
            self.dirname = dlg.GetDirectory()   # Y el directorio
            # Abrimos el archivo de excel, se imprime la ruta, el nombre del archivo
            # y el numero de pesta?as en el archivo
            self.libro = xlrd.open_workbook(self.dirname+"/"+self.filename)
            #print (self.dirname)
            #print (self.filename)
            self.actual=self.dirname
            #print(self.libro.nsheets)
            self.cargar_datos()
        dlg.Destroy()   # Finalmente destruimos la ventana de di?logo

    def cargar_datos(self):
        r=0
        #Se extraen los datos de la pestanha de datos
        for r in range(int(self.libro.nsheets)):
            if self.libro.sheet_by_index(r).name == "origen":
                p = r
        pest = self.libro.sheet_by_index(p)
        for i in range(pest.ncols):
            for j in range(pest.nrows):
                temporal=[]
                if i==0:
                    temporal.append(pest.cell_value(rowx=j, colx=i))
                    Ia.append(pest.cell_value(rowx=j, colx=i))
                if i==1:
                    temporal.append(pest.cell_value(rowx=j, colx=i))
                    Ib.append(pest.cell_value(rowx=j, colx=i))
                if i==2:
                    temporal.append(pest.cell_value(rowx=j, colx=i))
                    Ic.append(pest.cell_value(rowx=j, colx=i))
                if i==3:
                    temporal.append(pest.cell_value(rowx=j, colx=i))
                    In.append(pest.cell_value(rowx=j, colx=i))
                if i==4:
                    temporal.append(pest.cell_value(rowx=j, colx=i))
                    Va.append(pest.cell_value(rowx=j, colx=i))
                if i==5:
                    temporal.append(pest.cell_value(rowx=j, colx=i))
                    Vb.append(pest.cell_value(rowx=j, colx=i))
                if i==6:
                    temporal.append(pest.cell_value(rowx=j, colx=i))
                    Vc.append(pest.cell_value(rowx=j, colx=i))
        dlg = wx.TextEntryDialog(None, "Ingrese el valor en el que ocurre la falla",
        "Ciclo de falla", "576")
        if dlg.ShowModal() == wx.ID_OK:
            self.inicioFalla = int(dlg.GetValue())
        self.finFalla=self.inicioFalla+32
        #print(self.inicioFalla)
        #print(self.finFalla)
        dlg.Destroy()

        dlg = wx.TextEntryDialog(None, "Ingrese el valor prefalla",
        "Ciclo pre-falla", "1")
        if dlg.ShowModal() == wx.ID_OK:
            self.inicioPreFalla = int(dlg.GetValue())
        self.finPreFalla=self.inicioPreFalla+32
        #print(inicioPreFalla)
        dlg.Destroy()
        #codigo utilizado para habilitar las graficas de los canales de transmision
        self.m_checkBox1.SetValue(True)
        self.m_checkBox2.SetValue(True)
        self.m_checkBox3.SetValue(True)
        self.m_checkBox4.SetValue(True)
        self.m_checkBox5.SetValue(True)
        self.m_checkBox6.SetValue(True)
        self.asignarFalla()
        self.asignarPreFalla()
        self.dibujar_voltaje()
        self.dibujar_corriente()
        self.m_textCtrl3.SetValue(self.takagi())

    def asignarFalla(self):
        a=(-1+np.multiply(math.sqrt(3),1j))/2;
        Tfs=[[1,1,1],[1,np.power(a,2),a],[1,a,np.power(a,2)]]
        Tfs=np.divide(Tfs,3)
        #for x in range(self.inicioFalla,self.finFalla):
        for x in range(self.inicioFalla,self.finFalla):
            ia.append(Ia[x])
            ib.append(Ib[x])
            ic.append(Ic[x])
            i1n.append(In[x])
            va.append(Va[x])
            vb.append(Vb[x])
            vc.append(Vc[x])

        self.IA=np.dot(u,ia)
        self.IB=np.dot(u,ib)
        self.IC=np.dot(u,ic)
        self.IN=np.dot(u,i1n)
        self.VC=np.dot(u,vc)
        Ifase=[]
        Ifase.append(self.IC)
        Ifase.append(self.IA)
        Ifase.append(self.IB)
        #print(self.IC)

        #en la secuencia del codigo de matlab se hallan los fasores de un ciclo con cierto corrimiento,
        #en nuestro caso decidimos no manejarlo

        #Iseck=Tfs*Ifase
        Iseck=np.dot(Tfs,Ifase)
        #print(Iseck)
        self.I0=Iseck[0]
        self.I1=Iseck[1]
        self.I2=Iseck[2]

    def asignarPreFalla(self):

        #for x in range(self.inicioPreFalla,self.finPreFalla):
        for x in range(self.inicioPreFalla,self.finPreFalla):
            iprea.append(Ia[x])
            ipreb.append(Ib[x])
            iprec.append(Ic[x])
        Ipre.append(np.dot(u,iprea))
        Ipre.append(np.dot(u,ipreb))
        Ipre.append(np.dot(u,iprec))

    def takagi(self):
        Z= complex(0.01,0.1)
        If=self.IC-Ipre[2]

        #print(If)


        a= If/(3*self.I0)
        T= np.angle(a)

        #print (T)
        s= np.exp(-T*1j)


        self.I0=complex(self.I0.real,-self.I0.imag)

        #print(s)
        x=(self.VC*self.I0*s).imag/(Z*self.IC*self.I0*s).imag
        #print(x)
        return str(x)

    def on_about(self, event):
        msg = """ 
        Aplicacion desarrollada conjuntamente entre la
        Empresa de Enegia de Cundinamarca y el LABE para la
        localizacion de fallas en la red electrica de cundinamarca\n
        Laboratorio de Ensayos Electricos Industriales - Labe
        Contacto: labe_fibog@unal.edu.co
        """
        #image = wx.Image("labe.png", wx.BITMAP_TYPE_ANY)
        #image.set_from_file("labe.png")
        #image.set_from_stock(Gtk.STOCK_CAPS_LOCK_WARNING, Gtk.IconSize.DIALOG)
        #image.show()
        #messagedialog.set_image(image)

        

        
        dlg = wx.MessageDialog(self, msg, "Acerca de ...", wx.OK)
        #dlg.set_image(image)
        dlg.ShowModal()
        dlg.Destroy()


    def salir(self, event):
        dlg = wx.MessageDialog( self, 'Realmente desea salir del programa?', 'Aviso', wx.YES_NO | wx.ICON_QUESTION )
        salir = dlg.ShowModal()
        dlg.Destroy()
        if wx.ID_YES == salir :
            self.Destroy()



###########################################################################
## Class MyPanel3                                                         #
###########################################################################


if __name__ == '__main__':
    app = wx.App()
    app.frame = Aplicacion()
    app.frame.Show()
    app.MainLoop()


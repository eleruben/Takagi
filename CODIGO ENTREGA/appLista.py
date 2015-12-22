# -*- coding: cp1252 -*-
import wx
import wx.xrc
import math
import matplotlib
import xlrd
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

import networkx as nx
import os

import numpy as np

import Circuito

import claseComtrade

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

total=[]


N=32
T1=np.arange(0,(N-1)*2*math.pi/N+0.001,2*math.pi/N)
#T1=0:2*math.pi/N:(N-1)*2*math.pi/N;
u=2*np.exp(np.multiply(1j,T1))/(math.sqrt(3)*N);


###########################################################################
##                          Class Aplicacion                              #
###########################################################################

class Aplicacion ( wx.Frame ):

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
        
        #######
		#wx.Frame.__init__ ( self, None, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		#self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

    def crear_panel_main(self):
        #Panel que contiene el listBook
        principalSizer = wx.BoxSizer( wx.VERTICAL )
        self.m_listbook1 = wx.Listbook( self, wx.ID_ANY, style=wx.BK_DEFAULT )
        #Creacion de los paneles del List Book
        #Panel de inicio
        self.m_panel1 = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #Panel de graficas de las senhales
        self.m_panel2 = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #Panel de localizacion de falla en el grafo
        self.m_panel3 = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #Panel de reporte
        self.m_panel4 = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        ###########################################################################
        ##                          PANEL DE INICIO                               #
        ###########################################################################
        #Creacion de los BoxSizer que contienen los elementos del panel de inicio
        panelInicioSizer = wx.BoxSizer( wx.HORIZONTAL )
        letrasInicioSizer = wx.BoxSizer( wx.VERTICAL )
        cajasInicioSizer = wx.BoxSizer( wx.VERTICAL )
        '''self.m_button5 = wx.Button( self.m_panel1, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
        panelInicioSizer.Add( self.m_button5, 0, wx.ALL, 5 )'''
        
        #Objeto de tipo Static text que tiene por nombre Tipo de falla
        self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Tipo de falla", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        self.m_staticText1.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        letrasInicioSizer.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        #Espacio entre Tipo de falla y Canal de falla
        letrasInicioSizer.AddSpacer(8)
        
        #Objeto de tipo Static text que tiene por nombre Canal de falla
        self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Canal de falla", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        letrasInicioSizer.Add( self.m_staticText2, 0, wx.ALL, 5 )
        #Espacio entre Canal de falla y Distancia
        letrasInicioSizer.AddSpacer(8)
        #Objeto de tipo Static text que tiene por nombre Distancia
        self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Distancia", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        self.m_staticText3.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        letrasInicioSizer.Add( self.m_staticText3, 0, wx.ALL, 5 )
        panelInicioSizer.Add( letrasInicioSizer, 0, wx.EXPAND, 5 )
        
        ######Boxsizer que contiene los datos asociados a el BoxSizer4, que se muestran cuando se importan los datos
        #de la falla
        self.m_textCtrl1 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl1.Enable( False )
        cajasInicioSizer.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
        
        self.m_textCtrl2 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl2.Enable( False )
        cajasInicioSizer.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
        
        self.m_textCtrl3 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl3.Enable( False )
        cajasInicioSizer.Add( self.m_textCtrl3, 0, wx.ALL, 5 )
        
        panelInicioSizer.Add( cajasInicioSizer, 0, wx.EXPAND, 5 )
        self.m_panel1.SetSizer( panelInicioSizer )
        self.m_panel1.Layout()
        panelInicioSizer.Fit( self.m_panel1 )
        self.m_listbook1.AddPage( self.m_panel1, u"INICIO", True )
        ###########################################################################
        ##                          PANEL DE GRAFICAS                             #
        ###########################################################################
        
        #Creacion de los BoxSizer que contienen los elementos del panel de graficas
        panelGraficasSizer = wx.BoxSizer( wx.VERTICAL )
        
        #Boxsizers de tension
        panelTensionSizer = wx.BoxSizer( wx.VERTICAL )
        panelTensionGraficaSizer = wx.BoxSizer( wx.VERTICAL )
        panelTensionCheckBoxsSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        #Boxsizers de corriente
        panelCorrienteSizer = wx.BoxSizer( wx.VERTICAL )
        panelCorrienteGraficaSizer = wx.BoxSizer( wx.VERTICAL )
        panelCorrienteCheckBoxsSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        #Creacion de los paneles que contienen las graficas
        self.m_panelTension = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panelCorriente = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

	
        self.dpi = 100

        #Figura que corresponde a la grafica de tensiones de falla del circuito
        self.fig1 = Figure((10.0, 2.8), dpi=self.dpi)
        self.canvas_voltaje = FigCanvas(self.m_panelTension, -1, self.fig1)


        self.axes_voltaje = self.fig1.add_subplot(111)


        self.axes_voltaje.set_xlabel('t')
        self.axes_voltaje.set_ylabel('V(t)')
        
        panelTensionGraficaSizer.Add( self.m_panelTension, 0, wx.EXPAND |wx.ALL, 5)
        #panelTensionSizer contiene el grafico y los checkboxs
        panelTensionSizer.Add( panelTensionGraficaSizer, 0, wx.EXPAND, 5 )
        self.m_checkBox1 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE A", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl1= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.GREEN, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseAvoltaje, self.ColourPickerCtrl1)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseA_voltaje, self.m_checkBox1)
        panelTensionCheckBoxsSizer.Add( self.m_checkBox1, 0, wx.ALL, 5 )
        panelTensionCheckBoxsSizer.Add( self.ColourPickerCtrl1, 0, wx.ALL, 5 )
        
        self.m_checkBox2 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE B", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl2= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.BLUE, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseBvoltaje, self.ColourPickerCtrl2)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseB_voltaje, self.m_checkBox2)
        panelTensionCheckBoxsSizer.Add( self.m_checkBox2, 0, wx.ALL, 5 )
        panelTensionCheckBoxsSizer.Add( self.ColourPickerCtrl2, 0, wx.ALL, 5 )
        
        self.m_checkBox3 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE C", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl3= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.RED, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseCvoltaje, self.ColourPickerCtrl3)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseC_voltaje, self.m_checkBox3)
        panelTensionCheckBoxsSizer.Add( self.m_checkBox3, 0, wx.ALL, 5 )
        panelTensionCheckBoxsSizer.Add( self.ColourPickerCtrl3, 0, wx.ALL, 5 )
        
        panelTensionSizer.Add( panelTensionCheckBoxsSizer, 0, wx.EXPAND, 5 )
        
        #Figura que corresponde a la grafica de corrientes de falla del circuito
        self.fig2 = Figure((10.0, 2.8), dpi=self.dpi)
        self.canvas_corriente = FigCanvas(self.m_panelCorriente, -1, self.fig2)
        self.axes_corriente = self.fig2.add_subplot(111)
        self.axes_corriente.set_xlabel('t')
        self.axes_corriente.set_ylabel('I(t)')
        
        panelCorrienteGraficaSizer.Add( self.m_panelCorriente, 0, wx.EXPAND |wx.ALL, 5)
        
        #panelCorrienteSizer contiene el grafico y los checkboxs
        panelCorrienteSizer.Add( panelCorrienteGraficaSizer, 0, wx.EXPAND, 5 )
        
        self.m_checkBox4 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE A", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl4= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.GREEN, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseAcorriente, self.ColourPickerCtrl4)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseA_corriente, self.m_checkBox4)
        panelCorrienteCheckBoxsSizer.Add( self.m_checkBox4, 0, wx.ALL, 5 )
        panelCorrienteCheckBoxsSizer.Add( self.ColourPickerCtrl4, 0, wx.ALL, 5 )
        
        self.m_checkBox5 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE B", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl5= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.BLUE, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseBcorriente, self.ColourPickerCtrl5)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseB_corriente, self.m_checkBox5)
        panelCorrienteCheckBoxsSizer.Add( self.m_checkBox5, 0, wx.ALL, 5 )
        panelCorrienteCheckBoxsSizer.Add( self.ColourPickerCtrl5, 0, wx.ALL, 5 )
        
        self.m_checkBox6 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE C", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl6= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.RED, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseCcorriente, self.ColourPickerCtrl6)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseC_corriente, self.m_checkBox6)
        panelCorrienteCheckBoxsSizer.Add( self.m_checkBox6, 0, wx.ALL, 5 )
        panelCorrienteCheckBoxsSizer.Add( self.ColourPickerCtrl6, 0, wx.ALL, 5 )
        
        panelCorrienteSizer.Add( panelCorrienteCheckBoxsSizer, 0, wx.EXPAND, 5 )
        #Se agregar los BoxSizer de tension y corriente a el BoxSizer de graficasSizer
        panelGraficasSizer.Add( panelTensionSizer, 0, wx.EXPAND, 5 )
        panelGraficasSizer.Add( panelCorrienteSizer, 0, wx.EXPAND, 5 )
        self.m_panel2.SetSizer( panelGraficasSizer )
        self.m_panel2.Layout()
        panelGraficasSizer.Fit( self.m_panel2 )
        self.m_listbook1.AddPage( self.m_panel2, u"GRAFICAS", False )
        
        ###########################################################################
        ##              PANEL DE UBICACION DE LA FALLA                            #
        ###########################################################################
        panelUbicacionSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.m_panelUbicacion = wx.Panel( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        retorno=Circuito.Grafos()
        distancia=13
        Grafo=Circuito.punto_falla(retorno,distancia)
        #Circuito.imprimir_grafo(imprimible)
        color=nx.get_node_attributes(Grafo,'color')
        values = [color.get(node, 50) for node in Grafo.nodes()]
        #imprimible de circuito
        pos=nx.get_node_attributes(Grafo,'pos')
        #print("las posiciones son "+str(pos))
        etiquetas={}
        for n in pos.keys():
            #print(str(n)+" tiene "+str(pos[n][0]))
            etiquetas[n]=[pos[n][0]+0.5,pos[n][1]+0.5]
            #print("la posicion de las etiquetas son "+str(etiquetas))
            color=nx.get_node_attributes(Grafo,'color')
        
        #Figura que corresponde a la grafica de la ubicacion de la falla en el circuito
        #self.fig3 = Figure((10.0, 2.8), dpi=self.dpi)
        #self.canvas_ubicacion = FigCanvas(self.m_panelUbicacion , -1, self.fig3)

        #self.fig3 = Figure((10.0, 2.8), dpi=self.dpi)
        self.fig3 = plt.figure(figsize=(10.0,20.0))
        self.canvas_ubicacion = FigCanvas(self.m_panel3, -1, self.fig3)
        
        
        #self.axes_ubicacion = self.fig3.add_subplot(111)
        
        #self.axes_ubicacion.set_xlabel('t')
        #self.axes_ubicacion.set_ylabel('I(t)')
        
        nx.draw_networkx_nodes(Grafo,pos,node_size=100,node_color=values,alpha=1.0)
        nx.draw_networkx_edges(Grafo,pos,alpha=0.4,node_size=0,width=1,edge_color='k')
        nx.draw_networkx_labels(Grafo,etiquetas,fontsize=14)
        #nx.draw_networkx_labels(Grafo,pos,labels)
        #nx.draw_networkx(Grafo,pos, arrows=False, with_labels=True,node_color=values,ax=ax)
        #plt.savefig("GrafoCaminos.png")
        plt.axis('off')

        panelUbicacionSizer.Add(self.canvas_ubicacion, 0, wx.LEFT | wx.TOP | wx.GROW)
        #self.toolbar = NavigationToolbar(self.canvas)
        #self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        #self.m_panel3.SetSizer(self.vbox)
        #self.vbox.Fit(self)
        
        panelUbicacionSizer.Add( self.m_panelUbicacion, 0, wx.EXPAND |wx.ALL, 5)
        
        #panelCorrienteGraficaSizer.Add( self.m_panelCorriente, 0, wx.EXPAND |wx.ALL, 5)
        
        #f = plt.figure(1)
        #ax = f.add_subplot(1,1,1)
        
        '''for label in val_map:
                ax.plot([0],[0],color=scalarMap.to_rgba(val_map[label]),label=label)'''
        #values = [val_map.get(node, 30) for node in Grafo.nodes()]
        
        #self.fig3.set_facecolor('w')
        #plt.legend(loc='best')
        
        
        #self.fig3.tight_layout()
        
        #nx.draw(Grafo, cmap=plt.get_cmap('jet'), node_color=values)
        
        ###se dibuja el grafo normal
        #nx.draw(Grafo,pos)
        
        ###se dibuja el grafo con etiquetas
        #nx.draw_networkx(Grafo,pos, arrows=True, with_labels=True,node_color=color)
        #nx.draw_networkx(Grafo,pos, arrows=True, with_labels=True,node_color=values)
        
        #self.axes_ubicacion.plot(nx.draw_networkx_nodes(Grafo,pos,node_size=100,node_color=values,alpha=1.0))
        #nx.draw_networkx_edges(Grafo,pos,alpha=0.4,node_size=0,width=1,edge_color='k')
        #nx.draw_networkx_labels(Grafo,etiquetas,fontsize=14)
        #nx.draw_networkx_labels(Grafo,pos,labels)
        #nx.draw_networkx(Grafo,pos, arrows=False, with_labels=True,node_color=values,ax=ax)
        #plt.savefig("GrafoCaminos.png")
        #plt.axis('off')
        #plt.show()
        #self.canvas_ubicacion.draw()
        '''self.fig = plt.figure()
        self.canvas = FigCanvas(self.m_panel3, -1, self.fig)
        G=nx.house_graph()
        pos={0:(0,0),
            1:(1,0),
            2:(0,1),
            3:(1,1),
            4:(0.5,2.0)}

        nx.draw_networkx_nodes(G,pos,node_size=2000,nodelist=[4])
        nx.draw_networkx_nodes(G,pos,node_size=3000,nodelist=[0,1,2,3],node_color='b')
        nx.draw_networkx_edges(G,pos,alpha=0.5,width=6)
        plt.axis('off')
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.toolbar = NavigationToolbar(self.canvas)
        self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        self.m_panel3.SetSizer(self.vbox)
        self.vbox.Fit(self)'''
        
        '''bSizer22 = wx.BoxSizer( wx.VERTICAL )
        self.m_button7 = wx.Button( self.m_panel3, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer22.Add( self.m_button7, 0, wx.ALL, 5 )'''
        bSizer22 = wx.BoxSizer( wx.VERTICAL )
        self.m_button9 = wx.Button( self.m_panel3, wx.ID_ANY, u"Editar grafo", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Bind(wx.EVT_BUTTON, self.editar_grafo, self.m_button9)
        
        bSizer22.Add( self.m_button9, 0, wx.ALL, 5 )
        
        panelUbicacionSizer.Add( bSizer22, 0, wx.EXPAND, 5 )
        
        #panelUbicacionSizer.Add( self.m_button9, 0, wx.EXPAND |wx.ALL, 5)
        
        self.m_panel3.SetSizer( panelUbicacionSizer )
        self.m_panel3.Layout()
        panelUbicacionSizer.Fit( self.m_panel3 )
        self.m_listbook1.AddPage( self.m_panel3, u"UBICACION DE LA FALLA", False )
        ###########################################################################
        ##              PANEL DE REPORTE DE LA FALLA                              #
        ###########################################################################
        ####////////////////////////////////////////////////////////////
        ####////////////////////////////////////////////////////////////
        ####////////////////////////////////////////////////////////////
        ####///////////////VER COMO AGREGAR LAS IMAGENES A LA///////////
        ####/////////////////////LISTBOOK///////////////////////////////
        ####////////////////////////////////////////////////////////////
        ####////////////////////////////////////////////////////////////
        
        bSizer23 = wx.BoxSizer( wx.VERTICAL )
        
        png = wx.Image('labe.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bitmap = wx.Bitmap('labe.png')
        
        #bitmap = wx.Bitmap('labe.bpm')        
        self.algo = wx.StaticBitmap(self.m_panel4, -1, png, (10, 10), (png.GetWidth(), png.GetHeight()))
        
        bSizer23.Add( self.algo, 0, wx.ALL, 5 )
        
        self.m_button8 = wx.Button( self.m_panel4, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer23.Add( self.m_button8, 0, wx.ALL, 5 )
        
        self.m_panel4.SetSizer( bSizer23 )
        self.m_panel4.Layout()
        bSizer23.Fit( self.m_panel4 )
        # Show how to put an image on one of the notebook tabs,
        # first make the image list:
        self.imlist = wx.ImageList(16, 16)
        #source_pog_icon = self.imlist.Add\
        #(wx.Bitmap('labe.png',wx.BITMAP_TYPE_PNG))
        
        source_pog_icon = self.imlist.Add(bitmap)
        
        #idx1 = il.Add(images.Smiles.GetBitmap())
        #self.AssignImageList(il)
        
        # now put an image on the first tab we just created:
        #self.SetPageImage(0, idx1)
        
        self.m_listbook1.AssignImageList(self.imlist)
        ###ANADE EN EL PANEL 1 LA GRAFICA
        self.m_listbook1.SetPageImage(0, source_pog_icon)
        self.m_listbook1.AddPage( self.m_panel4, u"a page", imageId=0 )
		
        principalSizer.Add( self.m_listbook1, 1, wx.EXPAND |wx.ALL, 5 )
        self.SetSizer( principalSizer )
        self.Layout()
        self.Centre( wx.BOTH )



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

        dlg = wx.FileDialog(self, "Elige un fichero", self.dirname, "", "*.CFG", wx.OPEN)
        # Si se selecciona alguno => OK
        if dlg.ShowModal() == wx.ID_OK:

            
            self.dirname = dlg.GetDirectory()   # Y el directorio            
            self.filename = dlg.GetFilename()   # Guardamos el nombre del fichero

            self.filename= self.filename.split('.')[0]
            self.objeto=claseComtrade.comtrade(self.dirname, self.filename)
            #print(self.dirname)
            #print(self.filename)
            #print(self.objeto.cfg)
            self.objeto.config()
            self.objeto.extraerDatos()
            self.nombreEstacion=(self.objeto.cfg['id']['station_name'])
            #print(self.objeto.oscilografia[21])
            #self.objeto.exportTXT()
            #print(str(self.objeto.LALALA()))
            self.objeto.extraerListas()
            #print(self.objeto.arreglo)
            #self.objeto.excel()
            #self.objeto.excelRudas()
            self.cargar_datos(self.objeto.arreglo)
        dlg.Destroy()   # Finalmente destruimos la ventana de di?logo

    #Funcion en donde se cargan los datos
    def cargar_datos(self,arreglo):
        #Se extraen los datos del arreglo proveniente de la importacion
        #de los archivos en el formato comtrade
        #For que se hace en el numero de columnas, 6
        for i in range(len(arreglo[0])):
            #For que se hace en el numero de filas, 832
            for j in range(len(arreglo)):
                temporal=[]
                if i==5:
                    Ia.append(arreglo[j][i])
                if i==4:
                    Ib.append(arreglo[j][i])
                if i==3:
                    Ic.append(arreglo[j][i])
                if i==6:
                    In.append(arreglo[j][i])
                if i==2:
                    Va.append(arreglo[j][i])
                if i==1:
                    Vb.append(arreglo[j][i])
                if i==0:
                    Vc.append(arreglo[j][i])

                    
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
    
    #def reporte(self):
        
    
    

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


    def editar_grafo(self, event):
        dlg = wx.MessageDialog( self, 'Realmente desea salir del programa?', 'Aviso', wx.YES_NO | wx.ICON_QUESTION )
        salir = dlg.ShowModal()
        dlg.Destroy()
        if wx.ID_YES == salir :
            self.Destroy()

    def salir(self, event):
        dlg = wx.MessageDialog( self, 'Realmente desea salir del programa?', 'Aviso', wx.YES_NO | wx.ICON_QUESTION )
        salir = dlg.ShowModal()
        dlg.Destroy()
        if wx.ID_YES == salir :
            self.Destroy()

		
###########################################################################
## Invocacion del main                                                    #
###########################################################################


if __name__ == '__main__':
    app = wx.App()
    app.frame = Aplicacion()
    app.frame.Show()
    app.MainLoop()	


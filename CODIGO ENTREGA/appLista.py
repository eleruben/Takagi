# -*- coding: cp1252 -*-
import wx
import wx.xrc
import math
import matplotlib
import xlrd
from compiler.ast import Break
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
#from claseComtrade import invertir

import lecturaDeSenalesLUCHO as lect
import sys
#import ejemplo2

#import claseGraficas




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
        
        #Todavia no estan habilitados los dos modulos de importacion, REVISAR
        self.m_menu21 = wx.Menu()
        self.m_menuItem6 = wx.MenuItem( self.m_menu21, wx.ID_ANY, u"Formato CFG", wx.EmptyString, wx.ITEM_NORMAL )
        self.Bind(wx.EVT_MENU, self.on_import_file, self.m_menuItem6)
        self.m_menu21.AppendItem( self.m_menuItem6 )
        
        self.m_menuItem7 = wx.MenuItem( self.m_menu21, wx.ID_ANY, u"Formato xls", wx.EmptyString, wx.ITEM_NORMAL )
        self.Bind(wx.EVT_MENU, self.on_import_excel, self.m_menuItem7)
        self.m_menu21.AppendItem( self.m_menuItem7 )
        #self.m_menuItem7.Enable( False )
        #self.m_menuItem7.Enable( False )
        
        self.m_menu1.AppendSubMenu( self.m_menu21, u"Importar" )
        
        #Opcion de Exportar archivos, permite al usuario guardar los graficos de los datos de corriente y
        #tension, al igual que la ubicacion de la fala. Tambien permitira guardar los
        #datos de la falla en un formato xls, tambien se le permite al usuario tener un acceso
        #rapido con el comando "Ctrl - S"
        self.m_menuItem2 = self.m_menu1.Append(-1, "&Exportar\tCtrl-S", "Exportar archivos")
        self.m_menuItem2.Enable( False )
        self.Bind(wx.EVT_MENU, self.on_export_file, self.m_menuItem2)
        
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
        self.m_menuItem4 = self.m_menu2.Append(-1, "&Manual de uso", "Manual de uso")
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
        self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Tipo de falla", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap( -1 )
        self.m_staticText1.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        letrasInicioSizer.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        #Espacio entre Tipo de falla y Canal de falla
        letrasInicioSizer.AddSpacer(8)
        
        #Objeto de tipo Static text que tiene por nombre Fase(s) en falla
        self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Fase(s) en falla", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        letrasInicioSizer.Add( self.m_staticText2, 0, wx.ALL, 5 )
        #Espacio entre Canal de falla y Distancia
        letrasInicioSizer.AddSpacer(8)
        #Objeto de tipo Static text que tiene por nombre Distancia
        self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Distancia (Km)", wx.DefaultPosition, wx.DefaultSize, 0 )
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
        
        
        self.m_staticText4 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Seleccion de fase y color de voltaje", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap( -1 )
        self.m_staticText4.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        #self.m_staticText4.SetForegroundColour(wx.Colour(0,255,0))
        panelTensionCheckBoxsSizer.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        
        
        
        self.m_checkBox1 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE A", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl1= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.GREEN, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseAvoltaje, self.ColourPickerCtrl1)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseA_voltaje, self.m_checkBox1)
        self.m_checkBox1.Enable(False)
        self.m_checkBox1.SetValue(False)
        panelTensionCheckBoxsSizer.Add( self.m_checkBox1, 0, wx.ALL, 5 )
        panelTensionCheckBoxsSizer.Add( self.ColourPickerCtrl1, 0, wx.ALL, 5 )
        
        self.m_checkBox2 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE B", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl2= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.BLUE, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseBvoltaje, self.ColourPickerCtrl2)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseB_voltaje, self.m_checkBox2)
        self.m_checkBox2.Enable(False)
        self.m_checkBox2.SetValue(False)
        panelTensionCheckBoxsSizer.Add( self.m_checkBox2, 0, wx.ALL, 5 )
        panelTensionCheckBoxsSizer.Add( self.ColourPickerCtrl2, 0, wx.ALL, 5 )
        
        self.m_checkBox3 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE C", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl3= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.RED, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseCvoltaje, self.ColourPickerCtrl3)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseC_voltaje, self.m_checkBox3)
        self.m_checkBox3.Enable(False)
        self.m_checkBox3.SetValue(False)
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
        
        self.m_staticText5 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Seleccion de fase y color de corriente", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap( -1 )
        self.m_staticText5.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        panelCorrienteCheckBoxsSizer.Add( self.m_staticText5, 0, wx.ALL, 5 )
        
        self.m_checkBox4 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE A", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl4= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.GREEN, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseAcorriente, self.ColourPickerCtrl4)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseA_corriente, self.m_checkBox4)
        self.m_checkBox4.Enable(False)
        self.m_checkBox4.SetValue(False)
        panelCorrienteCheckBoxsSizer.Add( self.m_checkBox4, 0, wx.ALL, 5 )
        panelCorrienteCheckBoxsSizer.Add( self.ColourPickerCtrl4, 0, wx.ALL, 5 )
        
        self.m_checkBox5 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE B", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl5= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.BLUE, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseBcorriente, self.ColourPickerCtrl5)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseB_corriente, self.m_checkBox5)
        self.m_checkBox5.Enable(False)
        self.m_checkBox5.SetValue(False)
        panelCorrienteCheckBoxsSizer.Add( self.m_checkBox5, 0, wx.ALL, 5 )
        panelCorrienteCheckBoxsSizer.Add( self.ColourPickerCtrl5, 0, wx.ALL, 5 )
        
        self.m_checkBox6 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"FASE C", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ColourPickerCtrl6= wx.ColourPickerCtrl( self.m_panel2,wx.ID_ANY, wx.RED, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE | wx.CLRP_SHOW_LABEL)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_colourFaseCcorriente, self.ColourPickerCtrl6)
        self.Bind(wx.EVT_CHECKBOX, self.on_faseC_corriente, self.m_checkBox6)
        self.m_checkBox6.Enable(False)
        self.m_checkBox6.SetValue(False)
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
        #Colocar la distancia que se extrae del metodo de localizacion REVISAR
        distancia=13
        self.Grafo=Circuito.punto_falla(retorno,distancia)
        #Circuito.imprimir_grafo(Grafo)
        #Circuito.imprimir_grafo(imprimible)
        color=nx.get_node_attributes(self.Grafo,'color')
        self.Values = [color.get(node, 50) for node in self.Grafo.nodes()]
        #imprimible de circuito
        pos=nx.get_node_attributes(self.Grafo,'pos')
        #print("las posiciones son "+str(pos))
        etiquetas={}
        for n in pos.keys():
            #print(str(n)+" tiene "+str(pos[n][0]))
            etiquetas[n]=[pos[n][0]+0.5,pos[n][1]+0.5]
            #print("la posicion de las etiquetas son "+str(etiquetas))
            color=nx.get_node_attributes(self.Grafo,'color')
        
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.zoomEntry = True

        self.fig3 = plt.figure(figsize=(12.0,25.0))
        self.canvas_ubicacion = FigCanvas(self.m_panel3, -1, self.fig3)
        
        #self.ax = self.fig3.add_subplot(111, xlim=(0,1), ylim=(0,1), autoscale_on=False)
        self.ax = self.fig3.add_subplot(111)
        
        nx.draw_networkx_nodes(self.Grafo,pos,node_size=100,node_color=self.Values,alpha=1.0)
        nx.draw_networkx_edges(self.Grafo,pos,alpha=0.4,node_size=0,width=1,edge_color='k')
        nx.draw_networkx_labels(self.Grafo,etiquetas,fontsize=14)
        
        self.canvas_ubicacion.mpl_connect('button_press_event',self.onPress)
        self.canvas_ubicacion.mpl_connect('button_release_event',self.onRelease)
        self.canvas_ubicacion.mpl_connect('motion_notify_event',self.onMotion)
        self.canvas_ubicacion.mpl_connect('scroll_event', self.zoom)
        #self.fig3.canvas.
        
        plt.axis('off')

        panelUbicacionSizer.Add(self.canvas_ubicacion, 0, wx.LEFT | wx.TOP | wx.GROW)
        #self.toolbar = NavigationToolbar(self.canvas_ubicacion)
        #panelUbicacionSizer.Add( self.toolbar, 0, wx.EXPAND |wx.ALL, 5)
        #self.m_panel3.SetSizer(self.self.Vbox)
        #self.self.Vbox.Fit(self)
        
        panelUbicacionSizer.Add( self.m_panelUbicacion, 0, wx.EXPAND |wx.ALL, 5)
        
        #panelCorrienteGraficaSizer.Add( self.m_panelCorriente, 0, wx.EXPAND |wx.ALL, 5)
        
        #f = plt.figure(1)
        #ax = f.add_subplot(1,1,1)
        
        '''for label in self.Val_map:
                ax.plot([0],[0],color=scalarMap.to_rgba(self.Val_map[label]),label=label)'''
        #self.Values = [self.Val_map.get(node, 30) for node in Grafo.nodes()]
        
        #self.fig3.set_facecolor('w')
        #plt.legend(loc='best')
        
        
        #self.fig3.tight_layout()
        
        #nx.draw(Grafo, cmap=plt.get_cmap('jet'), node_color=self.Values)
        
        ###se dibuja el grafo normal
        #nx.draw(Grafo,pos)
        
        ###se dibuja el grafo con etiquetas
        #nx.draw_networkx(Grafo,pos, arrows=True, with_labels=True,node_color=color)
        #nx.draw_networkx(Grafo,pos, arrows=True, with_labels=True,node_color=self.Values)
        
        #self.axes_ubicacion.plot(nx.draw_networkx_nodes(Grafo,pos,node_size=100,node_color=self.Values,alpha=1.0))
        #nx.draw_networkx_edges(Grafo,pos,alpha=0.4,node_size=0,width=1,edge_color='k')
        #nx.draw_networkx_labels(Grafo,etiquetas,fontsize=14)
        #nx.draw_networkx_labels(Grafo,pos,labels)
        #nx.draw_networkx(Grafo,pos, arrows=False, with_labels=True,node_color=self.Values,ax=ax)
        #plt.savefig("GrafoCaminos.png")
        #plt.axis('off')
        #plt.show()
        #self.canself.Vas_ubicacion.draw()
        '''self.fig = plt.figure()
        self.canself.Vas = FigCanself.Vas(self.m_panel3, -1, self.fig)
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
        self.self.Vbox = wx.BoxSizer(wx.VERTICAL)
        self.self.Vbox.Add(self.canself.Vas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.toolbar = NavigationToolbar(self.canself.Vas)
        self.self.Vbox.Add(self.toolbar, 0, wx.EXPAND)
        self.m_panel3.SetSizer(self.self.Vbox)
        self.self.Vbox.Fit(self)'''
        
        '''bSizer22 = wx.BoxSizer( wx.VERTICAL )
        self.m_button7 = wx.Button( self.m_panel3, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer22.Add( self.m_button7, 0, wx.ALL, 5 )'''
        bSizer22 = wx.BoxSizer( wx.VERTICAL )
        self.m_button9 = wx.Button( self.m_panel3, wx.ID_ANY, u"Editar grafo", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Bind(wx.EVT_BUTTON, self.editar_grafo, self.m_button9)
        
        self.m_button10 = wx.Button( self.m_panel3, wx.ID_ANY, u"Actualizar grafo", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Bind(wx.EVT_BUTTON, self.actualizar_grafo, self.m_button10)
        
        bSizer22.Add( self.m_button9, 0, wx.ALL, 5 )
        bSizer22.Add( self.m_button10, 0, wx.ALL, 5 )
        
        panelUbicacionSizer.Add( bSizer22, 0, wx.EXPAND, 5 )
        
        #panelUbicacionSizer.Add( self.m_button9, 0, wx.EXPAND |wx.ALL, 5)
        
        self.m_panel3.SetSizer( panelUbicacionSizer )
        self.m_panel3.Layout()
        panelUbicacionSizer.Fit( self.m_panel3 )
        self.m_listbook1.AddPage( self.m_panel3, u"UBICACION DE LA FALLA", False )
        ###########################################################################
        ##              PANEL DE REPORTE DE LA FALLA                              #
        ###########################################################################
        
        bSizer23 = wx.BoxSizer( wx.VERTICAL )
        #Imagen del logo del laboratorio
        png = wx.Image('LOGO_LABE.png', wx.BITMAP_TYPE_PNG)      
        #self.algo = wx.StaticBitmap(self.m_panel4, -1, png, (10, 10), (png.GetWidth(), png.GetHeight()))
        self.algo = wx.StaticBitmap(self.m_panel4, -1, wx.BitmapFromImage(png),(10, 10), (png.GetWidth(), png.GetHeight()))
        
        bSizer23.Add( self.algo, 0, wx.ALL, 5 )
        
        self.m_button8 = wx.Button( self.m_panel4, wx.ID_ANY, u"Generar reporte", wx.DefaultPosition, wx.DefaultSize, 0 )
        
        
        bSizer23.Add( self.m_button8, 0, wx.ALL, 5 )
        
        self.m_panel4.SetSizer( bSizer23 )
        self.m_panel4.Layout()
        bSizer23.Fit( self.m_panel4 )
        
        #self.m_listbook1.AddPage( self.m_panel4, u"REPORTE", imageId=0 )
        self.m_listbook1.AddPage( self.m_panel4, u"REPORTE", False )
        #Tamanho de las imagenes contenidas en la ImageList
        self.imlist = wx.ImageList(100,100)
        
        #Se anhade la lista de imagenes dentro de el listbook
        self.m_listbook1.AssignImageList(self.imlist)
        
        
        #Graficas de los paneles
        inicio= wx.Bitmap('inicio.png')
        graficas= wx.Bitmap('graficas.png')
        ubicacion= wx.Bitmap('ubicacion.png')
        reporte= wx.Bitmap('reporte.png')
        
        #Se agregan las imagenes a los paneles de la listbook
        self.m_listbook1.SetPageImage(0, self.imlist.Add(inicio))
        self.m_listbook1.SetPageImage(1, self.imlist.Add(graficas))
        self.m_listbook1.SetPageImage(2, self.imlist.Add(ubicacion))
        self.m_listbook1.SetPageImage(3, self.imlist.Add(reporte))
		
        principalSizer.Add( self.m_listbook1, 1, wx.EXPAND |wx.ALL, 5 )
        self.SetSizer( principalSizer )
        self.Layout()
        self.Centre( wx.BOTH )
        
        self.manual=True
        self.faseA=False
        self.faseB=False
        self.faseC=False
        self.carga=False
        
    def onPress(self,event):
        if event.inaxes != self.ax: return
        self.cur_xlim = self.ax.get_xlim()
        self.cur_ylim = self.ax.get_ylim()
        self.press = self.x0, self.y0, event.xdata, event.ydata
        self.x0, self.y0, self.xpress, self.ypress = self.press
    
    def onRelease(self,event):
        self.press = None
        self.canvas_ubicacion.draw()
    
    def onMotion(self,event):
        if self.press is None: return
        if event.inaxes != self.ax: return
        dx = event.xdata - self.xpress
        dy = event.ydata - self.ypress
        self.cur_xlim -= dx
        self.cur_ylim -= dy
        self.ax.set_xlim(self.cur_xlim)
        self.ax.set_ylim(self.cur_ylim)

        self.ax.figure.canvas.draw()
        self.canvas_ubicacion.draw()
    
    def zoom(self,event):
        #base_scale = 0.6
        
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
        if self.zoomEntry: 
            self.new_width = (cur_xlim[1] - cur_xlim[0]) * 1
            self.zoomEntry=False
        #REVISAR LAS POSICIONES QUE SE AJUSTEN AL ZOOM
        
        '''pos=nx.get_node_attributes(self.Grafo,'pos')
        etiquetas={}
        for n in pos.keys():
            #print(str(n)+" tiene "+str(pos[n][0]))
            etiquetas[n]=[pos[n][0]+0.5,pos[n][1]+0.1]
            #print("la posicion de las etiquetas son "+str(etiquetas))
            color=nx.get_node_attributes(self.Grafo,'color')'''
        
        
        '''###arbol binario, agregar los nodos y despues ordenar, cargado a izquierda o derecha dependiendo, 
        la rama mas larga sera la troncal
        '''
        
        if event.button == 'down':
            # cambia con  zoom in 
            #No permite hacer mas zoom in cuando llegue a cierto factor
            if self.new_width > 15:
                scale_factor = 1
            else:
                scale_factor = 1.1
            
        elif event.button == 'up':
            # cambia con zoom out
            #No permite hacer mas zoom out cuando llegue a cierto factor            
            if self.new_width < 1.9:
                scale_factor = 1
            else:
                scale_factor = 0.9
            
            #scale_factor = 0.9
        else:
            # deal with something that should never happen
            scale_factor = 1
            print event.button

        self.new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        self.new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        
        #print ('new_width'+str(self.new_width))
        #print ('new_height'+str(self.new_height))
        
        
        self.ax.set_xlim([xdata - self.new_width * (1-relx), xdata + self.new_width * (relx)])
        self.ax.set_ylim([ydata - self.new_height * (1-rely), ydata + self.new_height * (rely)])
        self.canvas_ubicacion.draw()

    def dibujar_voltaje(self):
        self.axes_voltaje.clear()
        self.axes_voltaje.set_xlabel('t')
        self.axes_voltaje.set_ylabel('V(t)')
        
        
        if self.manual and self.carga:
            '''self.axes_voltaje.plot(self.objetoComtrade.oscilografia[:,8],color= self.ColourPickerCtrl1.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='A')
            self.axes_voltaje.plot(self.objetoComtrade.oscilografia[:,7],color= self.ColourPickerCtrl2.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='B')
            self.axes_voltaje.plot(self.objetoComtrade.oscilografia[:,6],color= self.ColourPickerCtrl3.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='C')'''
            self.axes_voltaje.plot(self.objetoComtrade.oscilografia[:,5],color= self.ColourPickerCtrl1.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='A')
            self.axes_voltaje.plot(self.objetoComtrade.oscilografia[:,4],color= self.ColourPickerCtrl2.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='B')
            self.axes_voltaje.plot(self.objetoComtrade.oscilografia[:,3],color= self.ColourPickerCtrl3.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='C')
        if not self.manual and self.sale:
                       
            if (self.m_checkBox1.IsChecked()):
                self.axes_voltaje.plot(self.va,color= self.ColourPickerCtrl1.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='A')
                self.axes_voltaje.legend()
            if (self.m_checkBox2.IsChecked()):
                self.axes_voltaje.plot(self.vb,color= self.ColourPickerCtrl2.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='B')
                self.axes_voltaje.legend()
            if (self.m_checkBox3.IsChecked()):
                self.axes_voltaje.plot(self.vc,color= self.ColourPickerCtrl3.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='C')
                self.axes_voltaje.legend()
            
        
        
        
        self.m_textCtrl1.SetValue("Monofasica")
        #self.m_textCtrl2.SetValue("C")
        #self.m_textCtrl1.IsModified(False)

        self.canvas_voltaje.draw()
    
    
    

    def dibujar_corriente(self):
        self.axes_corriente.clear()
        self.axes_corriente.set_xlabel('t')
        self.axes_corriente.set_ylabel('I(t)')
        if self.manual and self.carga:
            #Caso en que ya se haya seleccionado la fase en falla
            if self.faseA or self.faseB or self.faseC:
                self.axes_corriente.set_title('Seleccione el ciclo prefalla')
            else:
                self.axes_corriente.set_title('Seleccione la fase en falla')
                self.m_staticText5.SetLabel("Seleccione la fase en falla")
            self.axes_corriente.plot(self.objetoComtrade.oscilografia[:,11],color= self.ColourPickerCtrl4.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='A')
            self.axes_corriente.plot(self.objetoComtrade.oscilografia[:,10],color= self.ColourPickerCtrl5.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='B')
            self.axes_corriente.plot(self.objetoComtrade.oscilografia[:,9],color= self.ColourPickerCtrl6.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='C')
            self.axes_corriente.legend()
        if not self.manual and self.sale:
            self.m_staticText5.SetLabel("Seleccion de fase y color de corriente")
            self.m_staticText5.SetForegroundColour(wx.Colour(0,0,0))
            
            if self.faseA:
                self.m_checkBox4.Enable(False)
            if self.faseB:
                self.m_checkBox5.Enable(False)
            if self.faseC:
                self.m_checkBox6.Enable(False)
                
            if (self.m_checkBox4.IsChecked()):
                self.axes_corriente.plot(self.ia,color= self.ColourPickerCtrl4.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='A')
                self.axes_corriente.legend()
            if (self.m_checkBox5.IsChecked()):
                self.axes_corriente.plot(self.ib,color= self.ColourPickerCtrl5.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='B')
                self.axes_corriente.legend()
            if (self.m_checkBox6.IsChecked()):
                self.axes_corriente.plot(self.ic,color= self.ColourPickerCtrl6.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='C')
                self.axes_corriente.legend()
        
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
        #Caso en que se este haciendo la seleccion manual
        if self.manual:
            #Caso en que la fase A esta seleccionada y se habilita la seleccion de las fallas
            if self.m_checkBox4.IsChecked():
                self.faseA=True
                #self.axes_corriente.set_title('Seleccione el ciclo prefalla')
                self.dibujar_corriente()
                self.m_staticText5.SetLabel("Falla en fase A")
                self.m_staticText5.SetForegroundColour(wx.Colour(0,0,0))
            #Caso en que la fase A esta se deshabilita y se pide nuevamente la seleccionde la fase en falla
            else:
                self.grafica_dentro_panel()
                self.faseA=False
                self.m_staticText5.SetLabel("Seleccione la fase en falla")
                self.m_staticText5.SetForegroundColour(wx.Colour(255,0,0))
        ######################################TERMINAR DE REVISAR QUE SOLO SE HABILITE UNO PARA EXTRAER LA FASE EN FALLA
            #Caso en que la fase B esta seleccionada y se deshabilita porque solo se trabajan fallas monofasicas
            if self.m_checkBox5.IsChecked():
                self.faseB=False
                self.m_checkBox5.SetValue(False)
            #Caso en que la fase C esta seleccionada y se deshabilita porque solo se trabajan fallas monofasicas
            if self.m_checkBox6.IsChecked():
                self.faseC=False
                self.m_checkBox6.SetValue(False)
        #Caso en que se este haciendo la seleccion manual
        else:
            self.dibujar_corriente()

    def on_faseB_corriente(self, event):
        #Caso en que se este haciendo la seleccion manual
        if self.manual:
            #Caso en que la fase B esta seleccionada y se habilita la seleccion de las fallas
            if self.m_checkBox5.IsChecked():
                self.faseB=True
                self.dibujar_corriente()
                #self.axes_corriente.set_title('Seleccione el ciclo prefalla')
                self.m_staticText5.SetLabel("Falla en fase B")
                self.m_staticText5.SetForegroundColour(wx.Colour(0,0,0))
            #Caso en que la fase B esta se deshabilita y se pide nuevamente la seleccionde la fase en falla
            else:
                self.grafica_dentro_panel()
                self.faseB=False
                self.m_staticText5.SetLabel("Seleccione la fase en falla")
                self.m_staticText5.SetForegroundColour(wx.Colour(255,0,0))
        ######################################TERMINAR DE REVISAR QUE SOLO SE HABILITE UNO PARA EXTRAER LA FASE EN FALLA
            #Caso en que la fase A esta seleccionada y se deshabilita porque solo se trabajan fallas monofasicas
            if self.m_checkBox4.IsChecked():
                self.faseA=False
                self.m_checkBox4.SetValue(False)
            #Caso en que la fase C esta seleccionada y se deshabilita porque solo se trabajan fallas monofasicas
            if self.m_checkBox6.IsChecked():
                self.faseC=False
                self.m_checkBox6.SetValue(False)
        #Caso en que se este haciendo la seleccion manual
        else:
            self.dibujar_corriente()
            
        
        
        
        '''#Caso en que se este haciendo la seleccion manual
        if self.manual:
            if self.m_checkBox4.IsChecked():
                self.m_checkBox4.SetValue(False)
            if self.m_checkBox6.IsChecked():
                self.m_checkBox6.SetValue(False)
        else:
            self.dibujar_corriente()'''

    def on_faseC_corriente(self, event):
        #Caso en que se este haciendo la seleccion manual
        if self.manual:
            #Caso en que la fase C esta seleccionada y se habilita la seleccion de las fallas
            if self.m_checkBox6.IsChecked():
                self.faseC=True
                #self.axes_corriente.set_title('Seleccione el ciclo prefalla')
                self.dibujar_corriente()
                self.m_staticText5.SetLabel("Falla en fase C")
                self.m_staticText5.SetForegroundColour(wx.Colour(0,0,0))
            #Caso en que la fase C esta se deshabilita y se pide nuevamente la seleccionde la fase en falla
            else:
                self.grafica_dentro_panel()
                self.faseC=False
                self.m_staticText5.SetLabel("Seleccione la fase en falla")
                self.m_staticText5.SetForegroundColour(wx.Colour(255,0,0))
        ######################################TERMINAR DE REVISAR QUE SOLO SE HABILITE UNO PARA EXTRAER LA FASE EN FALLA
            #Caso en que la fase A esta seleccionada y se deshabilita porque solo se trabajan fallas monofasicas
            if self.m_checkBox4.IsChecked():
                self.faseA=False
                self.m_checkBox4.SetValue(False)
            #Caso en que la fase B esta seleccionada y se deshabilita porque solo se trabajan fallas monofasicas
            if self.m_checkBox5.IsChecked():
                self.faseB=False
                self.m_checkBox5.SetValue(False)
        #Caso en que se este haciendo la seleccion manual
        else:
            self.dibujar_corriente()
        
        
        '''#Caso en que se este haciendo la seleccion manual
        if self.manual:
            
            if self.m_checkBox4.IsChecked():
                self.m_checkBox4.SetValue(False)
            if self.m_checkBox5.IsChecked():
                self.m_checkBox5.SetValue(False)
                
        else:
            self.dibujar_corriente()'''
    
    def inicializar(self):
        
        #Se dibujan nuevamente los paneles de voltaje y de corriente
        self.axes_corriente.clear()
        self.canvas_corriente.draw()
        self.axes_voltaje.clear()
        self.canvas_voltaje.draw()
        
        #Se inicializa el valor de los text control
        self.m_textCtrl2.SetValue("")
        self.m_textCtrl3.SetValue("")
        
        #Se inicializan variables de control
        self.faseA=False
        self.faseB=False
        self.faseC=False
        self.manual=True
        self.carga=True
        self.inicioPreFalla =0
        self.sale=False
        self.click1=False
        self.click2=False
        self.xant=0
        self.yant=0
        
        #Se inicializan variables de almacenamiento de datos
        
        
        self.muestras=[]
        
        self.Ia=[]
        self.Ib=[]
        self.Ic=[]
        self.In=[]
        self.Va=[]
        self.Vb=[]
        self.Vc=[]
        
        self.IA=0
        self.IB=0
        self.IC=0
        
        self.VA=0
        self.VB=0
        self.VC=0
    
        self.ia=[]
        self.ib=[]
        self.ic=[]
        self.i1n=[]
        self.va=[]
        self.vb=[]
        self.vc=[]
        self.iprea=[]
        self.ipreb=[]
        self.iprec=[]
        self.Ifase=[]
        self.Ipre=[]
        
        self.total=[]
        
        #Se deshabilitan los check box 
        self.m_checkBox1.Enable(False)
        self.m_checkBox2.Enable(False)
        self.m_checkBox3.Enable(False)                    
        self.m_checkBox4.Enable(False)
        self.m_checkBox5.Enable(False)
        self.m_checkBox6.Enable(False)
                        
        self.m_checkBox1.SetValue(False)
        self.m_checkBox2.SetValue(False)
        self.m_checkBox3.SetValue(False)
        self.m_checkBox4.SetValue(False)
        self.m_checkBox5.SetValue(False)
        self.m_checkBox6.SetValue(False)

        N=32
        self.T1=np.arange(0,(N-1)*2*math.pi/N+0.001,2*math.pi/N)
        self.u=2*np.exp(np.multiply(1j,self.T1))/(math.sqrt(3)*N);

    #Funcion que se invoca en el evento de importacion de los datos desde el comtrade
    def on_import_file(self, event):
        # Podemos crear un evento extra para abrir un fichero de texto
        """ Abrir un fichero"""
        
        #Llamado a la funcion para inicializar los self.Valores, lo que permite
        #hacer self.Varios import durante la ejecucion de la aplicacion
        self.dirname = self.actual

        dlg = wx.FileDialog(self, "Elige un fichero", self.dirname, "", "*.CFG", wx.OPEN)
        # Si se selecciona alguno => OK
        if dlg.ShowModal() == wx.ID_OK:
            self.inicializar()    
             
            
            self.dirname = dlg.GetDirectory()   # Y el directorio            
            self.filename = dlg.GetFilename()   # Guardamos el nombre del fichero

            self.filename= self.filename.split('.')[0]
            
            #Objeto de tipo comtrade creado a partir del archivo contrade .CFG Y .DAT
            self.objetoComtrade=claseComtrade.comtrade(self.dirname, self.filename)
            
            self.objetoComtrade.config()
            self.objetoComtrade.extraerDatos()
            self.nombreEstacion=(self.objetoComtrade.cfg['id']['station_name'])
            self.objetoComtrade.extraerListas()
            #print(self.objetoComtrade.oscilografia)
            self.cargar_datos(self.objetoComtrade.arreglo)
            #print('arreglo')
            #print(self.objetoComtrade.arreglo)
            
            #Se habilita el modulo de exportacion de los datos en formato de excel
            self.m_menuItem2.Enable(True)
        # Finalmente destruimos la ventana de dialogo    
        dlg.Destroy()   
    
    
    
    #Funcion que se invoca en el evento de importacion de los datos desde un archivo excel
    def on_import_excel(self, event):
        # Podemos crear un evento extra para abrir un fichero de texto
        """ Abrir un fichero"""
        
        #Llamado a la funcion para inicializar los self.Valores, lo que permite
        #hacer self.Varios import durante la ejecucion de la aplicacion
        self.dirname = self.actual

        dlg = wx.FileDialog(self, "Elige un fichero", self.dirname, "", "*.xls" , wx.OPEN)
        # Si se selecciona alguno => OK
        if dlg.ShowModal() == wx.ID_OK:
            self.inicializar()     
            
            self.dirname = dlg.GetDirectory()   # Y el directorio            
            self.filename = dlg.GetFilename()   # Guardamos el nombre del fichero
            
            self.objetoComtrade=claseComtrade.comtrade(self.dirname, self.filename)
            self.objetoComtrade.generarOscilografiaExcel()
            
            self.cargar_datos(self.objetoComtrade.arreglo)
            self.m_menuItem2.Enable(True)
        # Finalmente destruimos la ventana de dialogo    
        dlg.Destroy()  
    
        
    #Funcion que se invoca en el evento de exportacion de los datos    
    def on_export_file(self, event):
        self.dirname = self.actual
        dlg = wx.FileDialog(self, "Elige un fichero", self.dirname, self.filename, "*.xls", wx.SAVE | wx.OVERWRITE_PROMPT)
        guarda=False
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname  = dlg.GetDirectory()
            self.filename = dlg.GetFilename()
            self.objetoComtrade.excelRudas(self.dirname,self.filename)
            guarda=True
        dlg.Destroy()
        
        #Caso en que se guarda con exito el archivo
        msg = """ 
        Se ha guardado con exito el archivo
        """       
        if guarda:
            dlg1 = wx.MessageDialog(self, msg, "Guardado exitoso", wx.OK)
            dlg1.ShowModal()
            dlg1.Destroy()

    #Funcion en donde se cargan los datos
    def cargar_datos(self,arreglo):
        #Se extraen los datos del arreglo proveniente de la importacion
        #de los archivos en el formato comtrade
        #For que se hace en el numero de columnas, 6
        for i in range(len(arreglo[0])):
            #For que se hace en el numero de filas, 832
            for j in range(len(arreglo)):
                if i==5:
                    self.Ia.append(arreglo[j][i])
                if i==4:
                    self.Ib.append(arreglo[j][i])
                if i==3:
                    self.Ic.append(arreglo[j][i])
                if i==6:
                    self.In.append(arreglo[j][i])
                if i==2:
                    self.Va.append(arreglo[j][i])
                if i==1:
                    self.Vb.append(arreglo[j][i])
                if i==0:
                    self.Vc.append(arreglo[j][i])
        
        #Procedimiento para verificar si la señal de la FASE C se puede analizar de forma automatica
        [sirve, iniPre, iniFalla, Difn]=lect.Verificar(self.objetoComtrade.oscilografia[:,0],self.objetoComtrade.oscilografia[:,9])        
        if (sirve==1 and self.manual):
            
            self.m_textCtrl2.SetValue("C")
            self.inicioFalla=iniFalla
            self.finFalla=self.inicioFalla+32
            self.inicioPreFalla=iniPre
            self.finPreFalla=self.inicioPreFalla+32
            self.manual=False
            self.faseC=True
            
        
        
        #Procedimiento para verificar si la señal de la FASE B se puede analizar de forma automatica
        [sirve, iniPre, iniFalla, Difn]=lect.Verificar(self.objetoComtrade.oscilografia[:,0],self.objetoComtrade.oscilografia[:,10])
        if (sirve==1 and self.manual):
            
            self.m_textCtrl2.SetValue("B")
            self.inicioFalla=iniFalla
            self.finFalla=self.inicioFalla+32
            self.inicioPreFalla=iniPre
            self.finPreFalla=self.inicioPreFalla+32
            self.manual=False
            self.faseB=True
        
        
        #Procedimiento para verificar si la señal de la FASE A se puede analizar de forma automatica            
        [sirve, iniPre, iniFalla, Difn]=lect.Verificar(self.objetoComtrade.oscilografia[:,0],self.objetoComtrade.oscilografia[:,11])
        if (sirve==1 and self.manual):
            
            self.m_textCtrl2.SetValue("A")
            self.inicioFalla=iniFalla
            self.finFalla=self.inicioFalla+32
            self.inicioPreFalla=iniPre
            self.finPreFalla=self.inicioPreFalla+32
            self.manual=False
            self.faseA=True

        if self.manual:
            seleccion=wx.MessageDialog(None, 'Seleccione el ciclo prefalla y ciclo de falla en la grafica', 'Seleccion de ciclos',  style=wx.OK)
            seleccion.ShowModal()
            self.inicioPreFalla=0
            self.sale=False
            self.grafica_dentro_panel()
            
        else:
            seleccion=wx.MessageDialog(None, 'Se realizo automaticamente la seleccion de los ciclos', 'Seleccion automatica exitosa',  style=wx.OK)
            seleccion.ShowModal()
            self.m_checkBox1.Enable(True)
            self.m_checkBox2.Enable(True)
            self.m_checkBox3.Enable(True)
            self.m_checkBox4.Enable(True)
            self.m_checkBox5.Enable(True)
            self.m_checkBox6.Enable(True)
                        
            self.m_checkBox1.SetValue(True)
            self.m_checkBox2.SetValue(True)
            self.m_checkBox3.SetValue(True)
            self.m_checkBox4.SetValue(True)
            self.m_checkBox5.SetValue(True)
            self.m_checkBox6.SetValue(True)
            self.asignarFalla()
            self.asignarPreFalla()
            self.sale=True
            self.dibujar_voltaje()
            self.dibujar_corriente()
            self.m_textCtrl3.SetValue(self.takagi())
            #self.sale=True
            #self.manual=True
        
        #self.analisis_grafica()
        
            
        '''#Entra en el caso que no se haya podido analizar la señal de forma manual    
        if not self.manual:
            ############RETOMAR
            archivo=
            self.objetoGrafico=claseGraficas(self.dirname, self.filename,archivo)

            #self.objetoGrafico.analisis_grafica()'''
            

        '''ejemplo2.analisis_grafica(self.dirname,self.filename)
        self.inicioFalla=ejemplo2.iniFalla
        self.finFalla=self.inicioFalla+32'''
        
        
        '''
        self.inicioFalla=576    
        self.finFalla=self.inicioFalla+32
        self.inicioPreFalla = 1
        self.finPreFalla=self.inicioPreFalla+32'''
        
        '''dlg = wx.TextEntryDialog(None, "Ingrese el self.Valor en el que ocurre la falla",
        "Ciclo de falla", "576")
        if dlg.ShowModal() == wx.ID_OK:
            self.inicioFalla = int(dlg.GetValue())
        self.finFalla=self.inicioFalla+32
        #print(self.inicioFalla)
        #print(self.finFalla)
        dlg.Destroy()

        dlg = wx.TextEntryDialog(None, "Ingrese el self.Valor prefalla",
        "Ciclo pre-falla", "1")
        if dlg.ShowModal() == wx.ID_OK:
            self.inicioPreFalla = int(dlg.GetValue())
        self.finPreFalla=self.inicioPreFalla+32
        #print(inicioPreFalla)
        dlg.Destroy()'''
            
        


    #def inicializar_grafica(self):
        #def __init__(self, carpeta, nombre, oscilografia):
        #def __init__(self, carpeta, nombre):
        #self.carpeta=carpeta
        #self.nombre=nombre
        #self.iniFalla=0
        #self.iniPre=0
        #self.uno=True
        #self.dos=False
        #self.A=oscilografia[:,11]
        #self.B=oscilografia[:,10]
        #self.C=oscilografia[:,9]
        
        #self.ax = plt.subplot(111)
        #self.ax = self.figa.add_subplot(1,1,1)
    
    def grafica_dentro_panel(self):
        
        #Grafica de voltaje
        self.dibujar_voltaje()
        
        #Texto indicador
        self.m_staticText5.SetLabel("Seleccione la fase en falla")
        self.m_staticText5.SetForegroundColour(wx.Colour(255,0,0))
        
        #Variables de control
        self.inicioPreFalla =0
        self.inicioFalla=0
        self.sale=False
        #self.click=False
        
        self.axes_corriente.clear()
        
        self.axes_corriente.set_xlabel('t')
        self.axes_corriente.set_ylabel('I(t)')
        
        self.m_checkBox4.Enable(True)
        self.m_checkBox5.Enable(True)
        self.m_checkBox6.Enable(True)
        
        self.axes_corriente.plot(self.objetoComtrade.oscilografia[:,11],color= self.ColourPickerCtrl4.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='A')
        self.axes_corriente.plot(self.objetoComtrade.oscilografia[:,10],color= self.ColourPickerCtrl5.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='B')
        self.axes_corriente.plot(self.objetoComtrade.oscilografia[:,9],color= self.ColourPickerCtrl6.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='C')
        self.axes_corriente.set_title('Seleccione la fase en falla')
        #self.axes_corriente.title(u'Seleccione el ciclo prefalla')  # Ponemos un titulo superior
        self.axes_corriente.legend()  # Creamos la caja con la leyenda
        
        
        
        binding_id = self.canvas_corriente.mpl_connect('motion_notify_event', self.on_move)
        #self.canvas_corriente.mpl_connect('button_press_event', self.on_click)
        self.canvas_corriente.mpl_connect('button_release_event', self.on_click)
        self.canvas_corriente.draw()
    
        
        if "test_disconnect" in sys.argv:
            print("disconnecting console coordinate printout...")
            self.axes_corriente.disconnect(binding_id)
        
        
        '''#plt.ion()  # Ponemos el modo interactivo
        #plt.axvspan(-0.5,0.5, alpha = 0.25)
        plt.show(False)
        plt.draw()
        plt.close(self.fig3)
        
        
        if (self.m_checkBox4.IsChecked()):
            self.axes_corriente.plot(self.ia,color= self.ColourPickerCtrl4.GetColour().GetAsString(wx.C2S_HTML_SYNTAX))
        if (self.m_checkBox5.IsChecked()):
            self.axes_corriente.plot(self.ib,color= self.ColourPickerCtrl5.GetColour().GetAsString(wx.C2S_HTML_SYNTAX))
        if (self.m_checkBox6.IsChecked()):
            self.axes_corriente.plot(self.ic,color= self.ColourPickerCtrl6.GetColour().GetAsString(wx.C2S_HTML_SYNTAX))'''
        #self.canvas_corriente.draw()
    
        

    def on_move(self,event):
        # get the x and y pixel coords
        x, y = event.x, event.y

        if event.inaxes:
            if not self.sale and (self.faseA or self.faseB or self.faseC):
                ax = event.inaxes  # the axes instance
                #print('data coords %f %f' % (event.xdata, event.ydata))
                self.axes_corriente.clear()
                #self.axes_corriente.cla()                
                #plt.ion()
                #plt.clf()
                #print ('inicio on move esta en '+str(self.inicioPreFalla))
                
                #if (self.inicioPreFalla==0):
                
                ##############REVISAR PORQUE EN EL MODO AUTOMATICO LA SEGUNDA VEZ NO ENTRA AL SEGUNDO CLICK ######################
                if not self.click1:
                    #Titulo para el caso de asignar el ciclo prefalla
                    self.axes_corriente.set_title('Seleccione el ciclo prefalla')
                if self.click2:
                    #Titulo para el caso de asignar el ciclo de falla
                    self.axes_corriente.set_title('Seleccione el ciclo en que ocurre la falla')
                
                self.axes_corriente.plot(self.objetoComtrade.oscilografia[:,11],color= self.ColourPickerCtrl4.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='A')
                self.axes_corriente.plot(self.objetoComtrade.oscilografia[:,10],color= self.ColourPickerCtrl5.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='B')
                self.axes_corriente.plot(self.objetoComtrade.oscilografia[:,9],color= self.ColourPickerCtrl6.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),label='C')
                #Creamos la caja con la leyenda
                self.axes_corriente.legend()
                #Condicional para que no se desplace fuera de la grafica   
                if event.xdata<len(self.objetoComtrade.oscilografia[:,11])-32:
                    self.axes_corriente.axvspan(event.xdata,event.xdata+32, alpha = 0.25)
                self.canvas_corriente.draw()
                #plt.draw()
                #self.axes_corriente.axvspan(event.xdata,event.xdata+32, alpha = 0.25)
                


    def on_click(self,event):
        # get the x and y coords, flip y from top to bottom
        x, y = event.x, event.y
        if  x != self.xant and y != self.yant:
            if event.button == 1:
                if event.inaxes:
                    if not self.sale and (self.faseA or self.faseB or self.faseC):
                        #Se selecciona el ciclo de prefalla en el primer click
                        if not self.click1:
                            self.inicioPreFalla=int(event.xdata)
                            self.finPreFalla=self.inicioPreFalla+32
                            #self.click=True
                            
                        #Se selecciona el ciclo de falla en el segundo click                        
                        if self.click2:
                            self.inicioFalla=int(event.xdata)
                            self.finFalla=self.inicioFalla+32
                            #codigo utilizado para habilitar las graficas de los canales de transmision
                    
                        
                            self.m_checkBox1.Enable(True)
                            self.m_checkBox2.Enable(True)
                            self.m_checkBox3.Enable(True)                    
                            
                            self.m_checkBox1.SetValue(True)
                            self.m_checkBox2.SetValue(True)
                            self.m_checkBox3.SetValue(True)
                            self.m_checkBox4.SetValue(True)
                            self.m_checkBox5.SetValue(True)
                            self.m_checkBox6.SetValue(True)
                        
                            if self.faseA:
                                self.m_textCtrl2.SetValue("A")
                            if self.faseB:
                                self.m_textCtrl2.SetValue("B")
                            if self.faseC:
                                self.m_textCtrl2.SetValue("C")    
                            #self.click=False
                            self.asignarFalla()
                            self.asignarPreFalla()
                            self.sale=True
                            self.manual=False
                            self.dibujar_voltaje()
                            self.dibujar_corriente()
                        
                            self.m_textCtrl3.SetValue(self.takagi())
                            
                        
                        self.click1=True
                        self.click2=True
                        self.xant=x
                        self.yant=y
    
    def asignarFalla(self):
        a=(-1+np.multiply(math.sqrt(3),1j))/2;
        Tfs=[[1,1,1],[1,np.power(a,2),a],[1,a,np.power(a,2)]]
        Tfs=np.divide(Tfs,3)
        #for x in range(self.inicioFalla,self.finFalla):
        for x in range(self.inicioFalla,self.finFalla):
            self.ia.append(self.Ia[x])
            self.ib.append(self.Ib[x])
            self.ic.append(self.Ic[x])
            self.i1n.append(self.In[x])
            self.va.append(self.Va[x])
            self.vb.append(self.Vb[x])
            self.vc.append(self.Vc[x])

        self.IA=np.dot(self.u,self.ia)
        self.IB=np.dot(self.u,self.ib)
        self.IC=np.dot(self.u,self.ic)
        self.IN=np.dot(self.u,self.i1n)
        #VARIABLE NECESARIA PARA EL CALCULO DE TAKAGI, PARA ESTO ES NECESARIO CONOCER LA FASE EN FALLA
        self.VA=np.dot(self.u,self.va)
        self.VB=np.dot(self.u,self.vb)
        self.VC=np.dot(self.u,self.vc)
        Ifase=[]
        Ifase.append(self.IA)
        Ifase.append(self.IB)
        Ifase.append(self.IC)
        #print(self.IC)

        #en la secuencia del codigo de matlab se hallan los fasores de un ciclo con cierto corrimiento,
        #en nuestro caso decidimos no manejarlo

        #Iseck=Tfs*Ifase
        Iseck=np.dot(Tfs,Ifase)
        #print(Iseck)
        self.I0=Iseck[0]#IA
        self.I1=Iseck[1]#IB
        self.I2=Iseck[2]#IC

    def asignarPreFalla(self):

        #for x in range(self.inicioPreFalla,self.finPreFalla):
        for x in range(self.inicioPreFalla,self.finPreFalla):
            self.iprea.append(self.Ia[x])
            self.ipreb.append(self.Ib[x])
            self.iprec.append(self.Ic[x])
        
        #print('iprea '+str(len(self.iprea)))
        #print('ipre '+str(len(self.Ipre)))
        #print('inicio prefalla '+str(self.inicioPreFalla))
        #print('fin prefalla '+str(self.finPreFalla))
        self.Ipre.append(np.dot(self.u,self.iprea))
        self.Ipre.append(np.dot(self.u,self.ipreb))
        self.Ipre.append(np.dot(self.u,self.iprec))
        #print(self.Ipre)

    def takagi(self):
        Z= complex(0.72721,0.0016198)
        
        
        #If=self.IC-self.Ipre[2]
        #if self.m_textCtrl2.GetValue()=='A':
        
        casos = { 'A': [self.IA,self.Ipre[0],self.I0,self.VA], 'B': [self.IB,self.Ipre[1],self.I1,self.VB], 'C': [self.IC,self.Ipre[2],self.I2,self.VC] }
        
        #print (self.m_textCtrl2.GetValue()) 
        
        v=[]
        
        v=casos[self.m_textCtrl2.GetValue()]
        
        #print(v)  
        if self.m_textCtrl2.GetValue() == 'A' or self.m_textCtrl2.GetValue() == 'B' or self.m_textCtrl2.GetValue() == 'C':
            If=v[0]-v[1]
            a= If/(3*v[2])
            T= np.angle(a)
            s= np.exp(-T*1j)
            v[2]=complex(v[2].real,-v[2].imag)
            x=(v[3]*v[2]*s).imag/(Z*v[0]*v[2]*s).imag
            return str(x)
        
        
        '''original
        If=self.IA-self.Ipre[0]
        a= If/(3*self.I0)
        T= np.angle(a)
        s= np.exp(-T*1j)
        self.I0=complex(self.I0.real,-self.I0.imag)
        x=(self.VA*self.I0*s).imag/(Z*self.IA*self.I0*s).imag
        return str(x)
        print ('el otro resultado es'+str(x))'''
    
    #def reporte(self):
        
    
    

    def on_about(self, event):
        '''msg = """ 
        Aplicacion desarrollada conjuntamente entre la
        Empresa de Energia de Cundinamarca y el LABE para la
        localizacion de fallas en la red electrica de Cundinamarca.\n
        Laboratorio de Ensayos Electricos Industriales - LABE
        Contacto: labe_fibog@unal.edu.co
        """
        #image = wx.Image("labe.png", wx.BITMAP_TYPE_ANY)
        #image.set_from_file("labe.png")
        #image.set_from_stock(Gtk.STOCK_CAPS_LOCK_WARNING, Gtk.IconSize.DIALOG)
        #image.show()
        #messagedialog.set_image(image)
        
        dlg = wx.MessageDialog(self, msg, "Acerca de ...", wx.OK|wx.ICON_EXCLAMATION)
        #dlg.set_image(image)
        dlg.ShowModal()
        dlg.Destroy()'''
        
        description = """
        Aplicacion desarrollada conjuntamente entre la
        Empresa de Energia de Cundinamarca y el LABE para la
        localizacion de fallas en la red electrica de Cundinamarca.\n
        Laboratorio de Ensayos Electricos Industriales - LABE
        Contacto: labe_fibog@unal.edu.co
        """
        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('LOGO_LABE.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Localizador de fallas')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2016 LABE-EEC')
        info.SetWebSite('http://www.labe.unal.edu.co/')
        #info.SetLicence(licence)
        #info.AddDeveloper('jan bodnar')
        #info.AddDocWriter('jan bodnar')
        #info.AddArtist('The Tango crew')
        #info.AddTranslator('jan bodnar')
        wx.AboutBox(info)

    #EVENTO SIN IMPLEMENTAR
    def editar_grafo(self, event):
        dlg = wx.MessageDialog( self, 'Realmente desea salir del programa?', 'Aviso', wx.YES_NO | wx.ICON_QUESTION )
        salir = dlg.ShowModal()
        dlg.Destroy()
        if wx.ID_YES == salir :
            self.Destroy()

    #EVENTO SIN IMPLEMENTAR
    def actualizar_grafo(self, event):
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


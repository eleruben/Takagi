# -*- coding: cp1252 -*-
import wx
import wx.grid as wxgrid
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
#from claseComtrade import invertir

import lecturaDeSenalesLUCHO as lect
import sys

import Consultas
import modeloDatos

import re

import clases_Circuito
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
        
        #Extrae el directorio actual en el que se ejecuta el archivo
        self.actual = str(os.getcwd())
        
        #Lista vacia para incluir los ficheros
        self.m_comboBox1Choices = []
         
        #Lista con todos los ficheros del directorio:
        lstDir = os.walk(self.actual)   #os.walk()Lista directorios y ficheros
        
        #Crea una lista de los ficheros s3db que existen en el directorio y los incluye a la lista.
         
        for root, dirs, files in lstDir:
            for fichero in files:
                (nombreFichero, extension) = os.path.splitext(fichero)
                if(extension == ".s3db"):
                    #lstFiles.append(nombreFichero+extension)
                    #print (nombreFichero+extension)
                    self.m_comboBox1Choices.append(nombreFichero)
        
        #Funcion para crear el panel
        self.crear_panel_main()
        
        
        

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
        
        #Modulos de importacion desde archivo CFG y desde Archivo Excel con un formato especifico
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
        ##              PANEL DE UBICACION DE LA FALLA                            #
        ###########################################################################
        panelUbicacionSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.m_panelUbicacion = wx.Panel( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_TabPanel = wx.Notebook( self.m_panel3, wx.ID_ANY, style=wx.BK_DEFAULT )
        
        #Panel de consulta
        self.m_panel5 = wx.Panel( self.m_TabPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        
        #Panel de edicion de grafo
        self.m_panel6 = wx.Panel( self.m_TabPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        
        

             
        #######################################################
        ##       SUBPANEL CONSULTA DE CIRCUITO                #
        #######################################################
        
        bSizerTotal = wx.BoxSizer( wx.VERTICAL )
        
        bSizer22 = wx.BoxSizer( wx.VERTICAL )
        #Sizer de circuitos
        bSizerCircuitos = wx.BoxSizer( wx.HORIZONTAL )
        #Sizer de nodos
        bSizerNodos = wx.BoxSizer( wx.HORIZONTAL )
        #Sizer de lineas
        bSizerLineas = wx.BoxSizer( wx.HORIZONTAL )
        #Sizer de cargas
        bSizerCargas = wx.BoxSizer( wx.HORIZONTAL )
        
        
        self.m_staticText6 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"Circuito", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        self.m_staticText6.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        bSizerCircuitos.Add( self.m_staticText6, 0, wx.ALL, 5 )
        #bSizer22.Add( letrasInicioSizer, 0, wx.EXPAND, 5 )
        
        #REVISAR se deben extraer el nombre de los archivos .s3db
        #self.m_comboBox1Choices = ["yacopi","lalala"]
        #self.m_comboBox1 = wx.ComboBox(self.m_panel3, size=(95, -1), choices=m_comboBox1Choices, style=wx.CB_DROPDOWN)
        self.m_comboBox1 = wx.ComboBox( self.m_panel3, wx.ID_ANY, u"yacopi", wx.DefaultPosition, wx.DefaultSize, self.m_comboBox1Choices, 0 )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxCircuitos, self.m_comboBox1)
        bSizerCircuitos.Add( self.m_comboBox1, 0, wx.ALL, 5 )
        #Se ejecuta para crear la base de datos de yacopi, por si no esta creada
        texto = str(self.m_comboBox1.GetValue())
        self.objetoModelo=modeloDatos.Modelo(texto,True)
        
        bSizerCircuitos.AddSpacer(120)
        
        
        
        self.m_checkBoxNuevoCircuito = wx.CheckBox( self.m_panel3, wx.ID_ANY, u"Nuevo Circuito", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBoxNuevoCircuito.SetValue(False)
        self.Bind(wx.EVT_CHECKBOX, self.on_NuevoCircuito, self.m_checkBoxNuevoCircuito)
        bSizerCircuitos.Add( self.m_checkBoxNuevoCircuito, 0, wx.ALL, 5 )
        
        self.m_textCtrlNuevoCircuito = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrlNuevoCircuito.Enable( False )
        self.valTextCtrlNuevoCircuito=False
        self.Bind(wx.EVT_TEXT, self.EvtTextCtrlNuevoCircuito, self.m_textCtrlNuevoCircuito)
        bSizerCircuitos.Add( self.m_textCtrlNuevoCircuito, 0, wx.ALL, 5 )
        
        self.m_buttonNuevoCircuito = wx.Button( self.m_panel3, wx.ID_ANY, u"+", wx.DefaultPosition, size=wx.Size(20,25), style=0 )
        self.Bind(wx.EVT_BUTTON, self.NuevoCircuito, self.m_buttonNuevoCircuito)
        self.m_buttonNuevoCircuito.Enable(False)
        bSizerCircuitos.Add( self.m_buttonNuevoCircuito, 0, wx.ALL, 5 )
        
        
        bSizerTotal.Add( bSizerCircuitos, 0, wx.ALL, 5 )
        
        self.m_staticText7 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"NODO", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        self.m_staticText7.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        bSizer22.Add( self.m_staticText7, 0, wx.ALL, 5 )
        
        texto = str(self.m_comboBox1.GetValue())
        self.objetoBaseDatos=Consultas.baseDatos(texto)
        
        m_comboBox2Choices = self.objetoBaseDatos.tablaNodos()

        self.m_comboBox2 = wx.ComboBox( self.m_panel5, wx.ID_ANY, u"----", wx.DefaultPosition, wx.DefaultSize, m_comboBox2Choices, 0 )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxNodos, self.m_comboBox2)
        bSizerNodos.Add( self.m_comboBox2, 0, wx.ALL, 5 )
    
        
        bSizer22.Add( bSizerNodos, 0, wx.ALL, 5 )
        
        
        self.reja=wxgrid.Grid(self.m_panel5, wx.ID_ANY)
        self.reja.CreateGrid(1,2)
        nombres=[('Nombre Nodo', 120, False, wxgrid.GridCellStringRenderer()),
            ('Troncal',60, False, wxgrid.GridCellStringRenderer())]
        
        for ind, col in enumerate(nombres):
            self.reja.SetColLabelValue(ind, col[0])
            self.reja.SetColSize(ind, col[1])
            atrib = wxgrid.GridCellAttr()
            atrib.SetReadOnly(col[2])
            atrib.SetRenderer(col[3])
            self.reja.SetColAttr(ind, atrib)
        
        self.reja.Enable(False)
            
        bSizer22.Add( self.reja, 0, wx.ALL, 5 )
        
        
        
        self.m_staticText8 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"LINEA(S)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        self.m_staticText8.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        bSizer22.Add( self.m_staticText8, 0, wx.ALL, 5 )
        #bSizer22.Add( letrasInicioSizer, 0, wx.EXPAND, 5 )
        
        
        
        self.reja1=wxgrid.Grid(self.m_panel5, wx.ID_ANY)
        self.reja1.CreateGrid(5,6)
        nombres=[('Conexion con nodo',120, False, wxgrid.GridCellStringRenderer()),
            ('R0',30, False, wxgrid.GridCellStringRenderer()),
            ('R1',30, False, wxgrid.GridCellStringRenderer()),
            ('X0',30, False, wxgrid.GridCellStringRenderer()),
            ('X1',30, False, wxgrid.GridCellStringRenderer()),
            ('Distancia',120, False, wxgrid.GridCellStringRenderer())]
        
        for ind, col in enumerate(nombres):
            self.reja1.SetColLabelValue(ind, col[0])
            self.reja1.SetColSize(ind, col[1])
            atrib = wxgrid.GridCellAttr()
            atrib.SetReadOnly(col[2])
            atrib.SetRenderer(col[3])
            self.reja1.SetColAttr(ind, atrib)
        
        self.reja1.Enable(False)
            
        bSizerLineas.Add( self.reja1, 0, wx.ALL, 5 )
        bSizer22.Add( bSizerLineas, 0, wx.ALL, 5 )
        
        
        self.m_staticText9 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"CARGA DEL NODO", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        self.m_staticText9.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        bSizer22.Add( self.m_staticText9, 0, wx.ALL, 5 )
        #bSizer22.Add( letrasInicioSizer, 0, wx.EXPAND, 5 )
        
        self.reja2=wxgrid.Grid(self.m_panel5, wx.ID_ANY)
        self.reja2.CreateGrid(1,3)
        nombres=[('Nombre de carga',120, False, wxgrid.GridCellStringRenderer()),
            ('P',60, False, wxgrid.GridCellStringRenderer()),
            ('Q',60, False, wxgrid.GridCellStringRenderer())]
        
        for ind, col in enumerate(nombres):
            self.reja2.SetColLabelValue(ind, col[0])
            self.reja2.SetColSize(ind, col[1])
            atrib = wxgrid.GridCellAttr()
            atrib.SetReadOnly(col[2])
            atrib.SetRenderer(col[3])
            self.reja2.SetColAttr(ind, atrib)
        self.reja2.Enable(False)
        
        bSizerCargas.Add( self.reja2, 0, wx.ALL, 5 )
        
        
        
        #######################################################
        ##       SUBPANEL EDICION DE CIRCUITO                 #
        #######################################################
        
        panelEdicionSizer = wx.BoxSizer( wx.VERTICAL )
        bSizerNod = wx.BoxSizer( wx.HORIZONTAL )
        bSizerEdNodo = wx.BoxSizer( wx.VERTICAL )
        bSizerNombreNodo = wx.BoxSizer( wx.HORIZONTAL )
        bSizerNvoNodo= wx.BoxSizer( wx.VERTICAL )
        
        grid = wx.GridBagSizer(hgap=7, vgap=4)
        gridCarga = wx.GridBagSizer(hgap=3, vgap=2)
        
        bSizerNombres = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizerBotones = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_radioBtn1 = wx.RadioButton( self.m_panel6, -1, " Seleccion nodo de circuito ", style = wx.RB_GROUP )
        
        bSizerEdNodo.Add( self.m_radioBtn1, 0, wx.ALL, 5 )
        
        texto = str(self.m_comboBox1.GetValue())
        self.objetoBaseDatos=Consultas.baseDatos(texto)
        
        
        
        m_comboBox3Choices = self.objetoBaseDatos.tablaNodos()
        #print(m_comboBox2Choices)
        
        #self.filename= self.filename.split('.')[0]
        
        #m_comboBox2Choices = ["1", "2", "3"]
        #self.m_comboBox1 = wx.ComboBox(self.m_panel3, size=(95, -1), choices=m_comboBox1Choices, style=wx.CB_DROPDOWN)
        self.m_comboBox3 = wx.ComboBox( self.m_panel6, wx.ID_ANY, u"----", wx.DefaultPosition, wx.DefaultSize, m_comboBox3Choices, 0 )
        self.valComboBox3=False
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxEdNodos, self.m_comboBox3)
        
        
        ####self.m_comboBox3.SetToolTipString('Selector')
        #CASO DEL RADIO BUTTON self.m_comboBox3.Enable(False)
        bSizerEdNodo.Add( self.m_comboBox3, 0, wx.ALL, 5 )
        
        self.m_staticText10 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Nombre nodo", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        self.m_staticText10.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        bSizerNombreNodo.Add( self.m_staticText10, 0, wx.ALL, 5 )
        
        self.m_textCtrl4 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl4.Enable( False )
        self.valTextCtrl4=False
        self.valTextCtrl4Repetido=False
        self.Bind(wx.EVT_TEXT, self.EvtTextCtrl4, self.m_textCtrl4)
        bSizerNombreNodo.Add( self.m_textCtrl4, 0, wx.ALL, 5 )
        
        bSizerEdNodo.Add( bSizerNombreNodo, 0, wx.ALL, 5 )
        
        ###INSERTAR RADIOBUTTON Y CREAR LOS EVENT_TEXT PARA LOS TEXTCTRL DE LOS CAMPOS DE LINEAS Y DE CARGA   REVISAR
        
        
        bSizerNod.Add( bSizerEdNodo, 0, wx.ALL, 5 )
        bSizerNod.AddSpacer(80)
        
        self.m_radioBtn2 = wx.RadioButton( self.m_panel6, -1, " Nuevo nodo " )
        bSizerNvoNodo.Add( self.m_radioBtn2, 0, wx.ALL, 5 )
        
        
        bSizerNvoNodo.AddSpacer(20)
        self.m_checkBox7 = wx.CheckBox( self.m_panel6, wx.ID_ANY, u"Troncal", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox7.Enable(False)
        self.Bind(wx.EVT_CHECKBOX, self.on_Troncal, self.m_checkBox7)
        
        self.m_checkBox8 = wx.CheckBox( self.m_panel6, wx.ID_ANY, u"Ramal", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox8.Enable(False)
        self.Bind(wx.EVT_CHECKBOX, self.on_Ramal, self.m_checkBox8)
        
        bSizerNvoNodo.Add( self.m_checkBox7, 0, wx.ALL, 5 )
        bSizerNvoNodo.Add( self.m_checkBox8, 0, wx.ALL, 5 )
        
  
        bSizerNod.Add( bSizerNvoNodo, 0, wx.ALL, 5 )
        panelEdicionSizer.Add( bSizerNod, 0, wx.ALL, 5 )
        
        
        self.group1_ctrls = []        
        self.group1_ctrls.append((self.m_radioBtn1, self.m_comboBox3))        
        self.group1_ctrls.append((self.m_radioBtn2, self.m_textCtrl4))

        for radio, text in self.group1_ctrls:
            wx.EVT_RADIOBUTTON( self, radio.GetId(), self.OnGroup1Select )
        
        
        self.m_staticText12 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Conexion", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        self.m_staticText12.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText12, pos=(0,0))
        
        self.m_staticText13 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"R0", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )
        self.m_staticText13.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText13, pos=(0,1))
        
        self.m_staticText14 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"R1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )
        self.m_staticText14.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText14, pos=(0,2))
        
        
        self.m_staticText15 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"X0", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )
        self.m_staticText15.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText15, pos=(0,3))
        
        self.m_staticText16 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"X1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )
        self.m_staticText16.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText16, pos=(0,4))
        
        self.m_staticText17 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Distancia", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )
        self.m_staticText17.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText17, pos=(0,5))
        
        
        
        self.m_comboBox4Choices = []
        self.m_comboBox4 = wx.ComboBox( self.m_panel6, wx.ID_ANY, u"----", wx.DefaultPosition, size=wx.Size(70,25), choices=self.m_comboBox4Choices, style=0 )
        grid.Add(self.m_comboBox4, pos=(1,0))
        self.valComboBox4=False
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxVecino1, self.m_comboBox4)
        
        self.m_textCtrl1R0 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrl1R0=False
        self.Bind(wx.EVT_TEXT, self.EvtText1R0, self.m_textCtrl1R0)
        grid.Add(self.m_textCtrl1R0, pos=(1,1))
        
        self.m_textCtrl1R1 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrl1R1=False
        self.Bind(wx.EVT_TEXT, self.EvtText1R1, self.m_textCtrl1R1)
        grid.Add(self.m_textCtrl1R1, pos=(1,2))
        
        self.m_textCtrl1X0 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrl1X0=False
        self.Bind(wx.EVT_TEXT, self.EvtText1X0, self.m_textCtrl1X0)
        grid.Add(self.m_textCtrl1X0, pos=(1,3))
        
        self.m_textCtrl1X1 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrl1X1=False
        self.Bind(wx.EVT_TEXT, self.EvtText1X1, self.m_textCtrl1X1)
        grid.Add(self.m_textCtrl1X1, pos=(1,4))
        
        self.m_textCtrl1Dis = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrl1Dis=False
        self.Bind(wx.EVT_TEXT, self.EvtText1Dis, self.m_textCtrl1Dis)
        grid.Add(self.m_textCtrl1Dis, pos=(1,5))
        
        self.m_button12 = wx.Button( self.m_panel6, wx.ID_ANY, u"X", wx.DefaultPosition, size=wx.Size(20,25), style=0 )
        self.Bind(wx.EVT_BUTTON, self.EliminarConexion, self.m_button12)
        self.m_button12.Enable(False)
        grid.Add(self.m_button12, pos=(1,6))
        
        #Nueva conexion esta habilitada solo para los casos del nuevo nodo, en el caso de edicion, si se crea una nueva conexion,
        #se estaria creando un ciclo en el circuito
        
        #Evaluar viabilidad de establecer cambio de conexion en el circuito REVISAR
        self.m_staticText18 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Nueva conexion", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )
        self.m_staticText18.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText18, pos=(2,0))
        
        self.m_staticText19 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"R0", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText19.Wrap( -1 )
        self.m_staticText19.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText19, pos=(2,1))
        
        self.m_staticText20 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"R1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText20.Wrap( -1 )
        self.m_staticText20.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText20, pos=(2,2))
        
        
        self.m_staticText21 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"X0", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText21.Wrap( -1 )
        self.m_staticText21.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText21, pos=(2,3))
        
        self.m_staticText22 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"X1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText22.Wrap( -1 )
        self.m_staticText22.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        grid.Add(self.m_staticText22, pos=(2,4))
        
        self.m_staticText23 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Distancia", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText23.Wrap( -1 )
        self.m_staticText23.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        
        grid.Add(self.m_staticText23, pos=(2,5))
        
        
        
        self.m_comboBox5Choices = []
        
        self.m_comboBox5Choices = self.objetoBaseDatos.tablaNodos()
        self.m_comboBox5 = wx.ComboBox( self.m_panel6, wx.ID_ANY, u"----", wx.DefaultPosition, size=wx.Size(70,25), choices=self.m_comboBox5Choices, style=0 )
        grid.Add(self.m_comboBox5, pos=(3,0))
        self.valComboBox5=False
        self.m_comboBox5.Enable(False)
        
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxNuevaConexion, self.m_comboBox5)
        
        
        self.m_textCtrl2R0 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrl2R0=False
        self.Bind(wx.EVT_TEXT, self.EvtText2R0, self.m_textCtrl2R0)
        grid.Add(self.m_textCtrl2R0, pos=(3,1))
        self.m_textCtrl2R0.Enable(False)
        
        
        self.m_textCtrl2R1 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrl2R1=False
        self.Bind(wx.EVT_TEXT, self.EvtText2R1, self.m_textCtrl2R1)
        grid.Add(self.m_textCtrl2R1, pos=(3,2))
        self.m_textCtrl2R1.Enable(False)
        
        
        self.m_textCtrl2X0 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrl2X0=False
        self.Bind(wx.EVT_TEXT, self.EvtText2X0, self.m_textCtrl2X0)
        grid.Add(self.m_textCtrl2X0, pos=(3,3))
        self.m_textCtrl2X0.Enable(False)
        
        
        self.m_textCtrl2X1 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrl2X1=False
        self.Bind(wx.EVT_TEXT, self.EvtText2X1, self.m_textCtrl2X1)
        grid.Add(self.m_textCtrl2X1, pos=(3,4))
        self.m_textCtrl2X1.Enable(False)
        
        
        self.m_textCtrl2Dis = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrl2Dis=False
        self.Bind(wx.EVT_TEXT, self.EvtText2Dis, self.m_textCtrl2Dis)
        grid.Add(self.m_textCtrl2Dis, pos=(3,5))
        self.m_textCtrl2Dis.Enable(False)
        #Adicion de grid de lineas al sizer del panel de edicion
        panelEdicionSizer.Add( grid, 0, wx.ALL, 5 )
        
        panelEdicionSizer.AddSpacer(15)
        
        self.m_checkBoxNodoConCarga = wx.CheckBox( self.m_panel6, wx.ID_ANY, u"Nodo incluye carga", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBoxNodoConCarga.SetValue(False)
        self.Bind(wx.EVT_CHECKBOX, self.on_NodoConCarga, self.m_checkBoxNodoConCarga)
        panelEdicionSizer.Add( self.m_checkBoxNodoConCarga, 0, wx.ALL, 5 )
        
        
        
        panelEdicionSizer.AddSpacer(15)
        
        self.m_staticText24 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Nombre de carga       ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText24.Wrap( -1 )
        self.m_staticText24.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        gridCarga.Add(self.m_staticText24, pos=(0,0))
        
        self.m_staticText19 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"P", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText19.Wrap( -1 )
        self.m_staticText19.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        gridCarga.Add(self.m_staticText19, pos=(0,1))
        
        self.m_staticText20 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Q", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText20.Wrap( -1 )
        self.m_staticText20.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        gridCarga.Add(self.m_staticText20, pos=(0,2))
        
        
        self.m_textCtrlAlias = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrlAlias=False
        self.Bind(wx.EVT_TEXT, self.EvtTextAlias, self.m_textCtrlAlias)
        self.m_textCtrlAlias.SetToolTipString('Nombre de la carga')
        gridCarga.Add(self.m_textCtrlAlias, pos=(1,0))
        
        
        
        self.m_textCtrlP = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrlP=False
        self.Bind(wx.EVT_TEXT, self.EvtTextP, self.m_textCtrlP)
        self.m_textCtrlP.SetToolTipString('Potencia activa')
        gridCarga.Add(self.m_textCtrlP, pos=(1,1))
    
        
        
        self.m_textCtrlQ = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(80,25), style=0 )
        self.valTextCtrlQ=False
        self.Bind(wx.EVT_TEXT, self.EvtTextQ, self.m_textCtrlQ)
        self.m_textCtrlQ.SetToolTipString('Potencia reactiva')
        gridCarga.Add(self.m_textCtrlQ, pos=(1,2))
        #Adicion de grid de cargas al sizer del panel de edicion
        panelEdicionSizer.Add( gridCarga, 0, wx.ALL, 5 )
        
        self.m_textCtrlObs = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(500,30), style=0 )
        self.m_textCtrlObs.Enable(False)
        
        
        
         
        
        #Adicion de grid de cargas al sizer del panel de edicion
        panelEdicionSizer.Add( self.m_textCtrlObs, 0, wx.ALL, 5 )
                       
        self.m_button9 = wx.Button( self.m_panel6, wx.ID_ANY, u"Guardar", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button9.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.GuardarCircuito, self.m_button9)
        bSizerBotones.Add( self.m_button9, 0, wx.ALL, 5 )
        
        self.m_button10 = wx.Button( self.m_panel6, wx.ID_ANY, u"Limpiar", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Bind(wx.EVT_BUTTON, self.LimpiarCircuito, self.m_button10)
        bSizerBotones.Add( self.m_button10, 0, wx.ALL, 5 )
        
        self.m_button11 = wx.Button( self.m_panel6, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Bind(wx.EVT_BUTTON, self.ResetCircuito, self.m_button11)
        bSizerBotones.Add( self.m_button11, 0, wx.ALL, 5 )
        
        
        
        
        #Adicion de sizer de botones al panel de edicion
        panelEdicionSizer.Add( bSizerBotones, 0, wx.ALL, 5 )
        
        self.m_panel6.SetSizer( panelEdicionSizer )
        self.m_panel6.Layout()
        panelEdicionSizer.Fit( self.m_panel6 )
        
        
        
        
        
        bSizer22.Add( bSizerCargas, 0, wx.ALL, 5 )
        
        self.m_panel5.SetSizer( bSizer22 )
        self.m_panel5.Layout()
        bSizer22.Fit( self.m_panel5 )
        
        
        self.m_TabPanel.AddPage(self.m_panel5, u"CONSULTA DE CIRCUITO", True )
        self.m_TabPanel.AddPage(self.m_panel6, u"EDICION DE CIRCUITO", False )
        #bSizer22.Add( self.m_TabPanel, 0, wx.ALL, 5 )
        
        
        bSizerTotal.Add( self.m_TabPanel, 0, wx.ALL, 5 )
        #Variable para el control de los cambios en el modo de edicion
        self.valCambios=False  
        #Metodo para llenar las observaciones
        self.LlenarObservaciones()
        
        #######################################################
        ##       SUBPANEL DE GRAFICA CIRCUITO                 #
        #######################################################
        
                
        self.objetoCircuito=Circuito.claseCircuito(texto)
        #retorno=self.objetoCircuito.Grafos()
        self.Grafo=self.objetoCircuito.Grafos()
        #distancia=40
        #self.Grafo=self.objetoCircuito.punto_falla(retorno,distancia)
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
            etiquetas[n]=[pos[n][0]+0.05,pos[n][1]+0.05]
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

        self.fig3 = plt.figure(figsize=(7.0,25.0))
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
        panelUbicacionSizer.Add( self.m_panelUbicacion, 0, wx.EXPAND |wx.ALL, 5)
        
        

        
        
        
        panelUbicacionSizer.Add( bSizerTotal, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.m_panel3.SetSizer( panelUbicacionSizer )
        self.m_panel3.Layout()
        panelUbicacionSizer.Fit( self.m_panel3 )
        self.m_listbook1.AddPage( self.m_panel3, u"UBICACION DE LA FALLA", True )
        
    
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
        ##                          PANEL DE INFORMACION                          #
        ###########################################################################
        #Creacion de los BoxSizer que contienen los elementos del panel de informacion
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
        self.m_listbook1.AddPage( self.m_panel1, u"INFORMACION", False )
        
        
        ###########################################################################
        ##              PANEL DE REPORTE DE LA FALLA                              #
        ###########################################################################
        
        bSizer23 = wx.BoxSizer( wx.VERTICAL )
        #Imagen del logo del laboratorio
        png = wx.Image('LOGO_LABE.png', wx.BITMAP_TYPE_PNG)      
        self.logo = wx.StaticBitmap(self.m_panel4, -1, wx.BitmapFromImage(png),(10, 10), (png.GetWidth(), png.GetHeight()))
        
        bSizer23.Add( self.logo, 0, wx.ALL, 5 )
        
        self.m_button8 = wx.Button( self.m_panel4, wx.ID_ANY, u"Generar reporte", wx.DefaultPosition, wx.DefaultSize, 0 )
        
        
        bSizer23.Add( self.m_button8, 0, wx.ALL, 5 )
        
        self.m_panel4.SetSizer( bSizer23 )
        self.m_panel4.Layout()
        bSizer23.Fit( self.m_panel4 )
        
        #self.m_listbook1.AddPage( self.m_panel4, u"REPORTE", imageId=0 )
        self.m_listbook1.AddPage( self.m_panel4, u"REPORTE", False )
        
        ###########################################################################
        ##              INSERCION DE LAS GRAFICAS A LOS PANELES                   #
        ###########################################################################
        
        #Tamanho de las imagenes contenidas en la ImageList
        self.imlist = wx.ImageList(100,100)
        
        #Se anhade la lista de imagenes dentro de el listbook
        self.m_listbook1.AssignImageList(self.imlist)
        
        
        
        #Graficas de los paneles
        ubicacion= wx.Bitmap('ubicacion.png')
        graficas= wx.Bitmap('graficas.png')
        informacion= wx.Bitmap('informacion.png')
        reporte= wx.Bitmap('reporte.png')
        
        #Se agregan las imagenes a los paneles de la listbook
        self.m_listbook1.SetPageImage(0, self.imlist.Add(ubicacion))
        self.m_listbook1.SetPageImage(1, self.imlist.Add(graficas))
        self.m_listbook1.SetPageImage(2, self.imlist.Add(informacion))
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
            ERROR=False
            
            try:
                try:
                    self.objetoComtrade.generarOscilografiaExcel()
                    self.cargar_datos(self.objetoComtrade.arreglo)
                    self.m_menuItem2.Enable(True)
                except ValueError:
                    msg='Por favor revise los datos del archivo'
                    ERROR=True  
            except UnboundLocalError or ValueError:
                self.m_menuItem2.Enable(False)
                msg='El archivo debe tener Datos'
                ERROR=True
            if ERROR:
                dlg = wx.MessageDialog(self, msg, "Error", wx.OK|wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
            
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
        #FASE N print(self.objetoComtrade.oscilografia[:,12])
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
    
    
    def EvtComboBoxCircuitos(self,event):        
        texto = str(self.m_comboBox1.GetValue())
        
        self.objetoModelo=modeloDatos.Modelo(texto,False)
        self.m_comboBox2.Clear()
        
        self.objetoBaseDatos=Consultas.baseDatos(texto)
        m_comboBox2Choices = self.objetoBaseDatos.tablaNodos()
        
        self.m_comboBox2.SetItems(m_comboBox2Choices)
        
        self.m_comboBox3.Clear()
        
        m_comboBox3Choices = self.objetoBaseDatos.tablaNodos()
        self.m_comboBox3.SetItems(m_comboBox3Choices)
        
        
        
        
        self.objetoCircuito=Circuito.claseCircuito(texto)
        
        self.ActualizarGrafo()
        
        self.blanquearTabla(self.reja)
        self.blanquearTabla(self.reja1)
        self.blanquearTabla(self.reja2)
        
        self.limpiarPaneles()
    
    
    def ActualizarGrafo(self):
        self.ax.clear()
        texto = str(self.m_comboBox1.GetValue())
        self.objetoCircuito=Circuito.claseCircuito(texto)
        #retorno=self.objetoCircuito.Grafos()
               
        self.Grafo=self.objetoCircuito.Grafos()
        #Metodo para insertar nodos a la misma distancia
        #distancia=30
        #self.Grafo=self.objetoCircuito.punto_falla(self.Grafo,distancia)
        color=nx.get_node_attributes(self.Grafo,'color')
        self.Values = [color.get(node, 50) for node in self.Grafo.nodes()]
        
        pos=nx.get_node_attributes(self.Grafo,'pos')
        etiquetas={}
        for n in pos.keys():
            etiquetas[n]=[pos[n][0]+0.05,pos[n][1]+0.01]
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
        
        
        
        nx.draw_networkx_nodes(self.Grafo,pos,node_size=100,node_color=self.Values,alpha=1.0)
        nx.draw_networkx_edges(self.Grafo,pos,alpha=0.4,node_size=0,width=1,edge_color='k')
        nx.draw_networkx_labels(self.Grafo,etiquetas,fontsize=14)
        
        plt.axis('off')
        
        self.ax.figure.canvas.draw()
        self.canvas_ubicacion.draw()
        
    def EvtComboBoxEdNodos(self,event):
        
        self.valComboBox3=True
        self.valComboBox4=False
        self.m_checkBox7.SetValue(False)
        self.m_checkBox7.Enable(False)   
        self.m_checkBox8.SetValue(False)
        self.m_checkBox8.Enable(False) 
        self.m_textCtrl1R0.SetValue('')
        self.m_textCtrl1R1.SetValue('')
        self.m_textCtrl1X0.SetValue('')
        self.m_textCtrl1X1.SetValue('')
        self.m_textCtrl1Dis.SetValue('')
        self.m_textCtrlAlias.SetValue('')
        self.m_textCtrlP.SetValue('')
        self.m_textCtrlQ.SetValue('')
        self.m_textCtrlAlias.Enable(True) 
        self.m_textCtrlP.Enable(True)
        self.m_textCtrlQ.Enable(True)
        
        texto = str(self.m_comboBox3.GetValue())
        self.m_textCtrl4.SetValue(texto)
        
        m_comboBox4Choices= self.Grafo.neighbors(texto)     
        self.m_comboBox4.SetItems(m_comboBox4Choices)

       
        #Se carga el valor de troncal o ramal del nodo
        troncal=nx.get_node_attributes(self.Grafo,'troncal')
        if troncal[texto]==1:
            self.m_checkBox7.SetValue(True)            
        elif troncal[texto]==0:
            self.m_checkBox8.SetValue(True)
        
        #Caso en que se puede cambiar de troncal a ramal, nodo es troncal, es diferente de B1 y nodo solo tiene un vecino
        if len(m_comboBox4Choices)==1 and self.m_checkBox7.IsChecked() and texto != 'B1':
            self.m_checkBox7.Enable(True)  
            self.m_checkBox8.Enable(True)
        #Caso en que se puede cambiar de ramal a troncal, tiene solo un vecino y este vecino es de tipo troncal
        elif self.m_checkBox8.IsChecked() and len(m_comboBox4Choices)==1 and troncal[self.Grafo.neighbors(texto)[0]]==1  :
            if len(self.Grafo.neighbors(m_comboBox4Choices[0]))==1:
                #NO SE DA EL CASO, PORQUE SI ES UN RAMAL Y EL VECINO SOLO TIENE UN VECINO ESTARIAN SOLO CONECTADOS LOS DOS, SIN UNA LINEA BASE
                pass 
            elif len(self.Grafo.neighbors(m_comboBox4Choices[0]))==2:
                #Si tiene dos vecinos se puede hacer el cambio, ya que uno es el vecino que esta cambiando y el otro es el vecino troncal de abajo
                self.m_checkBox7.Enable(True)  
                self.m_checkBox8.Enable(True)
            elif len(self.Grafo.neighbors(m_comboBox4Choices[0]))==3:
                #Casos en que tenga dos vecinos troncales
                if troncal[self.Grafo.neighbors(m_comboBox4Choices[0])[0]]==1 and troncal[self.Grafo.neighbors(m_comboBox4Choices[0])[1]]==1:
                    pass
                elif troncal[self.Grafo.neighbors(m_comboBox4Choices[0])[0]]==1 and troncal[self.Grafo.neighbors(m_comboBox4Choices[0])[2]]==1:
                    pass
                elif troncal[self.Grafo.neighbors(m_comboBox4Choices[0])[1]]==1 and troncal[self.Grafo.neighbors(m_comboBox4Choices[0])[2]]==1:
                    pass
                #Caso en que no tenga dos vecinos troncales, se puede habilita el paso de troncal a ramal
                elif True:
                    self.m_checkBox7.Enable(True)
                    self.m_checkBox8.Enable(True)
        
        self.m_checkBoxNodoConCarga.Enable(True)

        registros = self.objetoBaseDatos.consultaCargas(str(texto))
        #Caso en que sea diferente de B1
        if(len(registros))>0 and texto!='B1':
            self.m_checkBoxNodoConCarga.SetValue(True)
            try:
                self.m_textCtrlAlias.SetValue(registros[0][0]) 
                self.m_textCtrlP.SetValue(registros[0][1])
                self.m_textCtrlQ.SetValue(registros[0][2])
            except TypeError:
                self.m_checkBoxNodoConCarga.SetValue(False)
                self.m_textCtrlAlias.Enable(False) 
                self.m_textCtrlP.Enable(False)
                self.m_textCtrlQ.Enable(False)
        #Caso en que el nodo seleccionado sea B1
        else:
            if (texto=='B1'):
                self.m_checkBoxNodoConCarga.Enable(False)
            self.m_checkBoxNodoConCarga.SetValue(False)
            self.m_textCtrlAlias.Enable(False) 
            self.m_textCtrlP.Enable(False)
            self.m_textCtrlQ.Enable(False)
        self.LlenarObservaciones()
        
    
    #
    def EvtComboBoxNodos(self,event):
        texto = str(self.m_comboBox2.GetValue())
        registros = self.objetoBaseDatos.consultaNodo(str(texto)) 
        self.dibujarTablas(self.reja,registros)
        
        y=[]
        x= self.Grafo.neighbors(texto)
        for i in range(len(x)):
            distancia=self.Grafo[texto][x[i]]['length']
            r0=self.Grafo[texto][x[i]]['R0']
            r1=self.Grafo[texto][x[i]]['R1']
            x0=self.Grafo[texto][x[i]]['X0']
            x1=self.Grafo[texto][x[i]]['X1']
            #registro = self.objetoBaseDatos.consultaLineas(i)
            f=(x[i],r0,r1,x0,x1,distancia)
            y.append(f)
        registros = self.objetoBaseDatos.consultaLineas(str(texto)) 
        self.dibujarTablas(self.reja1,y)
        registros = self.objetoBaseDatos.consultaCargas(str(texto)) 
        self.dibujarTablas(self.reja2,registros)
        
    
    
    def EvtComboBoxVecino1(self,event):
        #Evento del primer vecino
        self.valComboBox4=True
        self.m_button12.Enable(False)
        
        texto = str(self.m_comboBox3.GetValue())
        texto1 = str(self.m_comboBox4.GetValue())
        
        #Se considera que se puede eliminar una conexion cuando solo exista un vecino
        x= self.Grafo.neighbors(texto1)
        if(len(x)==1) and texto1!='B1'and texto!='B1':
            self.m_button12.Enable(True)
            self.EliminacionNormal=True
        
        x= self.Grafo.neighbors(texto)
        if(len(x)==1) and texto!='B1'and texto1!='B1':
            self.m_button12.Enable(True)
            self.EliminacionNormal=False
        
        r0=self.Grafo[texto][texto1]['R0']
        r1=self.Grafo[texto][texto1]['R1']
        x0=self.Grafo[texto][texto1]['X0']
        x1=self.Grafo[texto][texto1]['X1']
        distancia=self.Grafo[texto][texto1]['length']
        
        self.m_textCtrl1R0.SetValue(str(r0))
        self.m_textCtrl1R1.SetValue(str(r1))
        self.m_textCtrl1X0.SetValue(str(x0))
        self.m_textCtrl1X1.SetValue(str(x1))
        self.m_textCtrl1Dis.SetValue(str(distancia))
        
        self.LlenarObservaciones()
        
        ###REVISAR FALTA LA EDICION DE LOS DATOS, METODO PARA INSERCION, CARGAS, PERO YA SE IMPLEMENTA LA MAYOR PARTE,
        #CONSULTAS SE REALIZA SOBRE LOS NODOS, TAL VEZ NO SEA NECESARIAS LAS RESTRICCIONES EN LOS EDIT NI DELETE
        
        
    
    #Evento correspondiente al checkBox7, con el se controla si un nodo esta en la troncal
    def on_Troncal(self, event):
        
        self.valComboBox5=False
        if self.m_checkBox8.IsChecked():
            self.m_checkBox8.SetValue(False)
        
        if(self.m_radioBtn2.GetValue()):
            self.m_textCtrl2R0.SetValue('')
            self.valTextCtrl2R0=False
            self.m_textCtrl2R1.SetValue('')
            self.valTextCtrl2R1=False
            self.m_textCtrl2X0.SetValue('')
            self.valTextCtrl2X0=False
            self.m_textCtrl2X1.SetValue('')
            self.valTextCtrl2X1=False
            self.m_textCtrl2Dis.SetValue('')
            self.valTextCtrl2Dis=False
            
            self.m_textCtrlAlias.SetValue('')
            self.valTextCtrlAlias=False
            self.m_textCtrlP.SetValue('')
            self.valTextCtrlP=False
            self.m_textCtrlQ.SetValue('')
            self.valTextCtrlQ=False
            
            #Se incluyen todos los nodos a los cuales se les puede agregar un nodo troncal
            troncal=nx.get_node_attributes(self.Grafo,'troncal')
            self.m_comboBox5.Clear()
            for i in troncal:
                if troncal[i]==1 and i!='B1':
                    if len(self.Grafo.neighbors(i))==1 and troncal[self.Grafo.neighbors(i)[0]]==1:
                        m_comboBox5Choices =[]
                        m_comboBox5Choices.append(i)
                        self.m_comboBox5.SetItems(m_comboBox5Choices)
                        
                    elif len(self.Grafo.neighbors(i))==2:
                        if troncal[self.Grafo.neighbors(i)[0]]==0 and troncal[self.Grafo.neighbors(i)[1]]==1:
                            m_comboBox5Choices =[]
                            m_comboBox5Choices.append(i)
                            self.m_comboBox5.SetItems(m_comboBox5Choices)
                        if troncal[self.Grafo.neighbors(i)[1]]==0 and troncal[self.Grafo.neighbors(i)[0]]==1:
                            m_comboBox5Choices =[]
                            m_comboBox5Choices.append(i)
                            self.m_comboBox5.SetItems(m_comboBox5Choices)
                    elif len(self.Grafo.neighbors(i))==3:    
                        if troncal[self.Grafo.neighbors(i)[0]]==1 and troncal[self.Grafo.neighbors(i)[1]]==0 and troncal[self.Grafo.neighbors(i)[2]]==0:
                            m_comboBox5Choices =[]
                            m_comboBox5Choices.append(i)
                            self.m_comboBox5.SetItems(m_comboBox5Choices)
                        if troncal[self.Grafo.neighbors(i)[0]]==0 and troncal[self.Grafo.neighbors(i)[1]]==1 and troncal[self.Grafo.neighbors(i)[2]]==0:
                            m_comboBox5Choices =[]
                            m_comboBox5Choices.append(i)
                            self.m_comboBox5.SetItems(m_comboBox5Choices)
                        if troncal[self.Grafo.neighbors(i)[0]]==0 and troncal[self.Grafo.neighbors(i)[1]]==0 and troncal[self.Grafo.neighbors(i)[2]]==1:
                            m_comboBox5Choices =[]
                            m_comboBox5Choices.append(i)
                            self.m_comboBox5.SetItems(m_comboBox5Choices)
        #Se llama al metodo de llenado de observaciones
        self.LlenarObservaciones()                
                        
    
    #Evento correspondiente al checkBox8, con el se controla si un nodo esta en algun ramal
    def on_Ramal(self, event):
        
        self.valComboBox5=False
        if self.m_checkBox7.IsChecked():
            self.m_checkBox7.SetValue(False)
        
        
        if(self.m_radioBtn2.GetValue()):
            self.m_textCtrl2R0.SetValue('')
            self.valTextCtrl2R0=False
            self.m_textCtrl2R1.SetValue('')
            self.valTextCtrl2R1=False
            self.m_textCtrl2X0.SetValue('')
            self.valTextCtrl2X0=False
            self.m_textCtrl2X1.SetValue('')
            self.valTextCtrl2X1=False
            self.m_textCtrl2Dis.SetValue('')
            self.valTextCtrl2Dis=False
            
            self.m_textCtrlAlias.SetValue('')
            self.valTextCtrlAlias=False
            self.m_textCtrlP.SetValue('')
            self.valTextCtrlP=False
            self.m_textCtrlQ.SetValue('')
            self.valTextCtrlQ=False
            #Se incluyen todos los nodos a los cuales se les puede agregar un nodo ramal
            self.m_comboBox5.Clear()
            m_comboBox5Choices=[]
            troncal=nx.get_node_attributes(self.Grafo,'troncal')
            for i in troncal:
                if i!='B1' and len(self.Grafo.neighbors(i))<4:
                    m_comboBox5Choices.append(i)
            m_comboBox5Choices.sort()
            self.m_comboBox5.SetItems(m_comboBox5Choices)

        #Se llama al metodo de llenado de observaciones
        self.LlenarObservaciones()
            
    def GuardarCircuito(self,event):
        #Caso en que se actualiza un nuevo nodo
        if(self.m_radioBtn1.GetValue()):
            nombre=str(self.m_comboBox3.GetValue())
            vecino=str(self.m_comboBox4.GetValue())
            
            
            if self.m_checkBox7.IsChecked():
                troncal=1
            if self.m_checkBox8.IsChecked():
                troncal=0
            r0=str(self.m_textCtrl1R0.GetValue())
            r1=str(self.m_textCtrl1R1.GetValue())
            x0=str(self.m_textCtrl1X0.GetValue())
            x1=str(self.m_textCtrl1X1.GetValue())
            distancia=str(self.m_textCtrl1Dis.GetValue())
            alias=str(self.m_textCtrlAlias.GetValue())
            p=str(self.m_textCtrlP.GetValue())
            q=str(self.m_textCtrlQ.GetValue())
            #Id del nodo > 2
            id=self.objetoBaseDatos.consultaId(str(nombre))
            #Id del vecino > 1
            linea=self.objetoBaseDatos.consultaId(str(vecino))
            
            #Caso en que el identificador del nodo sea mayor que el del vecino
            if(id>linea):
                datos1 = (nombre, troncal, linea,r0,r1,x0,x1,distancia,alias,p,q,id)
            #Caso en que el identificador del nodo sea menor que el del vecino, es necesario extraer los datos del vecino,
            #ya que la tabla esta conformada de esa forma
            elif(id<linea): 
                troncal=nx.get_node_attributes(self.Grafo,'troncal')
                troncal=troncal[vecino]
                t=id
                id=linea
                linea=t
                
                registros = self.objetoBaseDatos.consultaCargas(str(vecino))
                if(len(registros))>0:
                    self.m_textCtrlAlias.SetValue(registros[0][0]) 
                    self.m_textCtrlP.SetValue(registros[0][1])
                    self.m_textCtrlQ.SetValue(registros[0][2])
                        
                datos1 = (vecino, troncal, linea,r0,r1,x0,x1,distancia,alias,p,q,id)
            
            self.objetoModelo.actualizar(datos1)
            self.ActualizarGrafo()
            
            msg='Se actualizo la conexion entre los nodos '+str(nombre)+'-'+str(vecino)
            dlg = wx.MessageDialog(self, msg, "Actualizacion exitosa", wx.OK |wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            self.limpiarPaneles()
        
        
        
        #Caso en que se inserta un nuevo nodo
        if(self.m_radioBtn2.GetValue()):
            #nombre=str(self.m_comboBox3.GetValue())
            nombre=str(self.m_textCtrl4.GetValue())
            #REVISAR DEPENDIENDO DE LA POSIBILIDAD DE INSERCION TRONCAL O RAMAL m_comboBox5
            vecino=str(self.m_comboBox5.GetValue())
            if self.m_checkBox7.IsChecked():
                troncal=1
            if self.m_checkBox8.IsChecked():
                troncal=0
            r0=str(self.m_textCtrl2R0.GetValue())
            r1=str(self.m_textCtrl2R1.GetValue())
            x0=str(self.m_textCtrl2X0.GetValue())
            x1=str(self.m_textCtrl2X1.GetValue())
            distancia=str(self.m_textCtrl2Dis.GetValue())
            alias=str(self.m_textCtrlAlias.GetValue())
            p=str(self.m_textCtrlP.GetValue())
            q=str(self.m_textCtrlQ.GetValue())
            linea=self.objetoBaseDatos.consultaId(str(vecino))
            
            datos1 = (nombre, troncal, linea,r0,r1,x0,x1,distancia,alias,p,q)            
            self.objetoModelo.insertar(datos1)
            self.ActualizarGrafo()
            
            msg='Se inserto una nueva conexion entre los nodos '+str(nombre)+' - '+str(vecino)
            dlg = wx.MessageDialog(self, msg, "Insercion de nodo exitosa", wx.OK |wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            self.limpiarPaneles()
        
    def LimpiarCircuito(self,event):
        self.limpiarPaneles()
    
    def ResetCircuito(self,event):
        pass
    
    
    def on_NuevoCircuito(self,event):  
        if self.m_checkBoxNuevoCircuito.IsChecked():
            self.m_textCtrlNuevoCircuito.Enable(True)
        else:
            self.m_textCtrlNuevoCircuito.Enable(False)
            self.m_textCtrlNuevoCircuito.SetValue('')
          
    def EvtTextCtrlNuevoCircuito(self,event):
        campo=self.m_textCtrlNuevoCircuito.GetValue()
        if re.match('[a-z]+|[A-Z]+', campo):
            self.m_buttonNuevoCircuito.Enable(True)
        else:
            self.m_textCtrlObs.SetValue('El nombre del nuevo circuito debe empezar por una letra')
            self.m_buttonNuevoCircuito.Enable(False)

    def NuevoCircuito(self,event):
        NombreNuevo=self.m_textCtrlNuevoCircuito.GetValue()
        repetido=False
        #Lista vacia para incluir los ficheros
        for i in self.m_comboBox1Choices:
            if NombreNuevo==i:
                msg='El nombre del circuito ya existe, no se puede crear un circuito con el mismo nombre'
                dlg = wx.MessageDialog(self, msg, "Error", wx.OK|wx.ICON_ERROR)
                self.m_textCtrlNuevoCircuito.SetValue('')
                dlg.ShowModal()
                dlg.Destroy()
                repetido=True
        if not repetido:
            self.objetoModelo=modeloDatos.Modelo(NombreNuevo,False)
            msg="""
            Se creo el nuevo circuito con valores por defecto, 
            por favor ingrese al modulo de edicion y cambie 
            los valores de acuerdo al modelo del circuito
            """
            dlg = wx.MessageDialog(self, msg, "Nuevo circuito agregado", wx.OK|wx.ICON_INFORMATION)
            self.m_textCtrlNuevoCircuito.SetValue('')
            self.m_checkBoxNuevoCircuito.SetValue(False)
            dlg.ShowModal()
            dlg.Destroy()
            
            self.m_comboBox1Choices = []         
            #Lista con todos los ficheros del directorio:
            lstDir = os.walk(self.actual)   #os.walk()Lista directorios y ficheros
            
            #Crea una lista de los ficheros s3db que existen en el directorio y los incluye a la lista.
            for root, dirs, files in lstDir:
                for fichero in files:
                    (nombreFichero, extension) = os.path.splitext(fichero)
                    if(extension == ".s3db"):
                        self.m_comboBox1Choices.append(nombreFichero)
            self.m_comboBox1Choices.sort()
            self.m_comboBox1.SetItems(self.m_comboBox1Choices)
            self.limpiarPaneles()
            
    
    def EvtComboBoxNuevaConexion(self,event):
        self.valComboBox5=True
        self.LlenarObservaciones()
    
    #VALIDACIONES DE LOS EVENT TEXT
    def EvtTextCtrl4(self,event):
        self.valTextCtrl4Repetido=False
        campo=self.m_textCtrl4.GetValue()
        ##REVISAR   VALIDAR QUE EL NOMBRE INGRESADO NO ESTE EN LA LISTA DE NOMBRE DE LOS NODOS
        if re.match('[a-z]+|[A-Z]+', campo):
            self.valTextCtrl4=True
        else:
            self.valTextCtrl4=False
        
        for i in self.Grafo:
            if campo==i:
                self.valTextCtrl4Repetido=True
            
        self.LlenarObservaciones()
    
    def validacion_float(self,campo,variable):
        try:
            campo=float(campo)
            return True
        
        except ValueError:
            return False
    
    def EvtText1R0(self,event):
        
        campo=self.m_textCtrl1R0.GetValue()
        self.valTextCtrl1R0=self.validacion_float(campo,self.valTextCtrl1R0)
        self.LlenarObservaciones()
        try:
            texto = str(self.m_comboBox3.GetValue())
            texto1 = str(self.m_comboBox4.GetValue())
            r0=self.Grafo[texto][texto1]['R0']
            if campo!= str(r0):
                self.valCambios=True
                self.LlenarObservaciones()
        except KeyError:
            pass
    
    def EvtText1R1(self,event):
        campo=self.m_textCtrl1R1.GetValue()
        self.valTextCtrl1R1=self.validacion_float(campo,self.valTextCtrl1R1)
        self.LlenarObservaciones()
        try:
            texto = str(self.m_comboBox3.GetValue())
            texto1 = str(self.m_comboBox4.GetValue())
            r1=self.Grafo[texto][texto1]['R1']
            if campo!= str(r1):
                self.valCambios=True
                self.LlenarObservaciones()
        except KeyError:
            pass
    
    def EvtText1X0(self,event):
        campo=self.m_textCtrl1X0.GetValue()
        self.valTextCtrl1X0=self.validacion_float(campo,self.valTextCtrl1X0)
        self.LlenarObservaciones()
        try:
            texto = str(self.m_comboBox3.GetValue())
            texto1 = str(self.m_comboBox4.GetValue())
            x0=self.Grafo[texto][texto1]['X0']
            if campo!= str(x0):
                self.valCambios=True
                self.LlenarObservaciones()
        except KeyError:
            pass
    
    def EvtText1X1(self,event):
        campo=self.m_textCtrl1X1.GetValue()
        self.valTextCtrl1X1=self.validacion_float(campo,self.valTextCtrl1X1)
        self.LlenarObservaciones()
        try:
            texto = str(self.m_comboBox3.GetValue())
            texto1 = str(self.m_comboBox4.GetValue())
            x1=self.Grafo[texto][texto1]['X1']
            if campo!= str(x1):
                self.valCambios=True
                self.LlenarObservaciones()
        except KeyError:
            pass
    
    def EvtText1Dis(self,event):
        campo=self.m_textCtrl1Dis.GetValue()
        self.valTextCtrl1Dis=self.validacion_float(campo,self.valTextCtrl1Dis)
        if self.valTextCtrl1Dis and float(campo)<=0:
            self.valTextCtrl1Dis=False
        self.LlenarObservaciones()
        try:
            texto = str(self.m_comboBox3.GetValue())
            texto1 = str(self.m_comboBox4.GetValue())
            distancia=self.Grafo[texto][texto1]['length']
            if campo!= str(distancia):
                self.valCambios=True
                self.LlenarObservaciones()
        except KeyError:
            pass
    
    def EvtText2R0(self,event):
        campo=self.m_textCtrl2R0.GetValue()
        self.valTextCtrl2R0=self.validacion_float(campo,self.valTextCtrl2R0)
        self.LlenarObservaciones()
    
    def EvtText2R1(self,event):
        campo=self.m_textCtrl2R1.GetValue()
        self.valTextCtrl2R1=self.validacion_float(campo,self.valTextCtrl2R1)
        self.LlenarObservaciones()
    
    def EvtText2X0(self,event):
        campo=self.m_textCtrl2X0.GetValue()
        self.valTextCtrl2X0=self.validacion_float(campo,self.valTextCtrl2X0)
        self.LlenarObservaciones()
    
    def EvtText2X1(self,event):
        campo=self.m_textCtrl2X1.GetValue()
        self.valTextCtrl2X1=self.validacion_float(campo,self.valTextCtrl2X1)
        self.LlenarObservaciones()
    
    def EvtText2Dis(self,event):
        campo=self.m_textCtrl2Dis.GetValue()
        self.valTextCtrl2Dis=self.validacion_float(campo,self.valTextCtrl2Dis)
        if self.valTextCtrl2Dis and float(campo)<=0:
            self.valTextCtrl2Dis=False
        self.LlenarObservaciones()
    
    def on_NodoConCarga(self,event):
        if self.m_checkBoxNodoConCarga.IsChecked():
            self.m_textCtrlAlias.Enable(True)
            self.m_textCtrlP.Enable(True)
            self.m_textCtrlQ.Enable(True)
        else:
            self.m_textCtrlAlias.Enable(False)
            self.m_textCtrlP.Enable(False)
            self.m_textCtrlQ.Enable(False)
    
    def EvtTextAlias(self,event):
        campo=self.m_textCtrlAlias.GetValue()
        if re.match('[a-z]+|[A-Z]+', campo):
            self.valTextCtrlAlias=True
        else:
            self.valTextCtrlAlias=False
        self.LlenarObservaciones()
        try:
            texto = str(self.m_comboBox3.GetValue())
            registros = self.objetoBaseDatos.consultaCargas(str(texto))
            if(len(registros))>0:
                if campo!= str(registros[0][0]):
                    self.valCambios=True
                    self.LlenarObservaciones()
        except KeyError:
            pass
        
    
    def EvtTextP(self,event):
        campo=self.m_textCtrlP.GetValue()
        self.valTextCtrlP=self.validacion_float(campo,self.valTextCtrlP)
        self.LlenarObservaciones()
        
        try:
            texto = str(self.m_comboBox3.GetValue())
            registros = self.objetoBaseDatos.consultaCargas(str(texto))
            if(len(registros))>0:
                if campo!= str(registros[0][1]):
                    self.valCambios=True
                    self.LlenarObservaciones()
        except KeyError:
            pass
        
    
    def EvtTextQ(self,event):
        campo=self.m_textCtrlQ.GetValue()
        self.valTextCtrlQ=self.validacion_float(campo,self.valTextCtrlQ)
        self.LlenarObservaciones()
        
        try:
            texto = str(self.m_comboBox3.GetValue())
            registros = self.objetoBaseDatos.consultaCargas(str(texto))
            if(len(registros))>0:
                if campo!= str(registros[0][2]):
                    self.valCambios=True
                    self.LlenarObservaciones()
        except KeyError:
            pass
            
    
        
    #Metodo para llenar las observaciones que se puedan presentar            
    def LlenarObservaciones(self):
        #MODO EDICION
        if(self.m_radioBtn1.GetValue()):
            
            self.m_textCtrlObs.SetValue('Modo de edicion de circuito')
            #Caso en que no se ha elegido el nodo
            if not self.valComboBox3: 
                self.m_textCtrlObs.AppendText('\tPor favor seleccione un nodo del circuito para la edicion')
                self.m_button9.Enable(False)
            #Caso en que no se haya elegido el tipo del nodo, troncal/ramal
            elif not self.m_checkBox7.IsChecked() and not self.m_checkBox8.IsChecked() : 
                self.m_textCtrlObs.AppendText('\tPor favor elija el tipo de nodo, troncal/ramal')
                self.m_button9.Enable(False)
            #Caso en que no se ha elegido el nodo vecino    
            elif not self.valComboBox4: 
                self.m_textCtrlObs.AppendText('\tPor favor seleccione el nodo que tiene conexion')
                self.m_button9.Enable(False)
            #Caso en que no se hayan realizado cambios
            elif not self.valCambios: 
                self.m_textCtrlObs.AppendText('\tElija los datos que desee cambiar')
                self.m_button9.Enable(False)
            #Caso en que el valor de R0 no sea un float    
            elif not self.valTextCtrl1R0: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de R0, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que el valor de R1 no sea un float
            elif not self.valTextCtrl1R1: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de R1, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que el valor de X0 no sea un float
            elif not self.valTextCtrl1X0: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de X0, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que el valor de X1 no sea un float
            elif not self.valTextCtrl1X1: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de X1, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que el valor de distancia no sea un float
            elif not self.valTextCtrl1Dis: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de Distancia, debe ser numerico o decimal mayor que 0.0')
                self.m_button9.Enable(False)
            #Caso en que el valor de Alias no empiece por una letra
            elif not self.valTextCtrlAlias and self.m_checkBoxNodoConCarga.IsChecked(): 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de Alias, debe empezar con una letra')
                self.m_button9.Enable(False)
            #Caso en que el valor de P no sea un float
            elif not self.valTextCtrlP and self.m_checkBoxNodoConCarga.IsChecked(): 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de P, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que el valor de Q no sea un float
            elif not self.valTextCtrlQ and self.m_checkBoxNodoConCarga.IsChecked(): 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de Q, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que no tenga ningun error en los datos y haya cambiado un dato
            elif self.valCambios: 
                self.m_textCtrlObs.SetValue('Puede guardar los cambios en el circuito')
                self.m_button9.Enable(True)
        #MODO INSERTAR NUEVO NODO    
        if(self.m_radioBtn2.GetValue()):    
            self.m_textCtrlObs.SetValue('Modo insertar nuevo nodo')
            #Caso en que no se haya ingresado el nombre del nuevo nodo
            if not self.valTextCtrl4:
                self.m_textCtrlObs.AppendText('\tPor favor ingrese el nombre del nodo que se va a insertar')
                self.m_button9.Enable(False)
            #Caso en que el nombre del nodo ingresado ya este en el circuito
            elif self.valTextCtrl4Repetido:
                self.m_textCtrlObs.AppendText('\tEl texto ingresado en el nuevo nodo no puede estar repetido')
                self.m_button9.Enable(False)
            #Caso en que no se haya elegido el tipo del nodo, troncal/ramal
            elif not self.m_checkBox7.IsChecked() and not self.m_checkBox8.IsChecked() : 
                self.m_textCtrlObs.AppendText('\tPor favor elija el tipo de nodo, troncal/ramal')
                self.m_button9.Enable(False)
            #Caso en que no se ha elegido el nodo con el que se establece la nueva conexion
            elif not self.valComboBox5: 
                self.m_textCtrlObs.AppendText('\tPor favor seleccione el nodo para la nueva conexion')
                self.m_button9.Enable(False)
            #Caso en que el valor de R0 no sea un float    
            elif not self.valTextCtrl2R0: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de R0, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que el valor de R1 no sea un float
            elif not self.valTextCtrl2R1: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de R1, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que el valor de X0 no sea un float
            elif not self.valTextCtrl2X0: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de X0, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que el valor de X1 no sea un float
            elif not self.valTextCtrl2X1: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de X1, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que el valor de distancia no sea un float
            elif not self.valTextCtrl2Dis: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de Distancia, debe ser numerico o decimal mayor que 0.0')
                self.m_button9.Enable(False)
            #Caso en que el valor de Alias no empiece por una letra
            elif not self.valTextCtrlAlias: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de Alias, debe empezar con una letra')
                self.m_button9.Enable(False)
            #Caso en que el valor de P no sea un float
            elif not self.valTextCtrlP: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de P, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            #Caso en que el valor de Q no sea un float
            elif not self.valTextCtrlQ: 
                self.m_textCtrlObs.AppendText('\tPor favor revise el valor de Q, debe ser numerico o decimal')
                self.m_button9.Enable(False)
            elif True:
                self.m_textCtrlObs.SetValue('Puede guardar el nuevo nodo y la nueva conexion establecida')
                self.m_button9.Enable(True)
    
    def limpiarPaneles(self):
        self.nuevaLocalizacion()
        self.m_comboBox2.Clear()
        
        m_comboBox2Choices = self.objetoBaseDatos.tablaNodos()
        self.m_comboBox2.SetItems(m_comboBox2Choices)
        
        self.m_comboBox3.Clear()
        self.valComboBox3=False
        m_comboBox3Choices = self.objetoBaseDatos.tablaNodos()
        self.m_comboBox3.SetItems(m_comboBox3Choices)
        
        
        self.m_comboBox4.Clear()
        self.valComboBox4=False
        self.m_comboBox5.Clear()
        self.valComboBox5=False
        m_comboBox5Choices = self.objetoBaseDatos.tablaNodos()
        self.m_comboBox5.SetItems(m_comboBox5Choices)
        
        self.valCambios=False
        
        
        self.m_checkBox7.SetValue(False)
        self.m_checkBox8.SetValue(False)
        self.m_textCtrl4.SetValue('')
        self.valTextCtrl4=False
        self.valTextCtrl4Repetido=False
        self.m_textCtrl1R0.SetValue('')
        self.valTextCtrl1R0=False
        self.m_textCtrl1R1.SetValue('')
        self.valTextCtrl1R1=False
        self.m_textCtrl1X0.SetValue('')
        self.valTextCtrl1X0=False
        self.m_textCtrl1X1.SetValue('')
        self.valTextCtrl1X1=False
        self.m_textCtrl1Dis.SetValue('')
        self.valTextCtrl1Dis=False
        
        self.m_textCtrl2R0.SetValue('')
        self.valTextCtrl2R0=False
        self.m_textCtrl2R1.SetValue('')
        self.valTextCtrl2R1=False
        self.m_textCtrl2X0.SetValue('')
        self.valTextCtrl2X0=False
        self.m_textCtrl2X1.SetValue('')
        self.valTextCtrl2X1=False
        self.m_textCtrl2Dis.SetValue('')
        self.valTextCtrl2Dis=False
        
        
        self.m_checkBoxNodoConCarga.Enable(True)
        self.m_checkBoxNodoConCarga.SetValue(False)
        self.m_textCtrlAlias.Enable(True) 
        self.m_textCtrlAlias.SetValue('')
        self.valTextCtrlAlias=False
        self.m_textCtrlP.Enable(True)
        self.m_textCtrlP.SetValue('')
        self.valTextCtrlP=False
        self.m_textCtrlQ.Enable(True)
        self.m_textCtrlQ.SetValue('')
        self.valTextCtrlQ=False
        self.blanquearTabla(self.reja)
        self.blanquearTabla(self.reja1)
        self.blanquearTabla(self.reja2)
        #self.m_textCtrlObs.SetValue()
        self.m_button12.Enable(False)
        self.LlenarObservaciones()
    
    def EliminarConexion(self,event):
        if self.EliminacionNormal:
            vecino=str(self.m_comboBox4.GetValue())
        else:
            vecino=str(self.m_comboBox3.GetValue())
        msg='¿Esta seguro que desea eliminar el nodo '+str(vecino)+' del circuito?'
        dlg = wx.MessageDialog(self, msg, "Eliminar conexion", wx.YES_NO |wx.ICON_EXCLAMATION)
        if dlg.ShowModal() == wx.ID_YES:
            idVecino=self.objetoBaseDatos.consultaId(str(vecino))
            self.objetoModelo.eliminar(idVecino)
            #Metodo para actualizar el grafo
            self.ActualizarGrafo()
            #Volver a inicalizar los checkbox y los campos
            self.limpiarPaneles()
        dlg.Destroy()
        
    
        
    
    def dibujarTablas(self,rejilla,registros):
        self.numFilas = rejilla.GetNumberRows()
        difFilas = len(registros) - self.numFilas 
        self.blanquearTabla(rejilla)
        
        '''if difFilas > 0: 
            rejilla.AppendRows(difFilas) 
        elif difFilas < 0: 
            rejilla.AppendRows(-difFilas) '''
        for fila, dato in enumerate(registros): 
            for col, valor in enumerate(dato): 
                rejilla.SetCellValue(fila, col, str(valor))  
    
    def blanquearTabla(self,rejilla):
        rejilla.ClearGrid()
    
    
    
    def OnGroup1Select( self, event ):
        radio_sel = event.GetEventObject()
        for radio, texto in self.group1_ctrls:
            if radio is radio_sel:
                texto.Enable(True)
                self.m_comboBox5.Enable(True)
                self.m_textCtrl2R0.Enable(True)
                self.m_textCtrl2R1.Enable(True)
                self.m_textCtrl2X0.Enable(True)
                self.m_textCtrl2X1.Enable(True)
                self.m_textCtrl2Dis.Enable(True)
                
                self.m_comboBox4.Enable(False)
                self.valComboBox4=False
                self.m_textCtrl1R0.Enable(False)
                self.valTextCtrl1R0=False
                self.m_textCtrl1R1.Enable(False)
                self.valTextCtrl1R1=False
                self.m_textCtrl1X0.Enable(False)
                self.valTextCtrl1X0=False
                self.m_textCtrl1X1.Enable(False)
                self.valTextCtrl1X1=False
                self.m_textCtrl1Dis.Enable(False)
                self.valTextCtrl1Dis=False
                self.m_checkBoxNodoConCarga.Enable(True)
                self.m_textCtrlAlias.Enable(True) 
                self.m_textCtrlP.Enable(True)
                self.m_textCtrlQ.Enable(True)
                self.limpiarPaneles()
            else:
                texto.Enable(False)
                self.m_comboBox5.Enable(False)
                self.valComboBox5=False
                self.m_textCtrl2R0.Enable(False)
                self.valTextCtrl2R0=False
                self.m_textCtrl2R1.Enable(False)
                self.valTextCtrl2R1=False
                self.m_textCtrl2X0.Enable(False)
                self.valTextCtrl2X0=False
                self.m_textCtrl2X1.Enable(False)
                self.valTextCtrl2X1=False
                self.m_textCtrl2Dis.Enable(False)
                self.valTextCtrl2Dis=False
                self.m_comboBox4.Enable(True)
                self.m_checkBox7.Enable(True)
                self.m_checkBox8.Enable(True)
                self.m_textCtrl1R0.Enable(True)
                self.m_textCtrl1R1.Enable(True)
                self.m_textCtrl1X0.Enable(True)
                self.m_textCtrl1X1.Enable(True)
                self.m_textCtrl1Dis.Enable(True)
                self.m_checkBoxNodoConCarga.Enable(True)
                self.m_textCtrlAlias.Enable(True) 
                self.m_textCtrlP.Enable(True)
                self.m_textCtrlQ.Enable(True)
                self.limpiarPaneles()
    



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
    
    def nuevaLocalizacion(self):
        #Parametros de las lineas:
        R0 = 0.3864
        R1 = 0.01273
        L0 = 4.1264 * (10 ** -3)
        L1 = 0.9337 * (10 ** -3)
        
        
        #Mediciones subestación:
        #Voltajes
        Va = ( 1.1607e+04 - 3.6131e+02j)/np.sqrt(2)
        Vb = ( -6.1165e+03 - 9.8714e+03j)/np.sqrt(2)
        Vc = (-5.4907e+03 + 1.0233e+04j)/np.sqrt(2)
        Vpre=[Va, Vb, Vc]
        #Corrientes:
        Ia = (2.7342 - 0.1282j)/np.sqrt(2)
        Ib = (-1.4782 - 2.3038j)/np.sqrt(2)
        Ic = (-1.2561 + 2.4320j)/np.sqrt(2)
        Ipre=[Ia, Ib, Ic]
        
        #Mediciones post falla
        VaPost = (1.7875e+03 - 1.0998e+03j)/np.sqrt(2)
        VbPost = (-3.4673e+02 - 2.1806e+03j)/np.sqrt(2)
        VcPost = (-5.4665e+03 + 1.0262e+04j)/np.sqrt(2)
        VPost=[VaPost, VbPost, VcPost]
        
        IaPost= (18.5799 -71.6318j)/np.sqrt(2)
        IbPost= (-64.0093 +32.2525j)/np.sqrt(2)
        IcPost= (-1.3352 + 2.6700j)/np.sqrt(2)
        IPost=[IaPost, IbPost, IcPost]
        
        #Tablas de configuración
        TaNodos = [["ID", "Nombre", "Troncal"]]
        TaNodos=self.objetoBaseDatos.consultaTablaNodos(TaNodos)
        
        '''TaNodos = [["ID", "Nombre", "Troncal"],
               [1, "B1", 1],
               [2, "B2", 1],
               [3, "B3", 1],
               [4, "B4", 1],
               [5, "B5", 0],
               [6, "B6", 0],
               [7, "B7", 1]]'''
        TaLineas = [["ID", "Nombre", "Nodo1", "Nodo2", "R0", "R1", "L0", "L1", "Distancia"]]
        TaLineas=self.objetoBaseDatos.consultaTablaLineas(TaLineas)
        
        '''TaLineas = [["ID", "Nombre", "Nodo1", "Nodo2", "R0", "R1", "L0", "L1", "Distancia"],
                  [1, "Linea1", 1, 2, R0, R1, L0, L1, 30],
                  [2, "Linea2", 2, 3, R0, R1, L0, L1, 15],
                  [3, "Linea3", 3, 4, R0, R1, L0, L1, 10],
                  [4, "Linea4", 2, 5, R0, R1, L0, L1, 8],
                  [5, "Linea5", 3, 6, R0, R1, L0, L1, 20],
                  [6, "Linea6", 4, 7, R0, R1, L0, L1, 19]]'''
        
        TaCargas = [["ID", "Nodo", "Nombre", "P", "Q"],
                  [1, 2, "C2", 8*10**3, 100],
                  [2, 3, "C3", 8*10**3, 100],
                  [3, 4, "C4", 8*10**3, 100],
                  [4, 5, "C5", 8*10**3, 100],
                  [5, 6, "C6", 8*10**3, 100],
                  [6, 7, "C7", 8*10**3, 100]]
        D,tramo=clases_Circuito.Localizacion(Vpre, Ipre,VPost, IPost, TaNodos, TaLineas, TaCargas, 2, 0)
        print(D,tramo)
    
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
        
    
    '''def agregar(self, event):
        pass
        #if self.m_comboBox1.GetStringSelection() not in self.m_comboBox1.SelectAll():
        #    self.m_comboBox1.Append('otro')'''
           

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


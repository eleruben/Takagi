import wx
import wx.xrc
import wx.grid
 
###########################################################################
## Class MyFrame1
###########################################################################
 
class MiForm ( wx.Frame ):
 
    def __init__( self, parent ):
      wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 417,350 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
     
      self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
     
      bSizer1 = wx.BoxSizer( wx.VERTICAL )
     
      self.m_grid1 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
     
      # Grid
      self.m_grid1.CreateGrid( 4, 4 )
      self.m_grid1.EnableEditing( True )
      self.m_grid1.EnableGridLines( True )
      self.m_grid1.EnableDragGridSize( False )
      self.m_grid1.SetMargins( 0, 0 )
     
      # Columns
      self.m_grid1.EnableDragColMove( False )
      self.m_grid1.EnableDragColSize( True )
      self.m_grid1.SetColLabelSize( 30 )
      self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
     
      # Rows
      self.m_grid1.EnableDragRowSize( True )
      self.m_grid1.SetRowLabelSize( 80 )
      self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
     
      # Label Appearance
     
      # Cell Defaults
      self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
      bSizer1.Add( self.m_grid1, 0, wx.ALL, 5 )
     
      self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
      bSizer1.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
     
      fgSizer1 = wx.FlexGridSizer( 0, 4, 0, 0 )
      fgSizer1.SetFlexibleDirection( wx.BOTH )
      fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
     
      self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Producto", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText1.Wrap( -1 )
      fgSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
     
      self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
      fgSizer1.Add( self.m_textCtrl1, 1, wx.ALL|wx.EXPAND, 5 )
     
      self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Codigo", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText2.Wrap( -1 )
      fgSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
     
      self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
      fgSizer1.Add( self.m_textCtrl2, 1, wx.EXPAND|wx.ALL|wx.ALIGN_BOTTOM, 5 )
     
      self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Categoria", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText3.Wrap( -1 )
      fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
     
      m_comboBox1Choices = []
      self.m_comboBox1 = wx.ComboBox( self, wx.ID_ANY, u"Seleccionar", wx.DefaultPosition, wx.DefaultSize, m_comboBox1Choices, 0 )
      fgSizer1.Add( self.m_comboBox1, 0, wx.ALL, 5 )
     
      self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Fecha de ingreso", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText4.Wrap( -1 )
      fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
     
      self.m_datePicker1 = wx.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_DEFAULT )
      fgSizer1.Add( self.m_datePicker1, 1, wx.ALL|wx.EXPAND, 5 )
     
     
      bSizer1.Add( fgSizer1, 1, wx.EXPAND|wx.ALL, 5 )
     
      self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
      bSizer1.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
     
      bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
     
     
      bSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
     
      self.m_button4 = wx.Button( self, wx.ID_ANY, u"Grabar", wx.DefaultPosition, wx.DefaultSize, 0 )
      bSizer2.Add( self.m_button4, 0, wx.ALL, 5 )
     
      self.m_button5 = wx.Button( self, wx.ID_ANY, u"Eliminar", wx.DefaultPosition, wx.DefaultSize, 0 )
      bSizer2.Add( self.m_button5, 0, wx.ALL, 5 )
     
     
      bSizer1.Add( bSizer2, 1, wx.EXPAND|wx.ALL, 5 )
     
     
      self.SetSizer( bSizer1 )
      self.Layout()
      self.m_menubar1 = wx.MenuBar( 0 )
      self.m_menu1 = wx.Menu()
      self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Abrir", wx.EmptyString, wx.ITEM_NORMAL )
      self.m_menu1.AppendItem( self.m_menuItem1 )
     
      self.m_menu1.AppendSeparator()
     
      self.m_menuItem3 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Salir", wx.EmptyString, wx.ITEM_NORMAL )
      self.m_menu1.AppendItem( self.m_menuItem3 )
     
      self.m_menubar1.Append( self.m_menu1, u"Archivos" )
     
      self.SetMenuBar( self.m_menubar1 )
     
     
      self.Centre( wx.BOTH )
     
      # evento click que invoca a la funcion grabar
      self.m_button4.Bind( wx.EVT_LEFT_DOWN, self.Grabar )
     
    def __del__( self ):
      pass
        # creamos un cuadro de dialogo o mensaje personalizado
    def Mensaje(self, msg, title, style):
      dlg = wx.MessageDialog(parent=None, message=msg,
      caption=title, style=style)
      dlg.ShowModal()
      dlg.Destroy()
     
    # Funcion grabar que responde al evento click
    def Grabar( self, event ):
        self.Mensaje("Esto es un evento click!",
                                "Informacion - Tutorial", wx.OK|wx.ICON_INFORMATION)
app = wx.App(False)
frame = MiForm (None)
frame.Show(True)
app.MainLoop()
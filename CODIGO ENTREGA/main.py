import wx
import wx.lib.scrolledpanel
from controls import SimpleGrid
from controls import ListCtrlComboPopup


class GraphFrame(wx.Frame):
    title = 'Demo: Data Trending Tool'

    def __init__(self):
        self.selection = []
        self.displaySize = wx.DisplaySize() 
        wx.Frame.__init__(self, None, -1, self.title,
                 style = wx.DEFAULT_FRAME_STYLE,
                 size = (self.displaySize[0]/2, self.displaySize[1]/2))        
        self.containingpanel = wx.Panel(self, -1)
        self.toppanel = wx.Panel(self, -1)
        self.splittedwin = wx.SplitterWindow(self.containingpanel, wx.ID_ANY, style=wx.SP_3D | wx.SP_BORDER)
        self.splittedwin.SetMinimumPaneSize(20)
        self.gridpanel = wx.lib.scrolledpanel.ScrolledPanel(self.splittedwin,-1, style = wx.SUNKEN_BORDER)        
        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self.splittedwin,-1, style = wx.SUNKEN_BORDER)

        #### GRID
        self.grid = SimpleGrid(self.gridpanel)
        self.gridpanelsizer= wx.BoxSizer(wx.HORIZONTAL)
        self.gridpanelsizer.Add(self.grid, wx.GROW)
        self.gridpanel.SetSizer(self.gridpanelsizer)
        self.gridpanelsizer.Fit(self)             
        #### COMBOBOX
        self.cc = wx.combo.ComboCtrl(self.toppanel, style=wx.CB_READONLY, size=(200,-1), )
        self.cc.SetPopupMaxHeight(140)
        popup = ListCtrlComboPopup(self)
        self.cc.SetPopupControl(popup)
        self.cc.SetText("--select--")
        # Add some items to the listctrl
        for i in range(10):
            popup.AddItem(str(i))

        #### SIZER FOR COMBOBOX 
        self.cbpanelsizer= wx.BoxSizer(wx.HORIZONTAL)
        self.cbpanelsizer.Add(self.cc, border = 5,flag = wx.LEFT)
        self.toppanel.SetSizer(self.cbpanelsizer)


        self.splittedwin.SplitHorizontally(self.gridpanel,self.panel,100)

        ##### SIZER FOR CONTAININGPANEL
        self.cpsizer = wx.BoxSizer(wx.VERTICAL) 
        self.cpsizer.Add(self.splittedwin, 1, wx.EXPAND, 0)
        self.containingpanel.SetSizer(self.cpsizer)
        self.cpsizer.Fit(self.containingpanel)

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(self.toppanel, 0, wx.EXPAND)
        mainsizer.Add(self.containingpanel, 1, wx.EXPAND)
        self.SetSizerAndFit(mainsizer)

        self.panel.SetAutoLayout(1)
        self.panel.SetupScrolling()
        self.gridpanel.SetAutoLayout(1)
        self.gridpanel.SetupScrolling()
        self.draw_plot()

    def draw_plot(self):
        for i in range(10):  
          if i in self.selection:
             self.grid.ShowRow(i)
          else:
             self.grid.HideRow(i) 
        #self.Layout()
        self.gridpanelsizer.Layout()

if __name__ == "__main__":

  app = wx.PySimpleApp()
  app.frame = GraphFrame()
  app.frame.Show()

  app.MainLoop()
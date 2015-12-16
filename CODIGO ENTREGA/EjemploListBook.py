#import images
import wx
import panelOne, panelTwo, panelThree
 
########################################################################
class ListbookDemo(wx.Listbook):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Listbook.__init__(self, parent, wx.ID_ANY, style=
                            wx.BK_DEFAULT
                            #wx.BK_TOP
                            #wx.BK_BOTTOM
                            #wx.BK_LEFT
                            #wx.BK_RIGHT
                            )
        '''# make an image list using the LBXX images
        il = wx.ImageList(32, 32)
        for x in range(3):
            obj = getattr(images, 'LB%02d' % (x+1))
            bmp = obj.GetBitmap()
            il.Add(bmp)
        self.AssignImageList(il)'''
 
        pages = [(panelOne.TabPanel(self), "Panel Oneffffgfhfghfg"),
                 (panelTwo.TabPanel(self), "Panel Two"),
                 (panelThree.TabPanel(self), "Panel Three")]
        imID = 0
        for page, label in pages:
            #self.AddPage(page, label, imageId=imID)
            self.AddPage(page, label)
            imID += 1
 
        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGING, self.OnPageChanging)
 
    #----------------------------------------------------------------------
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel)
        event.Skip()
 
    #----------------------------------------------------------------------
    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print 'OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel)
        event.Skip()
 
########################################################################
class DemoFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""        
        wx.Frame.__init__(self, None, wx.ID_ANY, 
                          "Listbook Tutorial",
                          size=(700,400)
                          )
        panel = wx.Panel(self)
 
        notebook = ListbookDemo(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()
 
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = DemoFrame()
    app.MainLoop()

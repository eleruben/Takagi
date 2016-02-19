import wx
import wx.grid
import wx.combo
class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        self.CreateGrid(10, 5)
        for i in range(10):
            self.SetRowLabelValue(i,str(i))

class ListCtrlComboPopup(wx.ListCtrl, wx.combo.ComboPopup):

    def __init__(self,parent):
        self.gfobj = parent
        self.PostCreate(wx.PreListCtrl())
        self.parent = parent
        wx.combo.ComboPopup.__init__(self)

    def AddItem(self, txt):
        self.InsertStringItem(self.GetItemCount(), txt)
        self.Select(0)

    def GetSelectedItems(self):
      del self.gfobj.selection[:]
      current = -1
      while True:
            next = self.GetNextSelected(current)
            if next == -1:
                return
            self.gfobj.selection.append(next)
            current = next

    def onItemSelected(self, event):
        item = event.GetItem()
        self.GetSelectedItems()
        self.parent.draw_plot()

    def onItemDeSelected(self, event):
        self.GetSelectedItems()
        self.parent.draw_plot()


    def Init(self):
        """ This is called immediately after construction finishes.  You can
        use self.GetCombo if needed to get to the ComboCtrl instance. """
        self.value = -1
        self.curitem = -1


    def Create(self, parent):
        """ Create the popup child control. Return True for success. """
        wx.ListCtrl.Create(self, parent,
                           style=wx.LC_LIST|wx.SIMPLE_BORDER)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeSelected)
        return True


    def GetControl(self):
        """ Return the widget that is to be used for the popup. """
        return self

    def SetStringValue(self, val):
        """ Called just prior to displaying the popup, you can use it to
        'select' the current item. """
        idx = self.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.Select(idx)


    def GetStringValue(self):
        """ Return a string representation of the current item. """
        a = self.GetItemText(self.value)
        if self.value >= 0:
            return a
        return ""

    def OnPopup(self):
        """ Called immediately after the popup is shown. """
        self.state = []
        for i in range(self.GetItemCount()):
            item = self.GetItem(itemId=i)
            self.state.append(item.GetState())
            #print self.state
        wx.combo.ComboPopup.OnPopup(self)

    def OnDismiss(self):
        " Called when popup is dismissed. """
        wx.combo.ComboPopup.OnDismiss(self)
#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.5

import wx

class MyFrame( wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
       
        self.button_1 = wx.Button(self.panel_1, 1001, "Aqui boton 1")
        self.button_2 = wx.Button( self.panel_1, -1, "Aqui boton 2")

        self.button_1.SetToolTipString ('This is button 1')
        self.button_2.SetToolTipString('This is button 2')

        #self.panel_1.Bind(wx.EVT_BUTTON, self.OnButton, self.button_1)
        self.button_2_state = 1

        self.__set_properties()
        self.__do_layout()
        # end wxGlade       
 
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame_1")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer (wx.VERTICAL)
        sizer_2.Add(self.button_1, 0, wx.ALL, 20)
        sizer_2.Add(self.button_2, 0, wx.ALL, 20)
        self.panel_1.SetSizer (sizer_2)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyFrame


class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
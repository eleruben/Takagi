#!/usr/bin/python
#-*- coding: latin-1 -*-
import wx
class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        # Esta vez vamos a utilizar un panel
        wx.Panel.__init__(self, parent)
        self.quote = wx.StaticText(self, label="Una label de texto estático", pos=(20, 30))
 
        # Creamos un TextControl para mostrar un log de todos los eventos que se ejecutan en el programa
        self.logger = wx.TextCtrl(self, pos=(300,20), size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)
 
        # Creamos un botón y le creamos un evento onClick
        self.button =wx.Button(self, label="Guardar", pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
 
        # Y una label con un control de texto editable al lado y dos eventos para capturar texto
        self.lblname = wx.StaticText(self, label="Tu nombre :", pos=(20,60))
        self.editname = wx.TextCtrl(self, value="", pos=(120, 60), size=(140,-1))
        #self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)
 
        # Lo mismo con un combobox y sus eventos
        self.sampleList = ['Aburrido', 'Mola', 'Lo mejor', 'Alucinante']
        self.lblhear = wx.StaticText(self, label="Qué te parece el programa :", pos=(20, 90))
        self.edithear = wx.ComboBox(self, pos=(200, 90), size=(60, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
        #self.Bind(wx.EVT_TEXT, self.EvtText,self.edithear)
 
        # Para un Checkbox
        self.insure = wx.CheckBox(self, label="¿Quieres doble de queso en la pizza?", pos=(20,180))
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)
 
        # Y un Radiobox
        radioList = ['azul', 'rojo', 'amarillo', 'naranja', 'verde', 'lila', 'negro', 'gris']
        rb = wx.RadioBox(self, label="¿Cuál es tu color favorito?", pos=(20, 210), choices=radioList,  majorDimension=3,
                         style=wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
 
    def EvtRadioBox(self, event):
        self.logger.AppendText('Evento de radio box: %dn' % event.GetInt())
    def EvtComboBox(self, event):
        self.logger.AppendText('Evento de combo box: %sn' % event.GetString())
    def OnClick(self,event):
        self.logger.AppendText("Clic en el objeto con Id %dn" % event.GetId())
    def EvtText(self, event):
        self.logger.AppendText('Evento de texto: %sn' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('Evento de carácter: %dn' % event.GetKeyCode())
        print(event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('Evento de check box: %dn' % event.Checked())
 
 
app = wx.App(False)
frame = wx.Frame(None, title="Controles y eventos", size=(540,420))
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()
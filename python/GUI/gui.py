import wx
import numpy as np

class bucky(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Hola Mundo', size=(300, 200))
        print "Hola2"

j = np.zeros((3,3))

print j

l=[[]]
l.append([])
l[0].append(1)
l[1].append(2)
print l

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = bucky(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
    print "Hola"

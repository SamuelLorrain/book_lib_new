import wx

class LaunchButton(wx.Button):
    def __init__(self,parent):
        super().__init__(parent, wx.ID_ANY, label="Launch Button")


import wx
import constant

class SearchComboBox(wx.ComboBox):
    def __init__(self,parent):
        choices = constant.CHOICESCOMBOSEARCH
        super().__init__(parent, wx.ID_ANY, style=wx.CB_READONLY,
                choices=choices)
        self.InitUI()

    def InitUI(self):
        self.SetSelection(len(constant.CHOICESCOMBOSEARCH)-1)


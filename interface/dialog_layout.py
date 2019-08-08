import wx.adv
from collections import OrderedDict


#class EntrySimpleTable(wx.):
#    def __init__(self, parent):
#        super().__init__(wx.HORIZONTAL)


class Apropos(wx.adv.AboutDialogInfo):
    def __init__(self):
        super(Apropos, self).__init__()

        self.description = "description sample"
        self.licence = "licence sample"

        self.SetName("Book Library")
        self.SetVersion('0.1a')
        self.SetDescription(self.description)
        self.SetCopyright('Meh 2019 - Samuel Lorrain')
        self.SetLicence(self.licence)
        self.AddDeveloper("Samuel Lorrain")


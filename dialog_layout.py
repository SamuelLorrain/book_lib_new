import wx
import wx.adv
import config
from collections import OrderedDict

class EntryBooks(wx.BoxSizer):
    def __init__(self,parent,label,entry):
        super().__init__(wx.HORIZONTAL)

        label = label.capitalize() + " : "

        self.label = wx.StaticText(parent, wx.ID_ANY, label)
        if type(entry) == int:
            self.entry = wx.SpinCtrl(parent, wx.ID_ANY, min=1, max=10,
                    initial=entry)
        elif type(entry) == str:
            self.entry = wx.TextCtrl(parent, wx.ID_ANY, value=entry)
        elif type(entry) == bool:
            self.entry = wx.CheckBox(parent, wx.ID_ANY)
        else:
            raise TypeError("unknown type. Unable to create the menu")

        self.Add(self.label)
        self.Add(self.entry)

    def addWidget(self,widget):
        self.Add(widget)

#class EntrySimpleTable(wx.):
#    def __init__(self, parent):
#        super().__init__(wx.HORIZONTAL)


class PreferenceDialog(wx.Dialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.InitUI()
        self.SetTitle("Préférences")

    def InitUI(self):
        self.SetMinSize((600,400))
        self.SetMaxSize((600,400))
        self.panel = wx.Panel(self)

        self.sauverButton = wx.Button(self.panel, wx.ID_ANY, label="Sauver")
        self.annulerButton = wx.Button(self.panel, wx.ID_ANY, label="Annuler")
        self.listChoices = wx.ListBox(self.panel, wx.ID_ANY,
                size=(150,400),
                choices=[i.capitalize() for i in config.configuration.keys()],
                style=wx.LB_SINGLE)
        self.listChoices.SetSelection(0)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.listChoices, 1, wx.EXPAND | wx.ALL,5)

        self.saveBox = wx.BoxSizer(wx.HORIZONTAL)
        self.saveBox.AddSpacer(200)
        self.saveBox.Add(self.sauverButton,1,wx.RIGHT, 5)
        self.saveBox.Add(self.annulerButton,1,wx.RIGHT,5)

        self.mainBox = wx.BoxSizer(wx.VERTICAL)

        self.mainContent = wx.Panel(self.panel, size=(300, 330))

        self.mainBox.Add(self.mainContent)
        self.mainBox.Add(self.saveBox)
        self.vBox = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.vBox, 3, wx.EXPAND | wx.ALL,5)
        self.sizer.Add(self.mainBox, 1, wx.EXPAND | wx.ALL,5)

        self.panel.SetSizer(self.sizer)

class AddBookDialog(wx.Dialog):
    def __init__(self,parent):
        super(AddBookDialog,self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        self.SetTitle("Add book dialog")
        self.SetMinSize((600,400))
        self.SetMaxSize((600,400))
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.bookEntries = []

        self.pathBookEntry = EntryBooks(self.panel,"Path To Book","")
        self.PathButton = wx.Button(self.panel, label="Path")
        self.pathBookEntry.addWidget(self.PathButton)
        self.bookEntries.append(self.pathBookEntry)


        self.infoBook = {
                "note" : 5,
                "name" : "",
                "date" : "",
                "lu" : False,
                "commence" : False,
                "physic" : False,
                "resume" : False,
                "complement" : False }

        for j,k in self.infoBook.items():
            self.bookEntries.append(EntryBooks(self.panel,j,k))

        for i in self.bookEntries:
            self.sizer.Add(i)

        self.panel.SetSizer(self.sizer)
#        #
#        #filetype_id
#        #
#        self.filetypeSizer = wx.BoxSizer(wx.HORIZONTAL)
#        self.filetypeSizer.Add()
#
#        #edition_id
#
#        #subject :
#
#        #genre :
#
#        #author :

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


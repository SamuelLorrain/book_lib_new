import wx
import config
from collections import OrderedDict

class PreferenceDialog(wx.Dialog):
    def __init__(self,parent):
        super().__init__(parent)

        self.currentConfig = OrderedDict()

        self.SetTitle("Preferences")

        self.keyConfigChoosen = ""

        self.SetMinSize((600,400))
        self.SetMaxSize((600,400))
        self.panel = wx.Panel(self)
        self.listChoices = wx.ListBox(self.panel, wx.ID_ANY,
                size=(150,400),
                choices=[i.capitalize() for i in config.configuration.keys()],
                style=wx.LB_SINGLE)
        self.listChoices.SetSelection(0)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.listChoices, 1, wx.EXPAND | wx.ALL,5)

        #Savebox
        self.saveBox = wx.BoxSizer(wx.HORIZONTAL)
        self.saveBox.AddSpacer(200)
        self.sauverButton = wx.Button(self.panel, wx.ID_ANY, label="Sauver")
        self.annulerButton = wx.Button(self.panel, wx.ID_CANCEL, label="Annuler")
        self.saveBox.Add(self.sauverButton,1,wx.RIGHT, 5)
        self.saveBox.Add(self.annulerButton,1,wx.RIGHT,5)

        #mainBox
        self.initPanelPeferences(None)

        self.panel.SetSizer(self.sizer)

        self.vBox = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.vBox, 3, wx.EXPAND | wx.ALL,5)
        self.sizer.Add(self.mainBox, 1, wx.EXPAND | wx.ALL,5)

        #binding
        self.Bind(wx.EVT_BUTTON, self.closePreferences,
                    id=self.annulerButton.GetId())
        self.Bind(wx.EVT_BUTTON, self.savePreferences,
                    id=self.sauverButton.GetId())
        self.Bind(wx.EVT_LISTBOX, self.changePanelPreferences,
                    id=self.listChoices.GetId())


    def closePreferences(self,e):
        self.Destroy()

    def savePreferences(self,e):
        print("save")

    def changePanelPreferences(self,e):
        # Hide old active panel

        self.keyConfigChoosen = self.listChoices.GetString(
                self.listChoices.GetSelection()).upper()

        for i in self.contentBox:
            if i != self.keyConfigChoosen:
                self.contentBox[i].ShowItems(False)
            if i == self.keyConfigChoosen:
                self.contentBox[i].ShowItems(True)

        self.mainBox.Layout()

    def initPanelPeferences(self,e):
        self.mainBox = wx.BoxSizer(wx.VERTICAL)
        self.configPanel = OrderedDict()
        self.contentBox = OrderedDict()
        for i in config.configuration.keys():
            self.contentBox[i] = wx.BoxSizer(wx.VERTICAL)
            for k,value in config.configuration[i].items(): #for sub-configuration items
                self.contentBox[i].Add(wx.StaticText(self.panel,label=str(k)))
                self.contentBox[i].Add(wx.TextCtrl(self.panel,value=str(value),
                    size=(350,30)))

        self.keyConfigChoosen = self.listChoices.GetString(
                self.listChoices.GetSelection()).upper()

        for i in self.contentBox:
            self.mainBox.Add(self.contentBox[i])

        for i in self.contentBox:
            if i != self.keyConfigChoosen:
                self.contentBox[i].ShowItems(False)
            if i == self.keyConfigChoosen:
                self.contentBox[i].ShowItems(True)

        self.mainBox.AddSpacer(10)
        self.mainBox.Add(self.saveBox)
        self.mainBox.Layout()

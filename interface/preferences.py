import wx
import config
from collections import OrderedDict

class PreferenceDialog(wx.Dialog):
    def __init__(self,parent):
        super().__init__(parent)

        self.currentConfig = OrderedDict()

        self.SetTitle("Préférences")

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

        #Sizebox
        self.saveBox = wx.BoxSizer(wx.HORIZONTAL)
        self.saveBox.AddSpacer(200)
        self.sauverButton = wx.Button(self.panel, wx.ID_ANY, label="Sauver")
        self.annulerButton = wx.Button(self.panel, wx.ID_CANCEL, label="Annuler")
        self.saveBox.Add(self.sauverButton,1,wx.RIGHT, 5)
        self.saveBox.Add(self.annulerButton,1,wx.RIGHT,5)

        #mainBox
        #self.mainBox = wx.BoxSizer(wx.VERTICAL)

        #self.mainContent = wx.Panel(self.panel, size=(300, 330))
        #self.contentBox = wx.BoxSizer(wx.VERTICAL)
        #self.mainContent.SetSizer(self.contentBox)

        #self.a = wx.StaticText(self.mainContent, label='rootPath')
        #self.b = wx.TextCtrl(self.mainContent,
        #        value=str(config.configuration['PATH']['rootPath']),size=(300,30))
        #self.contentBox.Add(self.a)
        #self.contentBox.Add(self.b)

        self.changePanelPreferences(None)

        #self.mainBox.Add(self.mainContent)
        #self.mainBox.Add(self.saveBox)

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
        #if no modifications
        self.Destroy()

    def savePreferences(self,e):
        print("save !")

    def changePanelPreferences(self,e):
        #clear all things
        #for i,_ in enumerate(self.contentBox):
        #    self.contentBox.Remove(i)
        #self.contentBox.Layout()

        self.mainBox = wx.BoxSizer(wx.VERTICAL)

        self.mainContent = wx.Panel(self.panel, size=(300, 330))
        self.contentBox = wx.BoxSizer(wx.VERTICAL)
        self.mainContent.SetSizer(self.contentBox)

        #Create config panels dynamically
        self.labelConfig = []
        self.fieldConfig = []

        for keyConfig in config.configuration.keys():
            for k,value in config.configuration[keyConfig].items(): #for sub-configuration items
                self.labelConfig.append(wx.StaticText(self.mainContent,label=str(k)))
                self.fieldConfig.append(wx.TextCtrl(self.mainContent,value=str(value),
                                        size=(300,30)))
                self.contentBox.Add(self.labelConfig[-1])
                self.contentBox.Add(self.fieldConfig[-1])
        self.contentBox.Layout()

        self.mainBox.Add(self.mainContent)
        self.mainBox.Add(self.saveBox)

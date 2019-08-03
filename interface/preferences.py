import wx
import config

class PreferenceDialog(wx.Dialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.SetTitle("Préférences")

        self.SetMinSize((600,400))
        self.SetMaxSize((600,400))
        self.panel = wx.Panel(self)
        self.sauverButton = wx.Button(self.panel, wx.ID_ANY, label="Sauver")
        self.annulerButton = wx.Button(self.panel, wx.ID_CANCEL, label="Annuler")
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

        self.labelTest = wx.Label(self.mainContent, "test")

        self.mainContent.Add(self.labelTest)



        self.mainBox.Add(self.mainContent)
        self.mainBox.Add(self.saveBox)
        self.vBox = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.vBox, 3, wx.EXPAND | wx.ALL,5)
        self.sizer.Add(self.mainBox, 1, wx.EXPAND | wx.ALL,5)

        self.panel.SetSizer(self.sizer)

        #binding
        self.Bind(wx.EVT_BUTTON, self.closePreferences,
                    id=self.annulerButton.GetId())

        self.Bind(wx.EVT_BUTTON, self.savePreferences,
                    id=self.sauverButton.GetId())
        self.Bind(wx.EVT_CLICK, self.changeConfigItem,
                    id=self.listChoices.GetId())

    def closePreferences(self,e):
        #if no  modifications
        self.Destroy()

    def savePreferences(self,e):
        print("save !")

    def changeConfigItem(self,e):
        print("save !")

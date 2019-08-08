import wx

class EntryBooks(wx.BoxSizer):
    def __init__(self,parent,label,entry,choices=[]):
        super().__init__(wx.HORIZONTAL)

        label = label.capitalize() + " : "

        self.label = wx.StaticText(parent, wx.ID_ANY, label,
                    size=(100,20))
        if entry == 'spin':
            self.entry = wx.SpinCtrl(parent, wx.ID_ANY, min=1, max=10,
                    initial=5)
        elif entry == 'text':
            self.entry = wx.TextCtrl(parent, wx.ID_ANY, value='',
                    size=(300,30))
        elif entry == 'bool':
            self.entry = wx.CheckBox(parent, wx.ID_ANY)
        elif entry == 'choice':
            self.entry = wx.Choice(parent, wx.ID_ANY, choices=choices);
        else:
            raise TypeError("unknown type. Unable to create the menu")

        self.AddSpacer(25)
        self.Add(self.label, 1,0,0)
        self.AddSpacer(10)
        self.Add(self.entry, 3,wx.EXPAND,0)

    def addWidget(self,widget):
        self.AddSpacer(10)
        self.Add(widget)


class AddBookDialog(wx.Dialog):
    def __init__(self,parent):
        super(AddBookDialog,self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        self.SetTitle("Add book dialog")
        self.SetMinSize((600,410))
        self.SetMaxSize((600,410))
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.bookEntries = []

        self.pathBookEntry = EntryBooks(self.panel,"Path To Book","text")
        self.PathButton = wx.Button(self.panel, label="Path")
        self.pathBookEntry.addWidget(self.PathButton)
        self.bookEntries.append(self.pathBookEntry)

        self.sizer.Add(self.pathBookEntry)


        self.infoBook =[
                    ("note" ,'spin',[]),
                    ("name" , "text",[]),
                    ("date" , "text",[]),
                    ("lu" , "bool",[]),
                    ("commence" , "bool",[]),
                    ("physic" , "bool",[]),
                    ("resume" , "bool",[]),
                    ("complement" ,"bool",[]),
                    ("genre",'choice',[]),
                    ("auteurs (séparés par des ',')" ,"text",[]),
                    ("sujets (séparés par des ',')" ,"text",[]),
                    ]

        for j,k,l in self.infoBook:
            self.bookEntries.append(EntryBooks(self.panel,j,k,l))

        for i in self.bookEntries:
            self.sizer.Add(i)

        #saveBox, DUPLICATES REFERENCES
        self.saveBox = wx.BoxSizer(wx.HORIZONTAL)
        self.saveBox.AddSpacer(400)
        self.sauverButton = wx.Button(self.panel, wx.ID_ANY, label="Sauver")
        self.annulerButton = wx.Button(self.panel, wx.ID_CANCEL, label="Annuler")
        self.saveBox.Add(self.sauverButton,1,wx.RIGHT, 5)
        self.saveBox.Add(self.annulerButton,1,wx.RIGHT,5)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.saveBox)

        self.panel.SetSizer(self.sizer)

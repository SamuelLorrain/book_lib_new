import wx
import wx.lib.mixins.listctrl
import constant

"""
Main layout, contains
classed herited by wx.Widgets classes.
"""

class BookLibraryToolBar(wx.ToolBar):
    def __init__(self,frame):
        super().__init__()
        self.frame = frame
        self.InitUI()

    def InitUI(self):
        self.toolbar = self.frame.CreateToolBar()
        self.toolbar.SetToolSeparation(10)

        self.undo = self.toolbar.AddTool(wx.ID_UNDO,
                'Undo',
                wx.Bitmap('/usr/share/icons/gnome/32x32/actions/gtk-undo-ltr.png'))
        self.redo = self.toolbar.AddTool(wx.ID_REDO,
                'Redo',
                wx.Bitmap('/usr/share/icons/gnome/32x32/actions/gtk-redo-ltr.png'))
        self.toolbar.AddSeparator()
        self.add = self.toolbar.AddTool(wx.ID_ANY,
                'Add Book',
                wx.Bitmap('/usr/share/icons/gnome/32x32/actions/gtk-add.png'))
        self.properties = self.toolbar.AddTool(wx.ID_ANY,
                'Change Book',
                wx.Bitmap('/usr/share/icons/gnome/32x32/actions/gtk-properties.png'))
        self.export = self.toolbar.AddTool(wx.ID_ANY,
                'Export Book',
                wx.Bitmap('/usr/share/icons/gnome/32x32/actions/gtk-save-as.png'))
        self.toolbar.Realize()

class BookLibraryMenuBar(wx.MenuBar):
    def __init__(self):
        super().__init__()

        self.FileMenuInit()
        self.EditMenuInit()
        self.ToolMenuInit()
        self.HelpMenuInit()

        self.Append(self.fileMenu, '&File')
        self.Append(self.editMenu, '&Edit')
        self.Append(self.toolMenu, '&Tool')
        self.Append(self.helpMenu, '&Help')

    def FileMenuInit(self):
        self.fileMenu = wx.Menu()

        self.exportItem = self.fileMenu.Append(wx.ID_ANY,
                '&Export...\tCtrl+E', 'Export books to a tablet or a phone etc.')
        self.fileMenu.InsertSeparator(1)
        self.preferenceItem = self.fileMenu.Append(wx.ID_ANY,
                '&Préférences...\tCtrl+P', 'Préférences')
        self.quitItem = self.fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit Application')

    def EditMenuInit(self):
        self.editMenu = wx.Menu()
        self.undoItem = self.editMenu.Append(wx.ID_UNDO, "Undo\tCtrl+u",
                "Action Précédente")
        self.redoItem = self.editMenu.Append(wx.ID_REDO, "Redo\tCtrl+r",
                "Action Suivante")

    def ToolMenuInit(self):
        self.toolMenu = wx.Menu()

        self.addMenu = wx.Menu()
        self.modMenu = wx.Menu()

        self.addBookItem = self.toolMenu.Append(wx.ID_ANY, "Add Book...\tCtrl+N",
                "Ajouter un livre")

        self.addSubjectItem = self.addMenu.Append(wx.ID_ANY, "Subject...",
                "Ajouter un sujet")
        self.addGenreItem = self.addMenu.Append(wx.ID_ANY, "Genre...",
                "Ajouter un genre")
        self.addAuthorItem = self.addMenu.Append(wx.ID_ANY, "Author...",
                "Ajouter un auteur")

        self.modBookItem = self.modMenu.Append(wx.ID_ANY, "Book...",
                "Ajouter un livre")
        self.modSubjectItem = self.modMenu.Append(wx.ID_ANY, "Subject...",
                "Ajouter un sujet")
        self.modGenreItem = self.modMenu.Append(wx.ID_ANY, "Genre...",
                "Ajouter un genre")
        self.modAuthorItem = self.modMenu.Append(wx.ID_ANY, "Author...",
                "Ajouter un auteur")

        self.toolMenu.Append(wx.ID_ANY, 'Add', self.addMenu)
        self.toolMenu.Append(wx.ID_ANY, 'Modifier', self.modMenu)

    def HelpMenuInit(self):
        self.helpMenu = wx.Menu()
        self.aproposItem = self.helpMenu.Append(wx.ID_ANY, 'À &propos...',
                'Get information about the application')

class PanelLeft(wx.Panel):
    class InfoBookTree(wx.TreeCtrl):
        def __init__(self,parent):
            super().__init__(parent, wx.ID_ANY)

    class LaunchButton(wx.Button):
        def __init__(self,parent,label):
            super().__init__(parent, wx.ID_ANY, label=label)

    class SearchComboBox(wx.ComboBox):
        def __init__(self,parent):
            choices = constant.CHOICESCOMBOSEARCH
            super().__init__(parent, wx.ID_ANY, style=wx.CB_READONLY,
                    choices=choices)
            self.InitUI()

        def InitUI(self):
            self.SetSelection(len(constant.CHOICESCOMBOSEARCH)-1)

    class SearchPanel(wx.Panel):
        def __init__(self,parent):
            super().__init__(parent,wx.ID_ANY)
            self.InitUI()

        def InitUI(self):
            self.vBox = wx.BoxSizer(wx.VERTICAL)
            self.entrySearch = wx.SearchCtrl(self,wx.ID_ANY,size=(300,35),
                    style=wx.TE_PROCESS_ENTER)
            self.entrySearch.SetMaxLength(300)
            self.searchComboBox = PanelLeft.SearchComboBox(self)
            self.resultSearch = wx.ListBox(self,wx.ID_ANY)

            self.vBox.Add(self.entrySearch, 0,wx.EXPAND,0)
            self.vBox.Add(self.searchComboBox, 0,wx.EXPAND,0)
            self.vBox.Add(self.resultSearch, 1,wx.EXPAND,0)

            self.SetSizer(self.vBox)

    def __init__(self,parent,style=wx.BORDER_THEME,size=(250,300)):
        super().__init__(parent,wx.ID_ANY,style=style,size=(250,300))
        self.InitUI()

    def InitUI(self):
        self.vBox = wx.BoxSizer(wx.VERTICAL)

        self.infoBookTree = self.InfoBookTree(self)
        self.launchButton = self.LaunchButton(self,"Launch Book")

        #panelLeft_tab
        #self.vBox_tab = wx.Notebook(self)
        #self.authorPanel = self.AuthorPanel(self.vBox_tab)
        self.searchPanel = self.SearchPanel(self)

        #self.vBox_tab.AddPage(self.authorPanel, "info author")
        #self.vBox_tab.AddPage(self.searchPanel, "search")

        self.vBox.Add(self.infoBookTree, 1,wx.EXPAND,0)
        self.vBox.Add(self.launchButton, 0,wx.EXPAND,0)
        self.vBox.Add(self.searchPanel, 1,wx.EXPAND,0)

        #end
        self.SetSizer(self.vBox)

class PanelRight(wx.Panel):
    class BookList(wx.ListCtrl,
            wx.lib.mixins.listctrl.ColumnSorterMixin):
        def __init__(self,parent):
            wx.ListCtrl.__init__(self,parent,wx.ID_ANY, style=wx.LC_REPORT)
            wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self, 1000)

            #TODO itemDataMap

        def GetListCtrl(self):
            return self

    def __init__(self,parent,style=wx.BORDER_THEME,**kwargs):
        super().__init__(parent,wx.ID_ANY,
                style=wx.HSCROLL | wx.VSCROLL | wx.BORDER_RAISED
                , size=(600,300))
        self.InitUI()

    def InitUI(self):
        #list
        self.list = self.BookList(self)
        self.list.InsertColumn(0, 'name', width=200)
        self.list.InsertColumn(1, 'note', width=80)
        self.list.InsertColumn(2, 'date', width=80)
        self.list.InsertColumn(3, 'lu', width=80)
        self.list.InsertColumn(4, 'commence', width=80)
        self.list.InsertColumn(5, 'physic', width=80)
        self.list.InsertColumn(6, 'resume', width=80)
        self.list.InsertColumn(7, 'filetype', width=80)
        self.list.InsertColumn(8, 'edition', width=80)
        self.list.InsertColumn(8, 'complement', width=80)
        self.list.InsertColumn(9, 'subject', width=80)
        self.list.InsertColumn(10, 'genre', width=80)
        self.list.InsertColumn(11, 'author', width=80)

        #sizer
        self.hBox = wx.BoxSizer(wx.HORIZONTAL)
        self.hBox.Add(self.list,1,wx.EXPAND | wx.LEFT | wx.RIGHT , 5)
        self.SetSizer(self.hBox)

class MainFrame(wx.Frame):
    def __init__(self,parent,title):
        super().__init__(parent,title=title, size=(1200,700))

        self.InitUI()
        self.Centre()
        self.InitMenubar()
        self.InitStatusBar()
        self.InitToolBar()

    def InitUI(self):
        self.splitter = wx.SplitterWindow(self,
                style=wx.SP_LIVE_UPDATE|wx.SP_3D)
        #panelLeft
        self.panelLeft = PanelLeft(self.splitter)

        #panelRight
        self.panelRight = PanelRight(self.splitter)

        #splitter
        self.splitter.SplitVertically(self.panelLeft,self.panelRight,100)
        self.splitter.SetMinimumPaneSize(300)
        self.SetMinSize((500,200))

    def InitMenubar(self):
        self.menuBar = BookLibraryMenuBar()
        self.SetMenuBar(self.menuBar)

    def InitStatusBar(self):
        self.statusBar = self.CreateStatusBar(1)

    def InitToolBar(self):
        self.toolBar = BookLibraryToolBar(self)


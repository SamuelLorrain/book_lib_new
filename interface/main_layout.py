import wx
import wx.lib.mixins.listctrl
import constant

import interface.menubar
import interface.toolbar
import interface.booklist
import interface.infobooktree
import interface.launchbutton
import interface.searchcombobox

"""
Main layout, collect all
interfaces classes into a
complete layout.
Contains:
    - PanelLeft
    - PanelRight
    - MainFrame
"""

class PanelLeft(wx.Panel):
    class SearchPanel(wx.Panel):
        def __init__(self,parent):
            super().__init__(parent,wx.ID_ANY)
            self.InitUI()

        def InitUI(self):
            self.vBox = wx.BoxSizer(wx.VERTICAL)
            self.entrySearch = wx.SearchCtrl(self,wx.ID_ANY,size=(300,35),
                    style=wx.TE_PROCESS_ENTER)
            self.entrySearch.SetMaxLength(300)
            self.searchComboBox = interface.searchcombobox.SearchComboBox(self)
            self.resultSearch = wx.ListBox(self,wx.ID_ANY)

            self.vBox.Add(self.entrySearch, 0,wx.EXPAND,0)
            self.vBox.Add(self.searchComboBox, 0,wx.EXPAND,0)
            self.vBox.Add(self.resultSearch, 1,wx.EXPAND,0)

            self.SetSizer(self.vBox)

    def __init__(self,parent,booklist,style=wx.BORDER_THEME, size=(250,300)):
        super().__init__(parent,wx.ID_ANY,style=style,size=(250,300))
        self.InitUI(booklist)

    def InitUI(self, booklist):
        self.vBox = wx.BoxSizer(wx.VERTICAL)

        self.infoBookTree = interface.infobooktree.InfoBookTree(self)
        self.launchButton = interface.launchbutton.LaunchButton(self,
                "Launch Book", booklist)

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
    def __init__(self,parent,style=wx.BORDER_THEME,**kwargs):
        super().__init__(parent,wx.ID_ANY,
                style=wx.HSCROLL | wx.VSCROLL | wx.BORDER_RAISED
                , size=(600,300))
        self.InitUI()

    def InitUI(self):
        #list
        self.bookList = interface.booklist.BookList(self)

        #sizer
        self.hBox = wx.BoxSizer(wx.HORIZONTAL)
        self.hBox.Add(self.bookList,1,wx.EXPAND | wx.LEFT | wx.RIGHT , 5)
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
        self.panelRight = PanelRight(self.splitter)
        self.panelLeft = PanelLeft(self.splitter, self.panelRight.bookList)

        #splitter
        self.splitter.SplitVertically(self.panelLeft,self.panelRight,100)
        self.splitter.SetMinimumPaneSize(300)
        self.SetMinSize((500,200))

    def InitMenubar(self):
        self.menuBar = interface.menubar.BookLibraryMenuBar()
        self.SetMenuBar(self.menuBar)

    def InitStatusBar(self):
        self.statusBar = self.CreateStatusBar(1)

    def InitToolBar(self):
        self.toolBar = interface.toolbar.BookLibraryToolBar(self)


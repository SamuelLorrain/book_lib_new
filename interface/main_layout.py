import wx
import wx.lib.mixins.listctrl
import constant

import interface.menubar
import interface.toolbar
import interface.booklist

"""
Main layout, contains
classed herited by wx.Widgets classes.
Contains:
    - PanelLeft
        - InfoBookTree
        - LaunchButton
        - SearchComboBox
        - SearchPanel
    - PanelRight
        - BookList
And a global interface class: MainFrame

MainFrame contains objects from all classes except those
who are defined inside "PanelLeft" and "PanelRight".

Basically, all classes create objects from the wxWidget library,
and group them together to create the interface.
"""

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
    def __init__(self,parent,style=wx.BORDER_THEME,**kwargs):
        super().__init__(parent,wx.ID_ANY,
                style=wx.HSCROLL | wx.VSCROLL | wx.BORDER_RAISED
                , size=(600,300))
        self.InitUI()

    def InitUI(self):
        #list
        self.list = interface.booklist.BookList(self)

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
        self.menuBar = interface.menubar.BookLibraryMenuBar()
        self.SetMenuBar(self.menuBar)

    def InitStatusBar(self):
        self.statusBar = self.CreateStatusBar(1)

    def InitToolBar(self):
        self.toolBar = interface.toolbar.BookLibraryToolBar(self)


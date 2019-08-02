import wx
import wx.lib.mixins.listctrl
import constant

import interface.menubar
import interface.toolbar
import interface.booklist
import interface.infobooktree
import interface.launchbutton
import interface.searchpanel

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
    def __init__(self,parent,booklist,style=wx.BORDER_THEME, size=(250,300)):
        super().__init__(parent,wx.ID_ANY,style=style,size=(250,300))
        self.InitUI(booklist)

    def InitUI(self, booklist):
        self.vBox = wx.BoxSizer(wx.VERTICAL)

        self.infoBookTree = interface.infobooktree.InfoBookTree(self)
        self.launchButton = interface.launchbutton.LaunchButton(self)
        #panelLeft_tab
        self.searchPanel = interface.searchpanel.SearchPanel(self)
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

        #menubar
        self.menuBar = interface.menubar.BookLibraryMenuBar()
        self.SetMenuBar(self.menuBar)

        #statusbar
        self.statusBar = self.CreateStatusBar(1) #not in another object!

        #toolbar
        self.toolBar = interface.toolbar.BookLibraryToolBar(self)


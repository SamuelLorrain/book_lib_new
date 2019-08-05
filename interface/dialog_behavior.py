import wx
import wx.adv
from interface.dialog_layout import *
import interface.preferences
import interface.addbook_dialog

class DialogBehavior:
    def __init__(self, mainFrameObject):
        self.mainFrame = mainFrameObject

        #collecting menubar items
        self.menubar = self.mainFrame.menuBar
        self.fileMenu = self.mainFrame.menuBar.fileMenu
        self.editMenu = self.mainFrame.menuBar.editMenu
        self.toolMenu = self.mainFrame.menuBar.toolMenu
        self.helpMenu = self.mainFrame.menuBar.helpMenu

        self.exportItem = self.mainFrame.menuBar.exportItem
        self.preferenceItem = self.mainFrame.menuBar.preferenceItem
        self.quitItem = self.mainFrame.menuBar.quitItem

        self.undoItem = self.mainFrame.menuBar.undoItem
        self.redoItem = self.mainFrame.menuBar.redoItem

        self.addBookItem = self.mainFrame.menuBar.addBookItem
        self.addSubjectItem = self.mainFrame.menuBar.addSubjectItem
        self.addGenreItem = self.mainFrame.menuBar.addGenreItem
        self.addAuthorItem = self.mainFrame.menuBar.addAuthorItem

        self.modBookItem = self.mainFrame.menuBar.modBookItem
        self.modSubjectItem = self.mainFrame.menuBar.modSubjectItem
        self.modGenreItem = self.mainFrame.menuBar.modGenreItem
        self.modAuthorItem = self.mainFrame.menuBar.modAuthorItem

        self.aproposItem = self.mainFrame.menuBar.aproposItem

        #collecting toolbar items
        self.toolbar = self.mainFrame.toolBar
        self.undoButton = self.mainFrame.toolBar.undo
        self.redoButton = self.mainFrame.toolBar.redo
        self.addButton = self.mainFrame.toolBar.add
        self.propertiesButton = self.mainFrame.toolBar.properties

        #binding menu events
        self.mainFrame.Bind(wx.EVT_MENU, self.showPreference,
                id=self.preferenceItem.GetId())
        self.mainFrame.Bind(wx.EVT_MENU, self.showExport,
                id=self.exportItem.GetId())
        self.mainFrame.Bind(wx.EVT_MENU, self.pressQuit,
                id=self.quitItem.GetId())

        self.mainFrame.Bind(wx.EVT_MENU, self.pressUndo,
                id=self.undoItem.GetId())
        self.mainFrame.Bind(wx.EVT_MENU, self.pressRedo,
                id=self.redoItem.GetId())

        self.mainFrame.Bind(wx.EVT_MENU, self.showAddBook,
                id=self.addBookItem.GetId())
        self.mainFrame.Bind(wx.EVT_MENU, self.showAddSubject,
                id=self.addSubjectItem.GetId())
        self.mainFrame.Bind(wx.EVT_MENU, self.showAddGenre,
                id=self.addGenreItem.GetId())
        self.mainFrame.Bind(wx.EVT_MENU, self.showAddAuthor,
                id=self.addAuthorItem.GetId())

        self.mainFrame.Bind(wx.EVT_MENU, self.showModBook,
                id=self.modBookItem.GetId())
        self.mainFrame.Bind(wx.EVT_MENU, self.showModSubject,
                id=self.modSubjectItem.GetId())
        self.mainFrame.Bind(wx.EVT_MENU, self.showModGenre,
                id=self.modGenreItem.GetId())
        self.mainFrame.Bind(wx.EVT_MENU, self.showModAuthor,
                id=self.modAuthorItem.GetId())

        self.mainFrame.Bind(wx.EVT_MENU, self.showApropos,
                id=self.aproposItem.GetId())

        #bind toolbar
        self.mainFrame.Bind(wx.EVT_TOOL, self.pressUndo,
                id=self.undoButton.GetId())
        self.mainFrame.Bind(wx.EVT_TOOL, self.pressRedo,
                id=self.redoButton.GetId())
        self.mainFrame.Bind(wx.EVT_TOOL, self.showAddBook,
                id=self.addButton.GetId())
        #self.mainFrame.Bind(wx.TOOL, self.showAddBook, ??
        #        id=self.propertiesButton.GetId())

    #===============================
    #
    #===============================

    def showPreference(self,e):
        self.dialog = interface.preferences.PreferenceDialog(self.mainFrame)
        #self.content = self.dialog.mainContent

        self.dialog.ShowModal()

    def showExport(self,e):
        pass

    def pressQuit(self,e):
        print("Goodbye!")
        self.mainFrame.Close()

    #===============================
    #
    #===============================

    def pressUndo(self,e):
        pass
    def pressRedo(self,e):
        pass

    #===============================
    #
    #===============================

    def showAddBook(self,e):
        self.dialog = interface.addbook_dialog.AddBookDialog(self.mainFrame)
        self.dialog.ShowModal()

    def showAddSubject(self,e):
        pass
    def showAddGenre(self,e):
        pass
    def showAddAuthor(self,e):
        pass

    #===============================
    #
    #===============================

    def showModBook(self,e):
        pass
    def showModSubject(self,e):
        pass
    def showModGenre(self,e):
        pass
    def showModAuthor(self,e):
        pass


    def showApropos(self,e):
        wx.adv.AboutBox(Apropos())


import wx
import wx.adv
from layout.dialog_layout import *

class DialogBehavior:
    def __init__(self, mainFrameObject):
        self.mainFrame = mainFrameObject

    #===============================
    #
    #===============================

    def showPreference(self,e):
        self.dialog = PreferenceDialog(self.mainFrame)
        self.content = self.dialog.mainContent

        self.dialog.Bind(wx.EVT_BUTTON, self.pressAnnulerPreference,
                id=self.dialog.annulerButton.GetId())

        self.dialog.Bind(wx.EVT_BUTTON, self.pressSavePreference,
                id=self.dialog.sauverButton.GetId())

        self.dialog.ShowModal()

    def showExport(self,e):
        pass

    def pressQuit(self,e):
        print("Goodbye!")
        self.mainFrame.Close()

    def pressAnnulerPreference(self,e):
        print("test")

    def pressSavePreference(self,e):
        print("toast")

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
        self.dialog = AddBookDialog(self.mainFrame)
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


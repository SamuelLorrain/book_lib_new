from main_layout import *
from dialog_behavior import *
from dialog_layout import *
import wx
import select_items
import factory_table
from acces_files import *
import constant
import config
import bdd_misc_queries

"""
Main behavior, collect all logic in a master object
"""

class Behavior:
    def __init__(self, mainFrameObject):
        if type(mainFrameObject) is not MainFrame:
         TypeError("the input object is not MainFrame")

        """
        Collect all widgets
        """
        self.main = mainFrameObject
        self.dialogbehavior = DialogBehavior(self.main)

        self.panelL = self.main.panelLeft
        self.panelR = self.main.panelRight
        self.booklist = self.main.panelRight.list
        self.statusbar = self.main.statusBar
        self.launchButton = self.main.panelLeft.launchButton
        self.infoBookTree = self.main.panelLeft.infoBookTree

        self.menubar = self.main.menuBar
        self.statusbar = self.main.statusBar
        self.fileMenu = self.main.menuBar.fileMenu
        self.editMenu = self.main.menuBar.editMenu
        self.toolMenu = self.main.menuBar.toolMenu
        self.helpMenu = self.main.menuBar.helpMenu

        self.exportItem = self.main.menuBar.exportItem
        self.preferenceItem = self.main.menuBar.preferenceItem
        self.quitItem = self.main.menuBar.quitItem

        self.undoItem = self.main.menuBar.undoItem
        self.redoItem = self.main.menuBar.redoItem

        self.addBookItem = self.main.menuBar.addBookItem
        self.addSubjectItem = self.main.menuBar.addSubjectItem
        self.addGenreItem = self.main.menuBar.addGenreItem
        self.addAuthorItem = self.main.menuBar.addAuthorItem

        self.modBookItem = self.main.menuBar.modBookItem
        self.modSubjectItem = self.main.menuBar.modSubjectItem
        self.modGenreItem = self.main.menuBar.modGenreItem
        self.modAuthorItem = self.main.menuBar.modAuthorItem

        self.aproposItem = self.main.menuBar.aproposItem

        self.searchComboBox = self.main.panelLeft.searchPanel.searchComboBox
        self.searchEntry = self.main.panelLeft.searchPanel.entrySearch
        self.searchResult = self.main.panelLeft.searchPanel.resultSearch

        self.toolbar = self.main.toolBar
        self.undoButton = self.main.toolBar.undo
        self.redoButton = self.main.toolBar.redo
        self.addButton = self.main.toolBar.add
        self.propertiesButton = self.main.toolBar.properties


        self.query = []
        self.searchQuery = []
        self.history = []

        self.statusbar.SetStatusText("{} book(s) in the"
                " database".format(bdd_misc_queries.numberOfBooks()))


        self.initList()
        self.initEvent()

    def setQuery(self,newQuery):
        if len(self.history) >= config.configuration['HISTORY']['historyLength']:
            self.history.pop(0)
        self.history.append(self.query)
        self.query = newQuery

    def initEvent(self):
        #launchButton
        self.main.Bind(wx.EVT_BUTTON, self.launchBook,
                id=self.launchButton.GetId())
        #bookList
        self.main.Bind(wx.EVT_LIST_ITEM_SELECTED, self.showInfoBook,
                id=self.booklist.GetId())
        self.main.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.launchBook,
                id=self.booklist.GetId())
        self.main.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.launchBook,
                id=self.booklist.GetId())

        #searchText
        self.main.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN,self.searchItems,
                id=self.searchEntry.GetId())
        self.main.Bind(wx.EVT_TEXT_ENTER,self.searchItems,
                id=self.searchEntry.GetId())

        #searchComboBox
        self.main.Bind(wx.EVT_COMBOBOX, self.searchItems,
                id=self.searchComboBox.GetId())

        #searchResult
        self.main.Bind(wx.EVT_LISTBOX_DCLICK, self.setItemsSearched,
                id=self.searchResult.GetId())

        #menu
        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showPreference,
                id=self.preferenceItem.GetId())
        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showExport,
                id=self.exportItem.GetId())
        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.pressQuit,
                id=self.quitItem.GetId())

        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.pressUndo,
                id=self.undoItem.GetId())
        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.pressRedo,
                id=self.redoItem.GetId())

        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showAddBook,
                id=self.addBookItem.GetId())
        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showAddSubject,
                id=self.addSubjectItem.GetId())
        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showAddGenre,
                id=self.addGenreItem.GetId())
        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showAddAuthor,
                id=self.addAuthorItem.GetId())

        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showModBook,
                id=self.modBookItem.GetId())
        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showModSubject,
                id=self.modSubjectItem.GetId())
        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showModGenre,
                id=self.modGenreItem.GetId())
        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showModAuthor,
                id=self.modAuthorItem.GetId())

        self.main.Bind(wx.EVT_MENU, self.dialogbehavior.showApropos,
                id=self.aproposItem.GetId())

    def setItemsSearched(self,e):
        txtQuery = self.searchEntry.GetLineText(0)
        tmpQuery = factory_table.factory_table(
                self.searchComboBox.GetStringSelection(),e.GetString())
        self.setQuery(select_items.SelectItems.by(tmpQuery))
        self.fillList()

    def searchItems(self,e):
        txtQuery = self.searchEntry.GetLineText(0)
        if self.searchComboBox.GetStringSelection() == '':
            self.searchQuery = select_items.SelectItems.all(
                    self.searchComboBox.GetStringSelection())
        else:
            self.searchQuery = select_items.SelectItems.like(
                    self.searchComboBox.GetStringSelection(),
                    txtQuery,mode='before|after')

        if self.searchComboBox.GetStringSelection() == 'book':
            self.setQuery(self.searchQuery)
            self.fillList()

        if len(self.searchQuery) > 100:
            self.searchQuery = self.searchQuery[:100]

        self.fillSearchList()

    def launchBook(self,e):
        if self.booklist.GetFirstSelected() is not -1:
            print("launch book number %d" % self.booklist.GetFirstSelected())
            AccessFile.book(self.query[self.booklist.GetFirstSelected()])

    def showInfoBook(self,e):
        if self.booklist.GetFirstSelected() is not -1:
            self.main.Unbind(wx.EVT_TREE_ITEM_ACTIVATED, self.infoBookTree)
            self.infoBookTree.DeleteAllItems()
            self.infoBookTree_name = self.infoBookTree.AddRoot(
                    self.query[self.booklist.GetFirstSelected()].name)
            self.infoBookTree_infos = self.infoBookTree.AppendItem(
                    self.infoBookTree_name, "Infos")
            self.infoBookTree_note = self.infoBookTree.AppendItem(
                    self.infoBookTree_infos,
                    "note : "+
                    str(self.query[self.booklist.GetFirstSelected()].note))
            self.infoBookTree_date = self.infoBookTree.AppendItem(
                    self.infoBookTree_infos,
                    "date : "+
                    str(self.query[self.booklist.GetFirstSelected()].date))
            self.infoBookTree_lu = self.infoBookTree.AppendItem(
                    self.infoBookTree_infos,
                    "lu : "+
                    str(self.query[self.booklist.GetFirstSelected()].lu))
            self.infoBookTree_commence = self.infoBookTree.AppendItem(
                    self.infoBookTree_infos,
                    "commence : "+
                    str(self.query[self.booklist.GetFirstSelected()].commence))
            self.infoBookTree_physic = self.infoBookTree.AppendItem(
                    self.infoBookTree_infos,
                    "physic : "+
                    str(self.query[self.booklist.GetFirstSelected()].physic))
            self.infoBookTree_resume = self.infoBookTree.AppendItem(
                    self.infoBookTree_infos,
                    "resume : "+
                    str(self.query[self.booklist.GetFirstSelected()].resume))
            self.infoBookTree_filetype = self.infoBookTree.AppendItem(
                    self.infoBookTree_infos,
                    "filetype : "+
                    str(self.query[self.booklist.GetFirstSelected()].getFiletype()))
            self.infoBookTree_complement = self.infoBookTree.AppendItem(
                    self.infoBookTree_infos,
                    "complement : "+
                    str(self.query[self.booklist.GetFirstSelected()].complement))

            self.infoBookTree_subject = self.infoBookTree.AppendItem(
                    self.infoBookTree_name, "Subject")
            self.infoBookTree_subjectlist = []
            for j,i in enumerate(
                    self.query[self.booklist.GetFirstSelected()].getSubject()):
                self.infoBookTree_subjectlist.append(self.infoBookTree.AppendItem(
                        self.infoBookTree_subject, str(i), data=i))

            self.infoBookTree_author = self.infoBookTree.AppendItem(
                    self.infoBookTree_name, "Author")
            self.infoBookTree_authorlist = []
            for j,i in enumerate(
                    self.query[self.booklist.GetFirstSelected()].getAuthor()):
                self.infoBookTree_authorlist.append(self.infoBookTree.AppendItem(
                        self.infoBookTree_author, str(i), data=i))

            self.infoBookTree_genre = self.infoBookTree.AppendItem(
                    self.infoBookTree_name, "Genre")
            self.infoBookTree_genrelist = []
            for j,i in enumerate(
                    self.query[self.booklist.GetFirstSelected()].getGenre()):
                self.infoBookTree_genrelist.append(self.infoBookTree.AppendItem(
                        self.infoBookTree_genre, str(i), data=i))

            self.infoBookTree.Expand(self.infoBookTree_name)
            self.infoBookTree.ExpandAllChildren(self.infoBookTree_subject)
            self.infoBookTree.ExpandAllChildren(self.infoBookTree_author)
            self.infoBookTree.ExpandAllChildren(self.infoBookTree_genre)

            self.main.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.infoBookTreeActivated,
                    id=self.infoBookTree.GetId())

    def infoBookTreeActivated(self,e):
        if self.infoBookTree.GetSelection() == self.infoBookTree_name:
            self.launchBook(e)
        elif self.infoBookTree.GetSelection() in self.infoBookTree_subjectlist:
            for j,i in enumerate(self.infoBookTree_subjectlist):
                if self.infoBookTree.GetSelection() == i:
                    tmpBook = self.query[self.booklist.GetFirstSelected()]
                    tmpSubject = tmpBook.getSubject()
                    self.setQuery(select_items.SelectItems.by(
                                self.infoBookTree.GetItemData(i)))
                    self.fillList()
        elif self.infoBookTree.GetSelection() in self.infoBookTree_authorlist:
            for j,i in enumerate(self.infoBookTree_authorlist):
                if self.infoBookTree.GetSelection() == i:
                    tmpBook = self.query[self.booklist.GetFirstSelected()]
                    tmpAuthor = tmpBook.getAuthor()
                    self.setQuery(select_items.SelectItems.by(
                            self.infoBookTree.GetItemData(i)))
                    self.fillList()
        elif self.infoBookTree.GetSelection() in self.infoBookTree_genrelist:
            for j,i in enumerate(self.infoBookTree_genrelist):
                if self.infoBookTree.GetSelection() == i:
                    tmpBook = self.query[self.booklist.GetFirstSelected()]
                    tmpGenre = tmpBook.getGenre()
                    self.setQuery(select_items.SelectItems.by(
                            self.infoBookTree.GetItemData(i)))
                    self.fillList()

    def initList(self):
        self.setQuery(select_items.SelectItems.like('book','A'))
        self.fillList()

    def fillSearchList(self):
        self.searchResult.Clear()
        for i in self.searchQuery:
            self.searchResult.Append(i.name)

    def fillList(self):
        self.booklist.DeleteAllItems()
        for j,i in enumerate(self.query):
            index = self.booklist.InsertItem(j, i.name)
            self.booklist.SetItem(index,  1, str(i.note))
            self.booklist.SetItem(index,  2, str(i.date))
            self.booklist.SetItem(index,  3, str(i.lu))
            self.booklist.SetItem(index,  4, str(i.commence))
            self.booklist.SetItem(index,  5, str(i.physic))
            self.booklist.SetItem(index,  6, str(i.resume))
            self.booklist.SetItem(index,  7, str(i.getFiletype()))
            self.booklist.SetItem(index,  8, str(i.complement))

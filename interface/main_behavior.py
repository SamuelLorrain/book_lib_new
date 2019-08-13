from interface.main_layout import *
from interface.dialog_behavior import *
from interface.dialog_layout import *
from interface.search_behavior import *
import wx
from database import select_items
from tables import factory_table
from acces_files import *
import query
import history
import constant
import config
from database import bdd_misc_queries

"""
Main behavior, Proxy/Facade
collect all logic in a master object

Contains also 3 methods that use multiple
graphic components:
    - LaunchBook
    - infoBookTreeActivated
    - showInfoBook
"""

class Behavior:
    def __init__(self, mainFrameObject):
        if type(mainFrameObject) is not MainFrame:
         TypeError("the input object is not MainFrame")

        self.query = query.Query()
        """
        Collect all widgets
        """
        self.main = mainFrameObject
        self.dialogbehavior = DialogBehavior(self.main)
        self.searchPanelBehavior = SearchPanelBehavior(
                            self.main.panelLeft.searchPanel,
                            self.main.panelRight.bookList,
                            self.query)

        self.panelL = self.main.panelLeft
        self.panelR = self.main.panelRight
        self.booklist = self.main.panelRight.bookList
        self.statusbar = self.main.statusBar
        self.launchButton = self.main.panelLeft.launchButton
        self.infoBookTree = self.main.panelLeft.infoBookTree


        self.searchComboBox = self.main.panelLeft.searchPanel.searchComboBox
        self.searchEntry = self.main.panelLeft.searchPanel.entrySearch
        self.searchResult = self.main.panelLeft.searchPanel.resultSearch

        self.history = history.History()

        self.statusbar = self.main.statusBar
        self.statusbar.SetStatusText("{} book(s) in the"
                " database".format(bdd_misc_queries.numberOfBooks()))

        #init list items
        self.query.setQuery(select_items.SelectItems.like('book','A'))
        self.booklist.fillList(self.query)

        self.initEvent()

    def initEvent(self):
        #launchbook
        self.main.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.launchBook,
                id=self.booklist.GetId())
        self.main.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.launchBook,
                id=self.booklist.GetId())

        #showInfoBook
        self.main.Bind(wx.EVT_LIST_ITEM_SELECTED, self.showInfoBook,
                id=self.booklist.GetId())

        #searchText
        self.main.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN,self.searchPanelBehavior.searchItems,
                id=self.searchEntry.GetId())
        self.main.Bind(wx.EVT_TEXT_ENTER,self.searchPanelBehavior.searchItems,
                id=self.searchEntry.GetId())

        #searchComboBox
        self.main.Bind(wx.EVT_COMBOBOX, self.searchPanelBehavior.searchItems,
                id=self.searchComboBox.GetId())
        self.main.Bind(wx.EVT_BUTTON, self.launchBook,id=self.launchButton.GetId())

        #searchResult
        self.main.Bind(wx.EVT_LISTBOX_DCLICK,
                self.searchPanelBehavior.setItemsSearched,
                id=self.searchResult.GetId())

    """
    Launch a book based on the selected object of booklist
    """
    def launchBook(self,e):
        if self.booklist.GetFirstSelected() is not -1:
            print("launch book number %d" % self.booklist.GetFirstSelected())
            AccessFile.book(self.query[self.booklist.GetFirstSelected()])

    """
    Modify the infoBookTree when we click on an item on the bookList
    """
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

    """
    Modify bookList when there is a click on an item of the infoBookTree
    """
    def infoBookTreeActivated(self,e):
        if self.infoBookTree.GetSelection() == self.infoBookTree_name:
            self.launchBook(e)
        elif self.infoBookTree.GetSelection() in self.infoBookTree_subjectlist:
            for j,i in enumerate(self.infoBookTree_subjectlist):
                if self.infoBookTree.GetSelection() == i:
                    tmpBook = self.query[self.booklist.GetFirstSelected()]
                    tmpSubject = tmpBook.getSubject()
                    self.query.setQuery(select_items.SelectItems.by(
                                self.infoBookTree.GetItemData(i)))
                    self.booklist.fillList(self.query)
        elif self.infoBookTree.GetSelection() in self.infoBookTree_authorlist:
            for j,i in enumerate(self.infoBookTree_authorlist):
                if self.infoBookTree.GetSelection() == i:
                    tmpBook = self.query[self.booklist.GetFirstSelected()]
                    tmpAuthor = tmpBook.getAuthor()
                    self.query.setQuery(select_items.SelectItems.by(
                            self.infoBookTree.GetItemData(i)))
                    self.booklist.fillList(self.query)
        elif self.infoBookTree.GetSelection() in self.infoBookTree_genrelist:
            for j,i in enumerate(self.infoBookTree_genrelist):
                if self.infoBookTree.GetSelection() == i:
                    tmpBook = self.query[self.booklist.GetFirstSelected()]
                    tmpGenre = tmpBook.getGenre()
                    self.query.setQuery(select_items.SelectItems.by(
                            self.infoBookTree.GetItemData(i)))
                    self.booklist.fillList(self.query)

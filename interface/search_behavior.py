import wx
from tables import factory_table
from database import select_items

import interface.searchpanel
import interface.booklist
import query

class SearchPanelBehavior:
    def __init__(self, searchPanel, bookList, query):
        self.searchPanel = searchPanel
        self.bookList = bookList
        self.query = query

    def setItemsSearched(self,e):
        txtQuery = self.searchPanel.entrySearch.GetValue()
        tmpQuery = factory_table.factory_table(
                self.searchPanel.searchComboBox.GetStringSelection(),e.GetString())
        self.query.setQuery(select_items.SelectItems.by(tmpQuery))
        self.bookList.fillList(self.query)

    def searchItems(self,e):
        txtQuery = self.searchPanel.entrySearch.GetValue()
        searchQuery = ""
        if self.searchPanel.searchComboBox.GetStringSelection() == '':
            searchQuery = select_items.SelectItems.all(
                    self.searchPanel.searchComboBox.GetStringSelection())
        else:
            searchQuery = select_items.SelectItems.like(
                    self.searchPanel.searchComboBox.GetStringSelection(),
                    txtQuery,mode='before|after')

        if self.searchPanel.searchComboBox.GetStringSelection() == 'book':
            self.query.setQuery(searchQuery)
            self.bookList.fillList(self.query)

        if len(searchQuery) > 100:
            searchQuery = searchQuery[:100]

        self.searchPanel.fillSearchList(searchQuery)


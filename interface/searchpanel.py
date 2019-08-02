import wx
import interface.searchcombobox

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

    def fillSearchList(self, searchQuery):
        self.resultSearch.Clear()
        for i in searchQuery:
            self.resultSearch.Append(i.name)


import wx
from query import Query

class BookList(wx.ListCtrl,
        wx.lib.mixins.listctrl.ColumnSorterMixin):
    def __init__(self,parent):
        wx.ListCtrl.__init__(self,parent,wx.ID_ANY, style=wx.LC_REPORT)
        wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self, 1000)
        self.InsertColumn(0, 'name', width=200)
        self.InsertColumn(1, 'note', width=80)
        self.InsertColumn(2, 'date', width=80)
        self.InsertColumn(3, 'lu', width=80)
        self.InsertColumn(4, 'commence', width=80)
        self.InsertColumn(5, 'physic', width=80)
        self.InsertColumn(6, 'resume', width=80)
        self.InsertColumn(7, 'filetype', width=80)
        self.InsertColumn(8, 'complement', width=80)

        #TODO itemDataMap

    def GetListCtrl(self):
        return self

    def fillList(self,query):
        if type(query) is not Query:
            TypeError("query must be a Query object")
        self.DeleteAllItems()
        for j,i in enumerate(query):
            index = self.InsertItem(j, i.name)
            self.SetItem(index,  1, str(i.note))
            self.SetItem(index,  2, str(i.date))
            self.SetItem(index,  3, str(i.lu))
            self.SetItem(index,  4, str(i.commence))
            self.SetItem(index,  5, str(i.physic))
            self.SetItem(index,  6, str(i.resume))
            self.SetItem(index,  7, str(i.getFiletype()))
            self.SetItem(index,  8, str(i.complement))

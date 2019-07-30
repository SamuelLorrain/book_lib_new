import wx

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


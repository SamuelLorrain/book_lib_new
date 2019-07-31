import wx
from acces_files import AccessFile

class LaunchButton(wx.Button):
    def __init__(self,parent,label, booklist):
        super().__init__(parent, wx.ID_ANY, label=label)

        self.booklist = booklist
        self._query = None

        self.Bind(wx.EVT_BUTTON, self.launchBook,id=self.GetId())

    def launchBook(self,e):
        if self.booklist.GetFirstSelected() is not -1:
            print("launch book number %d" % self.booklist.GetFirstSelected())
            AccessFile.book(self._query[self.booklist.GetFirstSelected()])

    def setQuery(self,query):
        self._query = query

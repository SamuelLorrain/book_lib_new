import wx

"""
Describe the menubar layout
and behavior.
(Not complete yet!)
"""
class BookLibraryMenuBar(wx.MenuBar):
    def __init__(self):
        super().__init__()

        self.FileMenuInit()
        self.EditMenuInit()
        self.ToolMenuInit()
        self.HelpMenuInit()

        self.Append(self.fileMenu, '&File')
        self.Append(self.editMenu, '&Edit')
        self.Append(self.toolMenu, '&Tool')
        self.Append(self.helpMenu, '&Help')


    """
    File:
    - Export
    - Preferences
    - Quit
    """
    def FileMenuInit(self):
        self.fileMenu = wx.Menu()

        self.exportItem = self.fileMenu.Append(wx.ID_ANY,
                '&Export...\tCtrl+E', 'Export books to a tablet or a phone etc.')
        self.fileMenu.InsertSeparator(1)
        self.preferenceItem = self.fileMenu.Append(wx.ID_ANY,
                '&Préférences...\tCtrl+P', 'Préférences')
        self.quitItem = self.fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit Application')

    """
    Edit:
    - Undo
    - Redo
    """
    def EditMenuInit(self):
        self.editMenu = wx.Menu()
        self.undoItem = self.editMenu.Append(wx.ID_UNDO, "Undo\tCtrl+u",
                "Action Précédente")
        self.redoItem = self.editMenu.Append(wx.ID_REDO, "Redo\tCtrl+r",
                "Action Suivante")

    """
    Tool:
    - Add Book
    - Add:
        - Subject
        - Genre
        - Author
    - Modifier:
        - Book
        - Subject
        - Author
        - Genre
    """
    def ToolMenuInit(self):
        self.toolMenu = wx.Menu()

        self.addMenu = wx.Menu()
        self.modMenu = wx.Menu()

        self.addBookItem = self.toolMenu.Append(wx.ID_ANY, "Add Book...\tCtrl+N",
                "Ajouter un livre")

        self.addSubjectItem = self.addMenu.Append(wx.ID_ANY, "Subject...",
                "Ajouter un sujet")
        self.addGenreItem = self.addMenu.Append(wx.ID_ANY, "Genre...",
                "Ajouter un genre")
        self.addAuthorItem = self.addMenu.Append(wx.ID_ANY, "Author...",
                "Ajouter un auteur")

        self.modBookItem = self.modMenu.Append(wx.ID_ANY, "Book...",
                "Ajouter un livre")
        self.modSubjectItem = self.modMenu.Append(wx.ID_ANY, "Subject...",
                "Ajouter un sujet")
        self.modGenreItem = self.modMenu.Append(wx.ID_ANY, "Genre...",
                "Ajouter un genre")
        self.modAuthorItem = self.modMenu.Append(wx.ID_ANY, "Author...",
                "Ajouter un auteur")

        self.toolMenu.Append(wx.ID_ANY, 'Add', self.addMenu)
        self.toolMenu.Append(wx.ID_ANY, 'Modifier', self.modMenu)

    """
    Help:
        - A propos
    """
    def HelpMenuInit(self):
        self.helpMenu = wx.Menu()
        self.aproposItem = self.helpMenu.Append(wx.ID_ANY, 'À &propos...',
                'Get information about the application')


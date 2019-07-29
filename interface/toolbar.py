import wx

"""
Describe the menubar layout
and behavior.
(Not complete yet!)
"""
class BookLibraryToolBar(wx.ToolBar):
    def __init__(self,frame):
        super().__init__()
        self.frame = frame
        self.InitUI()

    def InitUI(self):
        self.toolbar = self.frame.CreateToolBar()
        self.toolbar.SetToolSeparation(10)

        #TODO fetch more generic icons ?
        self.undo = self.toolbar.AddTool(wx.ID_UNDO,
                'Undo',
                wx.Bitmap('/usr/share/icons/gnome/32x32/actions/gtk-undo-ltr.png'))
        self.redo = self.toolbar.AddTool(wx.ID_REDO,
                'Redo',
                wx.Bitmap('/usr/share/icons/gnome/32x32/actions/gtk-redo-ltr.png'))
        self.toolbar.AddSeparator()
        self.add = self.toolbar.AddTool(wx.ID_ANY,
                'Add Book',
                wx.Bitmap('/usr/share/icons/gnome/32x32/actions/gtk-add.png'))
        self.properties = self.toolbar.AddTool(wx.ID_ANY,
                'Change Book',
                wx.Bitmap('/usr/share/icons/gnome/32x32/actions/gtk-properties.png'))
        self.export = self.toolbar.AddTool(wx.ID_ANY,
                'Export Book',
                wx.Bitmap('/usr/share/icons/gnome/32x32/actions/gtk-save-as.png'))
        self.toolbar.Realize()


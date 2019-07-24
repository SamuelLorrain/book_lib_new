from main_comportement import *
import main_layout
from wx import App

class BookLibrary(App):
    def OnInit(self):
        mainFrame = main_layout.MainFrame(None,"Book Library")
        comportement = Comportement(mainFrame)
        mainFrame.Show()
        self.SetTopWindow(mainFrame)
        return True

if __name__ == "__main__":
    app = BookLibrary()
    app.MainLoop()

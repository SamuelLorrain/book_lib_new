from interface.main_behavior import *
import interface.main_layout
from wx import App

"""
Main class, call the Main Window (frame),
and loop on it
OnInit is derived from wx.App
and have more or less the same purpose
as __init__
"""

class BookLibrary(App):
    def OnInit(self):
        mainFrame = interface.main_layout.MainFrame(None,"Book Library")
        """
        Init of all behavior,
        communication between elements
        """
        behavior = Behavior(mainFrame)
        #mainFrame.panelLeft.launchButton.setQuery(behavior.query)
        #mainFrame.panelRight.bookList.setQuery(behavior.query)
        #behavior.setQuery(select_items.SelectItems.like('book','A'))

        mainFrame.Show()
        self.SetTopWindow(mainFrame)
        return True

if __name__ == "__main__":
    app = BookLibrary()
    app.MainLoop()

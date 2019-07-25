import config

"""
Undo/Redo object, implemented
as a simple pile like object.
"""

class History:
    def __init__(self):
        self.history = []
        self.currentItem = -1 #point to the last history item until we do
                              #undo/redo

    def setQueryHistory(self,query):
        if len(self.history) >= config.configuration['HISTORY']['historyLength']:
            self.history.pop(0)
            self.currentItem -= 1

        if self.canRedo(): #check redo
            self.history = self.history[:self.currentItem + 1]
            self.history.append(query)
            self.currentItem += 1
        else:
            self.history.append(query)
            self.currentItem += 1


    def canRedo(self):
        return self.currentItem < (len(self.history) - 1)

    def canUndo(self):
        return self.currentItem > 0

    def undoQuery(self):
        if self.canUndo():
            self.currentItem -= 1
            return self.history[self.currentItem]

    def redoQuery(self):
        if self.canRedo():
            self.currentItem += 1
            return self.history[self.currentItem]

    def getCurrentQuery(self):
        if self.currentItem < 0:
            return None
        return self.history[self.currentItem]

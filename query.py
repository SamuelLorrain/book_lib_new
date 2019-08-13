"""
Query handle in-app query.

Do not confuse with tables files.
"""
class Query:
    def __init__(self):
        self.i = 0
        self.query = []
        self.searchQuery = []

    @property
    def getQuery(self):
        return self.query

    def setQuery(self,newQuery):
        #self.history.setQueryHistory(newQuery)
        self.query = newQuery
        self.i = 0

    def __setitem__(self,index,value):
        self.query[index] = value

    def __getitem__(self,index):
        return self.query[index]

    def __iter__(self):
        return self.query.__iter__()

    def next(self):
        if i < len(self.query):
            oldi = i
            i += 1
            return self.query[oldi]
        else:
            raise StopIteration()


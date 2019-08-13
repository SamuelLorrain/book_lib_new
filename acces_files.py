import tables.complex_table
import config
import tools
import subprocess

"""
Methods to read books, books complements, or summary
"""
class AccessFile:
    path = config.configuration['PATH']['rootPath']
    bookPath = config.configuration['PATH']['bookPath']
    complementPath = config.configuration['PATH']['complementPath']
    resumePath = config.configuration['PATH']['resumePath']

    @classmethod
    def book(cls, book):
       thisBookPath = cls.path+cls.bookPath
       filetype = book.getFiletype().name.lower()
       bookfilename = tools.construct_filename(book.name,filetype)
       thisBookPath = thisBookPath+'/'+bookfilename
       print(thisBookPath)
       subprocess.Popen([config.configuration['READER'][filetype+'Reader'],thisBookPath])

    @classmethod
    def complement():
        #TODO
        pass

    @classmethod
    def resume():
        #TODO
        pass


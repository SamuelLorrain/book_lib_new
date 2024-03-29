from tables.bind_table import *
from tools import normalize_field
import database.sqliteConnect
import constant

"""
SimpleTypes represent atomic objects
in the database.
SimplesTypes that contains
only those attributs:
    - a name
    - a rowid
Edition, Author, Genre, Subject, Filetype
are all 4 types derived from SimpleType (they are
used only for type comparaison and interface simplicity).
It's a data mapper who dialog with the
database.

==============================================

#To use it, first, create a new object
t = SimpleType('subject','subjectName')

#Then add it to the database with
t.add() #(it will execute the corresponding SQL query)

#you can remove it from the database with
t.remove()  #(it will execute the corresponding SQL query)

==============================================

- We can compare the equality of two simple types (__eq__)
- 'name', and 'rowid' are accessible via @property and @setter method
- table name is accessible via 'table' @property
"""
class SimpleType:
    _string = [
        "UPDATE {} SET name = ? WHERE rowid = ?",
        "INSERT INTO {} VALUES(?)",
        "SELECT rowid FROM {} WHERE name = ?",
        "DELETE FROM {} WHERE rowid = ?",
        "SELECT * FROM {}book WHERE {}_id = ? and book_id = ?",
        "SELECT rowid FROM {} WHERE rowid = ?",
            ]

    def __init__(self,table,name,rowid=None):

        if table not in constant.SIMPLETABLES:
            raise TypeError
        self._table = table
        self._db = database.sqliteConnect.Db.getDB()
        self._cursor = database.sqliteConnect.Db.getCursor()

        #TODO test, add the rowid only if it exists in the DB
        self._rowid = rowid
        self._name = normalize_field(name)

    @property
    def table(self):
        return self._table

    @property
    def rowid(self):
        return self._rowid

    @rowid.setter
    def rowid(self,value):
        #change only if the rowid has never been initialised
        #in fact, DON'T USE THIS METHOD
        if self._rowid:
            raise ValueError("Unable to modify an existant rowid")
        self._cursor.execute(SimpleType._string[5].format(self._table), (value,))
        fetch = self._cursor.fetchone()
        if not fetch:
            raise ValueError("Unable to modify a non-existant rowid")
        self._rowid = value


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        self._name = normalize_field(value)
        if self._rowid:
            self._db.execute(SimpleType._string[0].format(self._table),
                    (self._name, self._rowid))
            self._db.commit()
        else:
            pass #TODO gérer le cas

    def add(self):
        if self._rowid:
            raise ValueError("Impossible d'ajouter un élément déjà existant")

        self._db.execute(SimpleType._string[1].format(self._table),(self._name,))
        self._db.commit()

        self._cursor.execute(SimpleType._string[2].format(self._table),
                (self._name,))
        self._rowid = self._cursor.fetchone()[0]

    def remove(self):
        if not self._rowid:
            raise ValueError("Impossible de supprimer un élément qui n'existe"
                    " pas")

        self._db.execute(SimpleType._string[3].format(self._table),(self._rowid,))
        self._db.commit()
        self._rowid = None

    def __str__(self):
        return "{}|{}".format(self._rowid,self._name)

    def __repr__(self):
        a = "rowid : {}".format(self._rowid)
        b = "name : {}".format(self._name)
        return a+'\n'+b

    def __eq__(self, a):
        return (self._rowid == a.rowid) and (self._table == a._table)

class Edition(SimpleType):
    def __init__(self,name,rowid=None):
        super(Edition,self).__init__('edition',name,rowid)

class Author(SimpleType):
    def __init__(self,name,rowid=None):
        super(Author,self).__init__('author',name,rowid)

class Genre(SimpleType):
    def __init__(self,name,rowid=None):
        super(Genre,self).__init__('genre',name,rowid)

class Subject(SimpleType):
    def __init__(self,name,rowid=None):
        super(Subject,self).__init__('subject',name,rowid)

class Filetype(SimpleType):
    def __init__(self,name,rowid=None):
        super(Filetype,self).__init__('filetype',name,rowid)


import tables.simple_table
import tables.complex_table
import database.sqliteConnect
import constant

"""
DB Types to map N:N relations.
Authorbook, Genrebook, and Subjectbook all inhérit from
BindType which define CRUD-like operations (add,remove)
to bind book and author,genre,subject together
in the DB. Subtypes are used for type comparaison and
interface only.

BindType contains:
    - col_one
    - col_two
    - rowid

========================================================
#first create a BindType object:
b = AuthorBook(SimpleType_author,SimpleType_book)

#then add it to de database
b.add()

#you can also remove it from the database
b.remove()

========================================================

- We can compare two BindType (__eq__)
- rowid, col_one, col_two are accessible via @property and @setter methods
- table, col_one_name, col_two_name are property that contains tables name
"""


class BindType:
    _string = [
            "INSERT INTO {} VALUES(?,?)",
            "SELECT rowid FROM {} WHERE {}_id = ? and {}_id = ?",
            "DELETE FROM {} WHERE rowid = ?"
            ]
    def __init__(self,table,col_one_name,col_two_name,col_one=None,col_two=None,rowid=None):
        if table not in constant.BINDTABLES:
            raise TypeError
        if col_one_name not in constant.SIMPLETABLES+constant.COMPLEXTABLES:
            raise TypeError
        if col_two_name not in constant.SIMPLETABLES+constant.COMPLEXTABLES:
            raise TypeError
        self._table = table
        self._col_one_name = col_one_name.lower()
        self._col_two_name = col_two_name.lower()
        """
        Subtypes must check attributs
        col_one and col_two.
        """
        #TODO check, set rowid only if it exists in the tables
        #(todo for all types)
        self._rowid = rowid
        self._col_one = col_one
        self._col_two = col_two

        self._db = database.sqliteConnect.Db.getDB()
        self._cursor = database.sqliteConnect.Db.getCursor()

    @property
    def rowid(self):
        return self._rowid

    @rowid.setter
    def rowid(self,value):
        #change only if the rowid has never been initialised
        #in fact, DON'T USE THIS METHOD
        if self._rowid:
            raise ValueError("Unable to modify an existant rowid")
        self._cursor.execute("SELECT rowid from book where rowid = ?",(value,))
        fetch = self._cursor.fetchone()
        if not fetch:
            raise ValueError("Unable to modify a non-existant rowid")
        self._rowid = value

    @property
    def col_one(self):
        return self._col_one

    @col_one.setter
    def col_one(self,value):
        #TODO
        pass

    @property
    def col_two(self):
        return self._col_two

    @col_two.setter
    def col_two(self,value):
        #TODO
        pass

    @property
    def col_one_name(self):
        return self._col_one_name

    @property
    def col_two_name(self):
        return self._col_two_name

    def add(self):
        if self._rowid:
            raise ValueError("Unable to add element who already exist")
        self._db.execute(BindType._string[0].format(self._table),
                (self._col_one.rowid,self._col_two.rowid))
        self._db.commit()
        self._cursor.execute(BindType._string[1].format(self._table,
            self._col_one_name,self._col_two_name),
                (self._col_one.rowid,self._col_two.rowid))
        self._rowid = self._cursor.fetchone()[0]
        return self #to keep ?

    def remove(self):
        if not self._rowid:
            raise ValueError("Unable to delete an element who doesn't exist")
        self._db.execute(BindType._string[2].format(self._table),(self._rowid,))
        self._db.commit()
        self._rowid = None
        return self #to keep ?

    def __repr__(self):
        string = "{} <==> {}\n".format(self._col_one.rowid, self.col_two.rowid)
        string += "{} <==> {}".format(self._col_one.name, self.col_two.name)
        return string

    def __str__(self):
        string = "{} <==> {}\n".format(self._col_one.rowid, self.col_two.rowid)
        string += "{} <==> {}".format(self._col_one.name, self.col_two.name)
        return string

    def __eq__(self,a):
        return (self._rowid == a.rowid) and (self._table == a._table)


"""
AuthorBook, GenreBook, SujbectBook inhérit from BindType,
the only special operations they all have is type checking.
"""
class AuthorBook(BindType):
    def __init__(self,col_one=None,col_two=None,rowid=None):
        if col_one and (type(col_one) is not simple_table.Author):
            raise TypeError("col_one must be None or Author object")
        if col_two and (type(col_two) is not complex_table.Book):
            raise TypeError("col_two must be None or Book object")
        super(AuthorBook,self).__init__('authorbook',
                'author','book',col_one,col_two,rowid)

class GenreBook(BindType):
    def __init__(self,col_one=None,col_two=None,rowid=None):
        if col_one and (type(col_one) is not simple_table.Genre):
            raise TypeError("col_one must be None or Genre object")
        if col_two and (type(col_two) is not complex_table.Book):
            raise TypeError("col_two must be None or Book object")
        super(GenreBook,self).__init__('genrebook',
                'genre','book',col_one,col_two,rowid=None)

class SubjectBook(BindType):
    def __init__(self,col_one=None,col_two=None,rowid=None):
        if col_one and (type(col_one) is not simple_table.Subject):
            raise TypeError("col_one must be None or Subject object")
        if col_two and (type(col_two) is not complex_table.Book):
            raise TypeError("col_two must be None or Book object")
        super(SubjectBook,self).__init__('subjectbook',
                'subject','book',col_one,col_two,rowid=None)

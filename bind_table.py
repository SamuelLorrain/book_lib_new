import simple_table
import complex_table
import sqliteConnect
import constant

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
        #!! les sous types doivent checker les variables
        #col_One et col_Two pour qu'elles correspondent
        #à des tables en particulier
        #TODO check, ne met le rowid que si il existe dans la base
        #(à faire pour tous les types!)
        self._rowid = rowid
        self._col_one = col_one
        self._col_two = col_two

        self._db = sqliteConnect.Db.getDB()
        self._cursor = sqliteConnect.Db.getCursor()

    @property
    def rowid(self):
        return self._rowid

    @property
    def col_one(self):
        return self._col_one

    @property
    def col_two(self):
        return self._col_two

    def add(self):
        if self._rowid:
            raise ValueError("Impossible d'ajouter un élément déjà existant")
        self._db.execute(BindType._string[0].format(self._table),
                (self._col_one.rowid,self._col_two.rowid))
        self._db.commit()
        self._cursor.execute(BindType._string[1].format(self._table,
            self._col_one_name,self._col_two_name),
                (self._col_one.rowid,self._col_two.rowid))
        self._rowid = self._cursor.fetchone()[0]
        return self #à voir si on garde ?

    def remove(self):
        if not self._rowid:
            raise ValueError("Impossible de supprimer un élément qui n'existe"
                    " pas")
        self._db.execute(BindType._string[2].format(self._table),(self._rowid,))
        self._db.commit()
        self._rowid = None
        return self #à voir si on garde?

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

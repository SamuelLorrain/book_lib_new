from tables import simple_table
import database.sqliteConnect
import constant
from tools import normalize_field

#
#TODO Test functions on filetype_id and edition_id
#

"""
Book is the type that represent books in the database.
Book contains:
    - note
    - name
    - date
    - lu (read)
    - commence (beginned)
    - physic
    - resume (summary)
    - complement
    - rowid

========================================================

#To use it, first, create a new book
book = Book('name')

#Then add it to the database with
book.add() #(it will execute the corresponding SQL query)

#you can remove it from the database with
book.remove()  #(it will execute the corresponding SQL query)

========================================================

All attribut are accessible via @property and @setter methods

We can fetch some informations about the books with those methods:
getAuthor(), getGenre(),
getSubject(), getFiletype(),
getEdition()

"""
class Book:
    _string = []
    def __init__(self,
            name,
            note=5,
            date=None,
            lu=False,
            commence=False,
            physic=False,
            resume=False,
            filetype_id=None,
            edition_id=None,
            complement=False,
            rowid=None):
        self.db = database.sqliteConnect.Db.getDB()
        self.cursor = database.sqliteConnect.Db.getCursor()
        self._table = 'book'

        #TODO add rowid only if it exist in the DB

        #All fields
        self._rowid = rowid
        self._note = note
        self._name = normalize_field(name)
        self._date = date
        self._lu = lu
        self._commence = commence
        self._physic = physic
        self._resume = resume
        if type(filetype_id) == simple_table.Filetype:
            self._filetype_id = filetype_id.rowid
        else:
            self._filetype_id = filetype_id
        if type(edition_id) == simple_table.Edition:
            self._edition_id = edition_id.rowid
        else:
            self._edition_id = edition_id
        self._complement = complement

    @property
    def rowid(self):
        return self._rowid

    @rowid.setter
    def rowid(self,value):
        #get rowid only if it exists in the table,
        #but can't modify it
        if self._rowid:
            raise ValueError("Can't modify existing rowid")
        self.cursor.execute("SELECT rowid from book where rowid = ?",(value,))
        fetch = self.cursor.fetchone()
        if not fetch:
            raise ValueError("Cant' acces to inexistant rowid")
        self._rowid = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        self._name = normalize_field(value)
        if self._rowid:
            self.db.execute("UPDATE book SET name = ? "
            "WHERE rowid = ?",(self._name,self._rowid))
            self.db.commit()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self,value):
        self._date = value
        if self._rowid:
            self.db.execute("UPDATE book SET date = ? "
            "WHERE rowid = ?",(self._date,self._rowid))
            self.db.commit()

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self,value):
        self._note = value
        if self._rowid:
            self.db.execute("UPDATE book SET note = ? "
            "WHERE rowid = ?",(self._note,self._rowid))
            self.db.commit()

    @property
    def lu(self):
        return self._lu

    @lu.setter
    def lu(self,value):
        self._lu = value
        if self._rowid:
            self.db.execute("UPDATE book SET lu = ? "
            "WHERE rowid = ?",(self._lu,self._rowid))
            self.db.commit()

    @property
    def commence(self):
        return self._commence

    @commence.setter
    def commence(self,value):
        self._commence = value
        if self._rowid:
            self.db.execute("UPDATE book SET commence = ? "
            "WHERE rowid = ?",(self._commence,self._rowid))
            self.db.commit()

    @property
    def physic(self):
        return self._physic

    @physic.setter
    def physic(self,value):
        self._physic = value
        if self._rowid:
            self.db.execute("UPDATE book SET physic = ? "
            "WHERE rowid = ?",(self._physic,self._rowid))
            self.db.commit()

    @property
    def resume(self):
        return self._resume

    @resume.setter
    def resume(self,value):
        self._resume = value
        if self._rowid:
            self.db.execute("UPDATE book SET resume = ? "
            "WHERE rowid = ?",(self._resume,self._rowid))
            self.db.commit()

    @property
    def filetype_id(self):
        return self._filetype_id

    @filetype_id.setter
    def filetype_id(self,value):
        if type(value) == simple_table.Filetype:
            self._filetype_id = value.rowid
        else:
            self._filetype_id = value
        if self._rowid:
            self.db.execute("UPDATE book SET filetype_id = ? "
            "WHERE rowid = ?",(self._filetype_id,self._rowid))
            self.db.commit()

    @property
    def edition_id(self):
        return self._edition_id

    @edition_id.setter
    def edition_id(self,value):
        if type(value) == simple_table.Edition:
            self._edition_id = value.rowid
        else:
            self._edition_id = value
        if self._rowid:
            self.db.execute("UPDATE book SET edition_id = ? "
            "WHERE rowid = ?",(self._edition_id,self._rowid))
            self.db.commit()

    @property
    def complement(self):
        return self._complement

    @complement.setter
    def complement(self,value):
        self._complement = value
        if self._rowid:
            self.db.execute("UPDATE book SET complement = ? "
            "WHERE rowid = ?",(self._complement,self._rowid))
            self.db.commit()

    @property
    def table(self):
        return self._table

    #
    #DB Acces
    #
    def add(self):
        if self._rowid:
            raise ValueError("Can't add an element who already exist")

        self.db.execute("INSERT INTO book VALUES(?,?,?,?,?,?,?,?,?,?)"
                ,(self._name,self._note,self._date,self._lu,self._commence,
                    self._physic,self._resume,self._filetype_id,self._edition_id,
                    self._complement))
        self.db.commit()

        self.cursor.execute("SELECT rowid FROM"
            " book WHERE name = ?",(self._name,))
        self._rowid = self.cursor.fetchone()[0]

    def remove(self):
        if not self._rowid:
            raise ValueError("Can't remove non existent element")

        self.db.execute("DELETE FROM book WHERE rowid = ?",(self._rowid,))
        self.db.commit()
        self._rowid = None

    def getAuthor(self):
        self.cursor.execute("""SELECT name,rowid FROM author WHERE rowid IN (
                SELECT author_id FROM authorbook WHERE book_id = ?
                )""", (self._rowid,))
        fetch = self.cursor.fetchall()
        return [simple_table.Author(*i) for i in fetch]

    def getGenre(self):
        self.cursor.execute("""SELECT name,rowid FROM genre WHERE rowid IN (
                SELECT genre_id FROM genrebook WHERE book_id = ?
                )""", (self._rowid,))
        fetch = self.cursor.fetchall()
        return [simple_table.Genre(*i) for i in fetch]

    def getSubject(self):
        self.cursor.execute("""SELECT name,rowid FROM subject WHERE rowid IN (
                SELECT subject_id FROM subjectbook WHERE book_id = ?
                )""", (self._rowid,))
        fetch = self.cursor.fetchall()
        return [simple_table.Subject(*i) for i in fetch]

    def getFiletype(self):
        self.cursor.execute("""SELECT *,rowid FROM filetype WHERE rowid =
                (SELECT filetype_id FROM book WHERE rowid = ?)""",(self._rowid,))
        fetch = self.cursor.fetchone()
        return simple_table.Filetype(*fetch)

    def getEdition(self):
        self.cursor.execute("""SELECT *,rowid FROM edition WHERE rowid =
                (SELECT edition_id FROM book WHERE rowid = ?)""",(self._rowid,))
        fetch = self.cursor.fetchone()
        if fetch is None:
            return ""
        return simple_table.Genre(*fetch)

    def __str__(self):
        return 10*"{}|".format(self._rowid,self._name)

    def __repr__(self):
        #TODO more clear
        rowid = "rowid : {}".format(self._rowid)
        name = "name : {}".format(self._name)
        note = "note : {}".format(self._note)
        lu = "lu : {}".format(self._lu)
        commence = "commence : {}".format(self._commence)
        physic = "physic : {}".format(self._physic)
        resume = "resume : {}".format(self._resume)
        filetype_id = "filetype_id : {}".format(self._filetype_id)
        edition_id = "edition_id : {}".format(self._edition_id)
        complement = "complement : {}".format(self._complement)
        string1  = rowid+"\n"+name+"\n"+note+"\n"+commence+"\n"
        string2 = physic+"\n"+resume+"\n"+filetype_id+"\n"+edition_id+"\n"
        author = "author :{}\n".format(self.getAuthor())
        subject= "subject :{}\n".format(self.getSubject())
        genre = "genre :{}\n".format(self.getGenre())
        return string1+string2+complement+'\n'+author+subject+genre+"\n\n"

    def __eq__(self, a):
        if type(a) == Book:
            return (self._rowid == a.rowid)
        else:
            raise TypeError("'==' not implemented for those types")

    def __lt__(self,a):
        if type(a) == Book:
            return (self._rowid < a.rowid)
        else:
            raise TypeError("'<' not implemented for those types")

    def __le__(self,a):
        if type(a) == Book:
            return (self._rowid <= a.rowid)
        else:
            raise TypeError("'<=' not implemented for those types")

    def __hash__(self):
        return hash((self.rowid, self.table))

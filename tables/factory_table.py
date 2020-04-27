from tables.simple_table import *
from tables.complex_table import *
from tables import bind_table
import database.sqliteConnect
import tools
import constant

"""
Factory functions for tables
Use the factory_table and factory_bind
function only
(other functions are used as sub_sections of
the factory)

"""
def factory_table(tableName,value):
    """
    Return the good constructor of the table
    or a reference to an object if the table already exist.

    tableName is the table name (in the existing tables)
    value is an existing value in the DB
    to get or create the good object

    factory_table dispatch his logic in the
    _factory_table_string and _factory_table_int functions
    """
    cursor = database.sqliteConnect.Db.getCursor()
    if tableName not in (constant.SIMPLETABLES+constant.COMPLEXTABLES):
        raise TypeError("table unknown")

    if type(value) == str:
        if tableName is "book":
            cursor.execute("""SELECT
                    rowid,name,note,
                    date,lu,commence,physic,
                    resume,filetype_id,
                    edition_id,complement
                    FROM book
                    WHERE name = ?""",(tools.normalize_field(value),))
        else:
            cursor.execute("SELECT rowid,* FROM {} "
                "WHERE name = ?".format(tableName),
                (tools.normalize_field(value),))
        fetch = cursor.fetchone()
        return _factory_table_string(tableName,tools.normalize_field(value),fetch)

    elif type(value) == int:
        if tableName is "book":
            cursor.execute("""SELECT
                    rowid,name,note,
                    date,lu,commence,physic,
                    resume,filetype_id,
                    edition_id,complement
                    FROM book
                    WHERE rowid = ?""",(value,))
        cursor.execute("SELECT rowid,* FROM {} "
                "WHERE rowid = ?".format(tableName),(value,))
        fetch = cursor.fetchone()
        return _factory_table_int(tableName,value,fetch)
    else:
        raise TypeError

def factory_bind(col_one,col_two):
    """
    Return the good constructor of the bind table.
    """
    if type(col_one) is not (Author or Genre or
            Subject):
        raise TypeError('col_one must be a author, genre or subject type')
    if type(col_two) is not Book:
        raise TypeError('col_two must be a book!')

    cursor = database.sqliteConnect.Db.getCursor()
    cursor.execute("""SELECT rowid from {0}book where {0}_id = ? and book_id =
            ?""".format(col_one.table), (col_one.rowid, col_two.rowid))
    if cursor.fetchone() == None:
        bind_rowid = None
    else:
        bind_rowid = cursor.fetchone()[0]

    if type(col_one) is Author:
        return bind_table.AuthorBook(col_one,col_two,bind_rowid)
    if type(col_one) is Genre:
        return bind_table.GenreBook(col_one,col_two,bind_rowid)
    if type(col_one) is Subject:
        return bind_table.SubjectBook(col_one,col_two,bind_rowid)


def _factory_table_string(tableName : str,value : str, fetch):
    if fetch:
        if tableName == 'edition':
            tmpObject = Edition(value)
            tmpObject.rowid = fetch[0]
            return tmpObject
        if tableName == 'author':
            tmpObject = Author(value)
            tmpObject.rowid = fetch[0]
            return tmpObject
        if tableName == 'genre':
            tmpObject = Genre(value)
            tmpObject.rowid = fetch[0]
            return tmpObject
        if tableName == 'subject':
            tmpObject = Subject(value)
            tmpObject.rowid = fetch[0]
            return tmpObject
        if tableName == 'filetype':
            tmpObject = Filetype(value)
            tmpObject.rowid = fetch[0]
            return tmpObject
        if tableName == 'book':
            tmpObject = Book(value)
            tmpObject.rowid = fetch[0]
            tmpObject.note = fetch[2]
            tmpObject.date = fetch[3]
            tmpObject.lu = fetch[4]
            tmpObject.commence = fetch[5]
            tmpObject.physic = fetch[6]
            tmpObject.resume = fetch[7]
            tmpObject.filetype_id = fetch[8]
            tmpObject.edition_id = fetch[9]
            tmpObject.complement = fetch[10]
            return tmpObject
    else:
        if tableName == 'edition':
            return Edition(value)
        if tableName == 'author':
            return Author(value)
        if tableName == 'genre':
            return Genre(value)
        if tableName == 'subject':
            return Subject(value)
        if tableName == 'filetype':
            return Filetype(value)
        if tableName == 'book':
            return Book(value)
    raise TypeError("pb dans la fonction factory_table_string")

def _factory_table_int(tableName : str,value : int, fetch):
    if fetch:
        if tableName == 'edition':
            tmpObject = Edition(fetch[1],rowid=fetch[0])
            return tmpObject
        if tableName == 'author':
            tmpObject = Author(fetch[1],rowid=fetch[0])
            return tmpObject
        if tableName == 'genre':
            tmpObject = Genre(fetch[1],rowid=fetch[0])
            return tmpObject
        if tableName == 'subject':
            tmpObject = Subject(fetch[1],rowid=fetch[0])
            return tmpObject
        if tableName == 'filetype':
            tmpObject = Filetype(fetch[1],rowid=fetch[0])
            return tmpObject
        if tableName == 'book':
            tmpObject = Book(fetch[1],rowid=fetch[0])
            tmpObject.note = fetch[2]
            tmpObject.date = fetch[3]
            tmpObject.lu = fetch[4]
            tmpObject.commence = fetch[5]
            tmpObject.physic = fetch[6]
            tmpObject.resume = fetch[7]
            tmpObject.filetype_id = fetch[8]
            tmpObject.edition_id = fetch[9]
            tmpObject.complement = fetch[10]
            return tmpObject
    else:
        raise ValueError("le rowid entré n'existe pas dans la table!")


from tables import simple_table
from tables import bind_table
from tables import complex_table
from tables import factory_table
import database.sqliteConnect
import constant
from tools import normalize_field
from collections.abc import Iterable

class SelectItems:
    @classmethod
    def by(cls,value,behavior='and'):
        cursor = database.sqliteConnect.Db.getCursor()
        if isinstance(value, Iterable) and behavior == 'or':
            return cls._by_or(value)
        elif isinstance(value, Iterable) and behavior == 'and':
            return cls._by_and(value)
        elif type(value) == simple_table.Edition:
            cursor.execute("""SELECT *,rowid FROM book where edition_id = ?""",
                    (value.rowid,))
        elif type(value) == simple_table.Author:
            cursor.execute("""SELECT *,rowid FROM book where rowid IN (
                    SELECT book_id FROM authorbook WHERE author_id = ?)""",
                    (value.rowid,))
        elif type(value) == simple_table.Genre:
            cursor.execute("""SELECT *,rowid FROM book where rowid IN (
                    SELECT book_id FROM genrebook WHERE genre_id = ?)""",
                    (value.rowid,))
        elif type(value) == simple_table.Subject:
            cursor.execute("""SELECT *,rowid FROM book where rowid IN (
                    SELECT book_id FROM subjectbook WHERE subject_id = ?)""",
                    (value.rowid,))
        elif type(value) == simple_table.Filetype:
            cursor.execute("""SELECT *,rowid FROM book where filetype_id = ?""",
                    (value.rowid,))
        elif type(value) == complex_table.Book:
            return [value]
        else:
            raise TypeError("""type de l'entrée incompatible avec la sélection
                    dans la base de données""")
        #TODO Ajouter des mecanismes (commit et transaction)
        #pour la bdd (éviter qu'elle ne soit
        #modifiée entre le fetch et la création des objets Book
        fetch = cursor.fetchall()
        return [complex_table.Book(*i) for i in fetch]

    @classmethod
    def _by_or(cls,value):
        #TODO optimiser pour ne faire qu'une seule requête
        booksQueried = []
        for i in value:
            booksQueried += cls.by(i)
        return sorted(list(set(booksQueried)))

    @classmethod
    def _by_and(cls,value):
        edition = False
        filetype = False
        first = True
        stringQuery = "SELECT *,rowid FROM book WHERE \n"
        for i in value:
            if type(i) == simple_table.Edition and not edition:
                if first:
                    first = False
                elif not first:
                    stringQuery += " and "
                edition = True
                stringQuery += "edition_id = {}".format(i.rowid)
            elif type(i) == simple_table.Author:
                if first:
                    first = False
                elif not first:
                    stringQuery += " and "
                stringQuery += """rowid IN (
                SELECT book_id FROM authorbook
                WHERE author_id = {})""".format(i.rowid)
            elif type(i) == simple_table.Genre:
                if first:
                    first = False
                elif not first:
                    stringQuery += " and "
                stringQuery += """rowid IN (
                SELECT book_id FROM genrebook
                WHERE = {})""".format(i.rowid)
            elif type(i) == simple_table.Subject:
                if first:
                    first = False
                elif not first:
                    stringQuery += " and "
                stringQuery += """rowid IN (
                SELECT book_id FROM subjectbook
                WHERE subject_id = {})""".format(i.rowid)
            elif type(i) == simple_table.Filetype and not filetype:
                if first:
                    first = False
                elif not first:
                    stringQuery += " and "
                filetype = True
                stringQuery += "filetype_id = {}".format(i.rowid)
            elif type(i) == complex_table.Book:
                return list(i)
            else:
                raise TypeError("""type de l'entrée incompatible avec la sélection
                        dans la base de données""")
        cursor = database.sqliteConnect.Db.getCursor()
        cursor.execute(stringQuery)
        return [complex_table.Book(*i) for i in cursor.fetchall()]

    @classmethod
    def like(cls,tableName,value,mode='after'):
        if type(value) is not str:
            raise TypeError("""type de l'entrée de la méthode \"like\" doit
            être de type str""")
        if tableName not in constant.SIMPLETABLES+constant.COMPLEXTABLES:
            raise ValueError("""la table entrée n'existe pas""")

        cursor = database.sqliteConnect.Db.getCursor()
        if mode == 'before':
            cursor.execute(
            "SELECT *,rowid FROM {} WHERE name LIKE ? ORDER BY name ASC".format(
                tableName),('%'+normalize_field(value),))
        elif mode == 'before|after' or mode == 'after|before':
            cursor.execute(
            "SELECT *,rowid FROM {} WHERE name LIKE ? ORDER BY name ASC".format(
                tableName),('%'+normalize_field(value)+'%',))
        else:
            cursor.execute(
                    "SELECT *,rowid FROM {} WHERE name LIKE ?"
                    " ORDER BY name ASC".format(tableName),
                    (normalize_field(value)+'%',))

        #TODO utiliser une factory?
        if tableName == 'edition':
            return [simple_table.Edition(*i) for i in cursor.fetchall()]
        elif tableName == 'author':
            return [simple_table.Author(*i) for i in cursor.fetchall()]
        elif tableName == 'genre':
            return [simple_table.Genre(*i) for i in cursor.fetchall()]
        elif tableName == 'subject':
            return [simple_table.Subject(*i) for i in cursor.fetchall()]
        elif tableName == 'filetype':
            return [simple_table.Filetype(*i) for i in cursor.fetchall()]
        elif tableName == 'book':
            return [complex_table.Book(*i) for i in cursor.fetchall()]


    @classmethod
    def all(cls, tableName):
        if type(value) is not str:
            raise TypeError("""type de l'entrée de la méthode \"all\" doit
            être de type str""")
        if tableName not in constant.SIMPLETABLES+constant.COMPLEXTABLES:
            raise ValueError("""la table entrée n'existe pas""")
        cursor = database.sqliteConnect.Db.getCursor()
        cursor.execute("SELECT *,rowid FROM {} ORDER BY name ASC".format(tableName))

        if tableName == 'edition':
            return [simple_table.Edition(*i) for i in cursor.fetchall()]
        elif tableName == 'author':
            return [simple_table.Author(*i) for i in cursor.fetchall()]
        elif tableName == 'genre':
            return [simple_table.Genre(*i) for i in cursor.fetchall()]
        elif tableName == 'subject':
            return [simple_table.Subject(*i) for i in cursor.fetchall()]
        elif tableName == 'filetype':
            return [simple_table.Filetype(*i) for i in cursor.fetchall()]
        elif tableName == 'book':
            return [complex_table.Book(*i) for i in cursor.fetchall()]

import sqlite3
from config import configuration

#singleton
#TODO voir si on en fait un observer pour les commit ?
class Db:
    _db = None
    _cursor = None

    @staticmethod
    def getDB():
        if not Db._db:
            Db._db = sqlite3.connect(configuration["PATH"]["databasePath"])
        return Db._db

    @staticmethod
    def getCursor():
        if not Db._cursor:
            Db._cursor = Db.getDB().cursor()
        return Db._cursor



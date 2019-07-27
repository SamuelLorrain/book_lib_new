import database.sqliteConnect

"""
misc functions
"""

def numberOfBooks():
    db = database.sqliteConnect.Db.getDB()
    fetch = db.execute("SELECT COUNT(*) FROM book").fetchone()
    return fetch[0]


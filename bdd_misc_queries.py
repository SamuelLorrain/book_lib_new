import sqliteConnect

"""
misc functions
"""

def numberOfBooks():
    db = sqliteConnect.Db.getDB()
    fetch = db.execute("SELECT COUNT(*) FROM book").fetchone()
    return fetch[0]


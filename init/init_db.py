import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

conn = create_connection("db/score_app.db")
cur = conn.cursor()

cur.execute("CREATE TABLE tenten(id INTEGER PRIMARY KEY, tentnr INTEGER, tentchef, kampers)")
cur.execute("CREATE TABLE scores(id INTEGER PRIMARY KEY, tentnr INTEGER, score INTEGER)")
cur.execute("CREATE TABLE activiteiten(id INTEGER PRIMARY KEY, naam, type, dagdeel, themadag_onderdeel INTEGER DEFAULT 0 NOT NULL)")
cur.execute("CREATE TABLE uitslagen(id INTEGER PRIMARY KEY, activiteit, tentnr INTEGER, tentchef, snelheid, datum, punten INTEGER)")

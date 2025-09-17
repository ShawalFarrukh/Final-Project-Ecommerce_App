import sqlite3
def db_connection():
    conn = sqlite3.connect("db/app.db")
    conn.row_factory = sqlite3.Row
    return conn
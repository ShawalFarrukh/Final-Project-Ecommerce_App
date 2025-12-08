import sqlite3  
from functools import wraps
from flask import session, redirect
def db_connection():
    conn = sqlite3.connect("db/app.db")
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


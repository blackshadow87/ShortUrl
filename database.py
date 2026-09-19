import sqlite3, config
from flask import g

def init_app(app):
    create_db()
    app.teardown_appcontext(close_db)

def get_db():
    if "db" not in g:
        g.db = connect_db()
    return g.db

def connect_db():
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    with sqlite3.connect(config.DATABASE_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            target_url TEXT NOT NULL
            )
        ''')
        conn.commit()

def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

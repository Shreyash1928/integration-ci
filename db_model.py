# db_model.py
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "app.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def add_todo(title: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO todos (title) VALUES (?)", (title,))
    conn.commit()
    last_id = c.lastrowid
    conn.close()
    return last_id

def get_todo(id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title FROM todos WHERE id=?", (id,))
    row = c.fetchone()
    conn.close()
    return row

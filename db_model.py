import sqlite3
import pathlib

# SQLite DB file
DB_FILE = pathlib.Path("todos.db")


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_todo(title: str) -> int:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO todos (title) VALUES (?)",
        (title,)
    )

    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return todo_id


def get_all_todos():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM todos")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "title": row[1]}
        for row in rows
    ]

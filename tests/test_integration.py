# tests/test_integration.py
import os
import time
import threading
import requests
import pathlib
import shutil
import json
from api_service import create_api_app
from notify_service import create_notify_app
from db_model import DB_FILE, init_db

ROOT = pathlib.Path(__file__).parent.parent
NOTIF_LOG = ROOT / "notifications.log"

def run_app(app, port):
    # use app.run which is blocking, so run it in a thread
    app.run(port=port, use_reloader=False)

def setup_module(module):
    # make sure clean start
    if DB_FILE.exists():
        DB_FILE.unlink()
    if NOTIF_LOG.exists():
        NOTIF_LOG.unlink()
    init_db()

    # start notify service
    notify_app = create_notify_app()
    t1 = threading.Thread(target=run_app, args=(notify_app, 5001), daemon=True)
    t1.start()

    # small wait for server start
    time.sleep(0.6)

    # start api service
    api_app = create_api_app()
    t2 = threading.Thread(target=run_app, args=(api_app, 5000), daemon=True)
    t2.start()

    time.sleep(0.6)  # allow both to be ready

def test_create_todo_and_notification():
    # create a todo via api service
    r = requests.post("http://127.0.0.1:5000/todos", json={"title": "buy milk"})
    assert r.status_code == 201
    data = r.json()
    todo_id = data["id"]
    assert data["title"] == "buy milk"

    # check DB row exists
    import sqlite3
    import pathlib
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title FROM todos WHERE id=?", (todo_id,))
    row = c.fetchone()
    conn.close()
    assert row is not None
    assert row[1] == "buy milk"

    # wait a moment for notify log to be written
    time.sleep(0.3)
    assert NOTIF_LOG.exists()
    with NOTIF_LOG.open("r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    assert len(lines) >= 1
    # last line should contain our todo id/title
    payload = json.loads(lines[-1])
    assert payload["title"] == "buy milk"
    assert payload["todo_id"] == todo_id

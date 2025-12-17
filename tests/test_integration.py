# tests/test_integration.py
import time
import threading
import requests
import pathlib
import json
import sqlite3

from api_service import create_api_app
from notify_service import create_notify_app
from db_model import DB_FILE, init_db

ROOT = pathlib.Path(__file__).parent.parent
NOTIF_LOG = ROOT / "notifications.log"


def run_app(app, port):
    # Explicit host for CI compatibility
    app.run(host="127.0.0.1", port=port, use_reloader=False)


def setup_module(module):
    """
    Integration test setup:
    - Clean database
    - Start notify service
    - Start API service
    """

    # Clean previous state
    if DB_FILE.exists():
        DB_FILE.unlink()

    if NOTIF_LOG.exists():
        NOTIF_LOG.unlink()

    init_db()

    # Start notification service
    notify_app = create_notify_app()
    notify_thread = threading.Thread(
        target=run_app, args=(notify_app, 5001), daemon=True
    )
    notify_thread.start()

    time.sleep(0.5)

    # Start API service
    api_app = create_api_app()
    api_thread = threading.Thread(
        target=run_app, args=(api_app, 5000), daemon=True
    )
    api_thread.start()

    time.sleep(0.5)


def test_create_todo_and_notification():
    """
    Integration test:
    API -> Database -> Notification Service
    """

    # Create TODO via API
    response = requests.post(
        "http://127.0.0.1:5000/todos",
        json={"title": "buy milk"},
        timeout=5,
    )

    assert response.status_code == 201

    data = response.json()
    todo_id = data["id"]

    assert data["title"] == "buy milk"

    # Verify DB entry
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM todos WHERE id=?", (todo_id,))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[1] == "buy milk"

    # Verify notification log
    time.sleep(0.3)
    assert NOTIF_LOG.exists()

    with NOTIF_LOG.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 1

    payload = json.loads(lines[-1])
    assert payload["title"] == "buy milk"
    assert payload["todo_id"] == todo_id

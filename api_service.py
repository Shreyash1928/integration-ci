# api_service.py
from flask import Flask, request, jsonify
import requests
from db_model import init_db, add_todo
from pathlib import Path
import os

NOTIFY_URL = "http://127.0.0.1:5001/notify"

def create_api_app():
    app = Flask("api_service")
    init_db()

    @app.route("/todos", methods=["POST"])
    def create_todo():
        data = request.get_json() or {}
        title = data.get("title")
        if not title:
            return jsonify({"error": "title required"}), 400

        todo_id = add_todo(title)

        # Call notification service
        try:
            requests.post(NOTIFY_URL, json={"todo_id": todo_id, "title": title}, timeout=2)
        except requests.RequestException:
            # For integration test, we don't crash if notification service is down.
            pass

        return jsonify({"id": todo_id, "title": title}), 201

    return app

if __name__ == "__main__":
    app = create_api_app()
    app.run(port=5000, debug=False)

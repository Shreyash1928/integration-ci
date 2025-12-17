from flask import Flask, request, jsonify
from db_model import add_todo, get_all_todos
import requests

def create_api_app():
    app = Flask(__name__)

    @app.route("/todos", methods=["POST"])
    def create_todo():
        data = request.json
        todo_id = add_todo(data["title"])

        # notify service
        requests.post(
            "http://127.0.0.1:5001/notify",
            json={"todo_id": todo_id, "title": data["title"]},
            timeout=5
        )

        return jsonify({"id": todo_id, "title": data["title"]}), 201

    @app.route("/todos", methods=["GET"])
    def list_todos():
        return jsonify(get_all_todos()), 200

    return app

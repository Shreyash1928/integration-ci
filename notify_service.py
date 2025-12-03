# notify_service.py
from flask import Flask, request, jsonify
from pathlib import Path
import json

NOTIF_LOG = Path(__file__).parent / "notifications.log"

def create_notify_app():
    app = Flask("notify_service")

    @app.route("/notify", methods=["POST"])
    def notify():
        payload = request.get_json() or {}
        # append to a simple log so integration test can assert
        with NOTIF_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
        return jsonify({"status": "ok"}), 200

    return app

if __name__ == "__main__":
    app = create_notify_app()
    app.run(port=5001, debug=False)

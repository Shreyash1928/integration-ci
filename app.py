from flask import Flask, jsonify, request
from api_service import create_item, get_items

app = Flask(__name__)

@app.route("/items", methods=["POST"])
def add_item():
    data = request.json
    result = create_item(data)
    return jsonify(result), 201

@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(get_items()), 200

if __name__ == "__main__":
    app.run(debug=True)

Integration Todo – Microservice Integration Test Project

This project demonstrates two Flask microservices and an integration test that verifies real communication between them.

🚀 Project Structure
integration-todo/
│
├── api_service.py          # Todo API service (port 5000)
├── notify_service.py       # Notification service (port 5001)
├── db_model.py             # SQLite helper functions
├── app.db                  # SQLite database
├── notifications.log       # Notification log file
│
├── tests/
│   └── test_integration.py # Full integration test
│
├── requirements.txt
└── README.md

📌 API Service (port 5000)
Endpoint:
POST /todos

Request body:

{
  "title": "Learn Flask"
}


This service:

Saves todo in SQLite (app.db)

Sends a POST request to the Notification Service

📌 Notification Service (port 5001)
Endpoint:
POST /notify

It appends the received JSON into notifications.log:

{"todo_id": 1, "title": "Learn Flask"}

🛠️ Installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

▶️ Running the Services

Start Notification Service:

python notify_service.py


Start API Service (in another terminal):

python api_service.py

🧪 Running Integration Tests

Before running tests:

STOP any running services (Ctrl + C)

Pytest will start services automatically

Run:

pytest -q

📂 Check SQLite DB Content

To check saved todos:

sqlite3 app.db "SELECT * FROM todos;"

📁 Check Notification Logs

Open:

notifications.log


Sample:

{"todo_id": 1, "title": "Learn Flask"}
{"todo_id": 2, "title": "hello"}

🎯 Project Summary

This project demonstrates:

Flask microservices

SQLite database usage

Service-to-service communication

Logging

Automated integration testing using pytest + requests

It’s a simple but complete example of microservice integration workflows.
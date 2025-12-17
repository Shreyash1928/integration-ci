import pytest
from app import app   # 👈 this imports app.py from ROOT

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

from fastapi.testclient import TestClient
import sys
sys.path.append('../')
from main import app  


client = TestClient(app)


def test_send_message():
    response = client.post("/messages", json={"text": "Hello, world!"})
    assert response.status_code == 200
    assert "timestamp" in response.json()


def test_get_messages():
    response = client.get("/messages")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_message_count():
    response = client.get("/messages/count")
    assert response.status_code == 200
    assert "count" in response.json()
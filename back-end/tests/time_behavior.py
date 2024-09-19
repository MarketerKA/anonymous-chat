import requests
import time


def test_time_behavior():
    url = "http://127.0.0.1:8000/messages"
    message_data = {"text": "Test message"}

    start_time = time.time()
    response = requests.post(url, json=message_data)
    end_time = time.time()

    response_time = end_time - start_time
    print(f"Response Time: {response_time:.3f} seconds")

    # Check if the response time is within acceptable limits (e.g., 500ms)
    assert response.status_code == 200
    assert response_time <= 0.5, f"Performance issue: Response time {response_time:.3f} exceeded limit."


test_time_behavior()

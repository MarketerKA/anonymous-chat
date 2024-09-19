# server.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

messages = []

class Message(BaseModel):
    text: str

@app.post("/messages")
def send_message(message: Message):
    new_message = {"text": message.text, "timestamp": str(datetime.now())}
    messages.append(new_message)
    return new_message

@app.get("/messages")
def get_messages():
    return messages

@app.get("/messages/count")
def get_message_count():
    return {"count": len(messages)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

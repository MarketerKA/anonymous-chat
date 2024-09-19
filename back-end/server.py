from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

messages = []  # List for storing messages
active_connections: List[WebSocket] = []  # List of active WebSocket connections

class Message(BaseModel):
    text: str

async def broadcast_message(message: dict, sender: WebSocket = None):
    """Broadcast a message to all connected clients except the sender."""
    for connection in active_connections:
        if connection != sender:
            await connection.send_json(message)

@app.post("/messages")
async def send_message(message: Message):
    """Handle sending a new message via POST request."""
    new_message = {"text": message.text, "timestamp": str(datetime.now())}
    messages.append(new_message)
    await broadcast_message(new_message)  # Send new message to all active connections
    return new_message

@app.get("/messages")
def get_messages():
    """Retrieve all messages."""
    return messages

@app.get("/messages/count")
def get_message_count():
    """Return the current count of messages."""
    return {"count": len(messages)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            await websocket.receive_text()  # Wait for messages from client if needed
    except WebSocketDisconnect:
        active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

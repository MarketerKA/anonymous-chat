from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Позволяет всем доменам отправлять запросы, можно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

messages = []  # Список для хранения сообщений
active_connections: List[WebSocket] = []  # Список активных WebSocket соединений

class Message(BaseModel):
    text: str

async def broadcast_message(message: dict):
    """Отправка сообщения всем подключенным клиентам."""
    for connection in active_connections:
        await connection.send_json(message)

@app.post("/messages")
async def send_message(message: Message):
    """Обработка отправки нового сообщения через POST запрос."""
    new_message = {"text": message.text, "timestamp": str(datetime.now())}
    messages.append(new_message)
    await broadcast_message(new_message)  # Отправка нового сообщения всем активным соединениям
    return new_message

@app.get("/messages")
def get_messages():
    """Получение всех сообщений."""
    return messages

@app.get("/messages/count")
def get_message_count():
    """Возвращает текущее количество сообщений в чате."""
    return {"count": len(messages)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Обработка WebSocket соединений."""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Ожидание сообщений от клиента, если требуется
    except WebSocketDisconnect:
        active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

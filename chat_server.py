
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import torch
import torch.nn as nn

# ======== Модель (заглушка — подставьте свою из image_model.py, classifier.py и т.д.) ========
class SimpleChatModel(nn.Module):
    def __init__(self):
        super(SimpleChatModel, self).__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)

    def chat(self, message: str) -> str:
        # Имитация обработки сообщения
        return f"Принято: '{message}'. Модель думает, что это интересно!"

# ======== Инициализация ========
app = FastAPI()
model = SimpleChatModel()

# ======== Pydantic модель запроса ========
class ChatRequest(BaseModel):
    message: str

# ======== Веб-интерфейс ========
@app.get("/", response_class=HTMLResponse)
async def get():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Нейро-чат</title>
        <style>
            body { font-family: Arial; padding: 20px; max-width: 600px; margin: auto; }
            .msg { margin: 10px 0; }
            .user { color: blue; }
            .bot { color: green; }
        </style>
    </head>
    <body>
        <h1>Чат с нейросетью</h1>
        <div id="chat"></div>
        <input id="msgInput" type="text" placeholder="Введите сообщение..." style="width: 80%;">
        <button onclick="sendMessage()">Отправить</button>
        <script>
            async function sendMessage() {
                const input = document.getElementById("msgInput");
                const message = input.value;
                if (!message) return;
                document.getElementById("chat").innerHTML += '<div class="msg user"><b>Вы:</b> ' + message + '</div>';
                input.value = "";
                const res = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message })
                });
                const data = await res.json();
                document.getElementById("chat").innerHTML += '<div class="msg bot"><b>Бот:</b> ' + data.response + '</div>';
            }
        </script>
    </body>
    </html>
    """

# ======== API чат ========
@app.post("/chat")
async def chat(req: ChatRequest):
    user_message = req.message
    response = model.chat(user_message)
    return JSONResponse(content={"response": response})

# ======== Запуск ========
if __name__ == "__main__":
    uvicorn.run("chat_server:app", host="0.0.0.0", port=8000, reload=True)

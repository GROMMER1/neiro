from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model import NeuralResponder
from utils import find_best_match, save_to_database

app = FastAPI()
responder = NeuralResponder()

# Разрешим CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(msg: Message):
    prompt = msg.text.strip()
    if not prompt:
        return {"response": "Пожалуйста, введите сообщение."}
    
    # Сначала ищем в базе знаний
    answer = find_best_match(prompt)
    if answer:
        return {"response": answer}
    
    # Если нет — вызываем нейросеть
try:
    global responder
    if 'responder' not in globals():
        responder = NeuralResponder()
    answer = responder.generate_response(prompt)
except Exception as e:
    print(f"Ошибка генерации: {e}")
    answer = "Ошибка генерации ответа."
@app.get("/reset")
async def reset_history():
    responder.reset_history()
    return {"status": "История очищена"}
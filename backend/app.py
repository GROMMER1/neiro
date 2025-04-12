
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from backend.responder_module import NeuralResponder

app = FastAPI()

# Ленивая инициализация модели
responder = None

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(prompt: Prompt):
    global responder
    try:
        if responder is None:
            responder = NeuralResponder()
        answer = responder.generate_response(prompt.prompt)
    except Exception as e:
        print(f"Ошибка генерации: {e}")
        raise HTTPException(status_code=500, detail="Ошибка генерации ответа.")
    return {"response": answer}

# Подключение фронтенда
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/dist")
app.mount("/static", StaticFiles(directory=frontend_path, html=True), name="static")

@app.get("/")
async def serve_root():
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path)

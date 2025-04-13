
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from backend.responder_module import NeuralResponder

app = FastAPI()

# Указываем путь к frontend/dist
frontend_path = Path(__file__).resolve().parent.parent / "frontend" / "dist"

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory=frontend_path, html=True), name="static")

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(prompt: Prompt):
    try:
        if 'responder' not in globals():
            global responder
            responder = NeuralResponder()
        answer = responder.generate_response(prompt.prompt)
    except Exception as e:
        print(f"Ошибка генерации: {e}")
        answer = "Ошибка генерации ответа."
    return {"response": answer}

# Отдаём index.html для любых маршрутов (SPA)
@app.get("/{path:path}")
async def serve_spa(path: str):
    index_file = frontend_path / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"detail": "index.html not found"}

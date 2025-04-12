from fastapi.responses import FileResponse
from fastapi import FastAPI, Request
from pydantic import BaseModel
from backend.responder_module import NeuralResponder

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(prompt: Prompt):
    try:
        if 'responder' not in globals():
            responder = NeuralResponder()
        answer = responder.generate_response(prompt.prompt)
    except Exception as e:
        print(f"Ошибка генерации: {e}")
        answer = "Ошибка генерации ответа."
    return {"response": answer}

@app.get("/")
async def serve_root():
    return FileResponse(frontend_path / "index.html")


@app.get("/{path:path}")
async def serve_spa(path: str):
    return FileResponse(frontend_path / "index.html")

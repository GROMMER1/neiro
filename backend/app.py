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
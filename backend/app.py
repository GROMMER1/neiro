import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils import save_uploaded_file, extract_text_from_file
from training.trainer import retrain_model

from model import load_neural_responder_lazy

app = FastAPI()

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ленивый загрузчик модели
responder = None

@app.on_event("startup")
def load_model():
    global responder
    responder = load_neural_responder_lazy()

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    filepath = await save_uploaded_file(file)
    text = extract_text_from_file(filepath)
    if not text:
        return JSONResponse(content={"error": "Не удалось извлечь текст из файла."}, status_code=400)

    with open("knowledge/data.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{text}\n")

    return {"message": "Файл успешно загружен и сохранён."}

@app.post("/api/train")
async def train_model():
    success = retrain_model()
    if success:
        return {"message": "Модель успешно переобучена."}
    return JSONResponse(content={"error": "Обучение не удалось."}, status_code=500)

@app.post("/api/chat")
async def chat(message: str = Form(...)):
    if responder is None:
        return JSONResponse(content={"error": "Модель не загружена."}, status_code=500)
    response = responder.generate_response(message)
    return {"response": response}
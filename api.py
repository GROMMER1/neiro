from fastapi import FastAPI

app = FastAPI()


from fastapi.responses import JSONResponse
from image_generator import generate_image_from_text
from info_search import fetch_best_info_from_sources

@app.post("/generate-image")
def generate_image(payload: dict):
    prompt = payload.get("prompt", "")
    image_data = generate_image_from_text(prompt)
    return JSONResponse(content={"image_base64": image_data})

@app.post("/generate-text")
def generate_text_full(payload: dict):
    prompt = payload.get("prompt", "")
    info = fetch_best_info_from_sources(prompt)
    try:
        from generator import generate_text
        text = generate_text(prompt)
    except:
        text = f"(Заглушка) Ответ на '{prompt}'"
    return JSONResponse(content={"response": f"{info}\n\n{text}"})


import os
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image, ImageOps
from io import BytesIO
import base64

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    filename = os.path.join(UPLOAD_DIR, file.filename)

    with open(filename, "wb") as f:
        f.write(contents)

    # Простейшая "обработка" изображения (инверсия цвета)
    image = Image.open(BytesIO(contents)).convert("RGB")
    processed = ImageOps.invert(image)
    buffer = BytesIO()
    processed.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return JSONResponse(content={"filename": file.filename, "processed_image_base64": img_str})



chat_history = []

@app.post("/generate-text")
async def generate_text(prompt: dict):
    user_input = prompt.get("prompt")
    
    # Добавляем в историю для псевдообучения
    chat_history.append(user_input)

    # Заглушка: эхо с "поиском"
    simulated_search_info = f"[Поиск по теме '{user_input}']: Найдено подходящее определение."
    generated_response = f"{simulated_search_info}\nОтвет нейросети: Это интересный вопрос — {user_input[::-1]}."

    # Обучение: имитация сохранения новых данных
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"{user_input}\n")

    return {"response": generated_response}



@app.post("/generate-article")
async def generate_article(prompt: dict):
    topic = prompt.get("prompt")
    article = f"Статья по теме '{topic}':\n\n{topic.upper()} — это важная и интересная тема, требующая глубокого изучения..."
    return {"response": article}

@app.post("/generate-code")
async def generate_code(prompt: dict):
    task = prompt.get("prompt")
    example_code = f"# Пример кода на Python по задаче '{task}'\ndef example():\n    print('Задача: {task}')"
    return {"response": example_code}

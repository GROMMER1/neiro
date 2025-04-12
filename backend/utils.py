import os
import shutil
from typing import IO

def save_uploaded_file(uploaded_file: IO, destination: str):
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(uploaded_file, buffer)

def extract_text_from_file(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return "❗ Только .txt файлы поддерживаются в текущей версии."
import json
from datetime import datetime

def save_interaction(text, response, file="backend/training/dialogs.json"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []

    data.append({"text": f"Пользователь: {text}"})
    data.append({"text": f"Бот: {response}"})

    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
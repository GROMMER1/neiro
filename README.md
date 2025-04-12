# 🧠 Neural Chat — Лёгкая и самообучающаяся нейросеть

## 🚀 Особенности
- Семантический поиск по базе знаний
- Самообучение через загрузку PDF/DOCX/TXT файлов
- Использует лёгкую модель `MiniLM` (Sentence Transformers)
- Работает на Free Render без превышения лимита памяти

## ⚙️ Установка

### Через Render:
1. Загрузите проект на GitHub
2. Создайте новый Web Service на [render.com](https://render.com/)
3. Укажите команду запуска:

```
uvicorn backend.app:app --host 0.0.0.0 --port 10000
```

## 📦 API Эндпоинты
- `POST /api/chat` — общение с нейросетью
- `POST /api/upload` — загрузка текстов/документов
- `POST /api/train` — переобучение модели
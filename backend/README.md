# 🤖 Neural Chat Ultimate

Интеллектуальный нейросетевой ассистент с автообучением, расширенным вводом и современным интерфейсом.

## 🚀 Возможности

- 🧠 **Мультиязычное обучение** из `.txt`, `.json`, `.pdf`, `.docx`
- 📥 Загрузка документов через веб-интерфейс
- 🤖 Подключение источников знаний (Wikipedia, Google snippets)
- 💡 Автоматическое самообучение на диалогах
- 🔁 Обнаружение новых документов и автообучение
- 📊 Web-панель управления (загрузка, запуск, лог обучения)

## 🖥 Интерфейс

На React (с Tailwind UI). Включает:
- Загрузку документов
- Кнопку запуска обучения
- Просмотр логов

## 🧾 API

Работает на FastAPI:

- `POST /api/upload` — Загрузка PDF или DOCX
- `POST /api/train` — Запуск обучения (документы → текст → дообучение)

## 📦 Запуск локально

```bash
git clone <репозиторий>
cd neural_chat_ultimate

# Установка зависимостей
pip install -r backend/training/requirements_training.txt
pip install -r backend/api/requirements.txt

# Запуск API
uvicorn backend.api.main:app --reload

# Запуск интерфейса (из директории frontend)
npm install && npm run dev
```

## ☁️ Деплой на Render

1. Подключи GitHub-репозиторий
2. Создай Web Service для FastAPI (`backend/api/main.py`)
3. Добавь Build Command:
   ```bash
   pip install -r backend/training/requirements_training.txt
   pip install -r backend/api/requirements.txt
   ```
4. Start Command:
   ```bash
   uvicorn backend.api.main:app --host 0.0.0.0 --port 10000
   ```

---

MIT License | Made with ❤️ by AI
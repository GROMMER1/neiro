
# 🧠 Neural Chat API

FastAPI-сервер с тремя нейросетевыми моделями:
- Классификация числовых векторов
- Генерация текста
- Классификация изображений

## 📦 Установка

```bash
git clone https://github.com/yourname/neural-chat-api.git
cd neural-chat-api
pip install -r requirements.txt
```

## 🛠 Обучение моделей

```bash
bash train_models.sh
```

Создаст файлы:
- `classifier.pth`
- `text_generator.pth`
- `cnn.pth`

## 🚀 Запуск сервера

```bash
bash run_server.sh
```

Доступен по адресу: `http://localhost:8000`

## 🔌 API Эндпоинты

### POST `/classify-vector`
Классификация числового вектора (список из 10 float)

```json
[0.1, 0.5, 0.3, ..., 0.9]
```

---

### POST `/classify-image`
Загрузка изображения (`multipart/form-data`)  
Классифицирует изображение 32x32

---

### POST `/generate-text`
```json
{
  "prompt": "Once upon a time"
}
```

Возвращает сгенерированный текст *(заглушка)*

## 📄 Структура проекта

```
.
├── train.py
├── run_server.sh
├── train_models.sh
├── models/
├── utils/
├── server/
└── requirements.txt
```

## ☁️ Деплой на Render

Добавь `render.yaml` и запусти:

```yaml
services:
  - type: web
    name: neural-chat-api
    env: python
    buildCommand: "./train_models.sh"
    startCommand: "./run_server.sh"
```

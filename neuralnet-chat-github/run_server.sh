#!/bin/bash
echo "Запуск API-сервера..."
uvicorn server.api:app --host 0.0.0.0 --port 8000 --reload

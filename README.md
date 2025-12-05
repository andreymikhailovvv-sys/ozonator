# Ozon Unit Economics Bot

## Установка:
pip install -r requirements.txt

## Переменные окружения:
BOTFUZZER_TOKEN=
OZON_CLIENT_ID=
OZON_API_KEY=

## Запуск локально:
python app.py

## Деплой на Render:
Build command: pip install -r requirements.txt
Start command: gunicorn app:app

Webhook URL:
https://your-render-instance.
onrender.com/webhook

# Ozon Unit Economics Bot

## Установка
pip install -r requirements.txt

## Переменные окружения
TELEGRAM_TOKEN=
OZON_CLIENT_ID=
OZON_API_KEY=

## Локальный запуск
python app.py

## Старт на Render
Build command: pip install -r requirements.txt
Start command: gunicorn app:app

Webhook URL:
https://your-render-instance.onrender.com/webhook

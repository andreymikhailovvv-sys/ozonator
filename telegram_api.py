import requests
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN")
BASE = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{BASE}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })


def send_keyboard(chat_id, text, keyboard):
    requests.post(f"{BASE}/sendMessage", json={
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "inline_keyboard": keyboard
        }
    })

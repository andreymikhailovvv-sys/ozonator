import os
import requests

BOTFUZZER_TOKEN = os.getenv("BOTFUZZER_TOKEN")


def send_message(chat_id, text):
    url = "https://api.botfuzzer.com/send"
    payload = {
        "token": BOTFUZZER_TOKEN,
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

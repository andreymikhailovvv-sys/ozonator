from flask import Flask, request
from botfuzzer_api import send_message
from ozon_api import get_product_data
from calculator import calculate_unit_economy
import os

app = Flask(__name__)

# Для Render: порт задаётся переменной окружения PORT.
PORT = int(os.environ.get("PORT", 10000))

@app.route("/", methods=["GET"])
def root():
    return "OK", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "Webhook OK", 200

    data = request.json or {}

    # BotFuzzer форматирует данные так:
    payload = data.get("data", data)

    chat_id = payload.get("chat_id")
    text = (payload.get("text") or "").strip()

    print("Incoming webhook:", payload, flush=True)

    if not chat_id:
        return "no chat_id", 200

    if not text:
        send_message(chat_id, "Введите SKU товара.")
        return "ok", 200

    try:
        product = get_product_data(text)
        result = calculate_unit_economy(product)
        send_message(chat_id, result)
    except Exception as e:
        print("Error:", e, flush=True)
        send_message(chat_id, f"Ошибка: {e}")

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

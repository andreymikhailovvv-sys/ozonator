from flask import Flask, request
from telegram_api import send_message
from ozon_api import get_product_data
from calculator import calculate_unit_economy
import os

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 10000))

@app.before_request
def log_req():
    print(f"REQ: {request.method} {request.path}", flush=True)
    try:
        print("BODY:", request.get_data(as_text=True), flush=True)
    except:
        pass

# Корневая проверка
@app.route("/", methods=["GET"])
def root():
    return "OK", 200

# ВОТ ЗДЕСЬ ВАЖНОЕ — webhook принимает GET и POST
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # Telegram делает GET при установке вебхука
    if request.method == "GET":
        return "Webhook OK", 200

    # Telegram присылает JSON с update
    update = request.json or {}
    print("UPDATE:", update, flush=True)

    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")

    if not chat_id or not text:
        return "no chat or text", 200

    sku = text.strip()

    try:
        product = get_product_data(sku)
        result = calculate_unit_economy(product)
        send_message(chat_id, result)
    except Exception as e:
        send_message(chat_id, f"Ошибка обработки SKU: {e}")

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

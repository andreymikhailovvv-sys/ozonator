from flask import Flask, request
from botfuzzer_api import send_message
from ozon_api import get_product_data
from calculator import calculate_unit_economy
import os

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 10000))

@app.before_request
def log_request():
    # Логируем все входящие запросы для отладки
    print(f"REQUEST: {request.method} {request.path}", flush=True)
    try:
        print("BODY:", request.get_data(as_text=True), flush=True)
    except Exception:
        pass

@app.route("/", methods=["GET"])
def root():
    return "OK", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Проверка доступности вебхука (BotFuzzer / браузер)
        return "Webhook OK", 200

    data = request.json or {}
    payload = data.get("data", data)  # на случай формата {"data": {...}}

    chat_id = payload.get("chat_id")
    text = (payload.get("text") or "").strip()

    if not chat_id:
        print("NO CHAT_ID IN PAYLOAD", flush=True)
        return "no chat_id", 200

    if not text:
        send_message(chat_id, "Введите SKU товара.")
        return "ok", 200

    try:
        product = get_product_data(text)
        result = calculate_unit_economy(product)
        send_message(chat_id, result)
    except Exception as e:
        print("ERROR IN HANDLER:", e, flush=True)
        send_message(chat_id, f"Ошибка при расчете: {e}")

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

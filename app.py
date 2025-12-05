from flask import Flask, request
from botfuzzer_api import send_message
from ozon_api import get_product_data
from calculator import calculate_unit_economy

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data.get("chat_id")
    text = data.get("text", "").strip()

    if not text:
        send_message(chat_id, "Введите SKU или offer_id товара.")
        return "ok", 200

    try:
        product = get_product_data(text)
        result = calculate_unit_economy(product)
        send_message(chat_id, result)
    except Exception as e:
        send_message(chat_id, f"Ошибка: {str(e)}")

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

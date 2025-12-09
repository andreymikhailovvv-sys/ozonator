print("APP VERSION: 9", flush=True)

from flask import Flask, request
from telegram_api import send_message, send_keyboard
from ozon_api import list_products, get_product_info
from calculator import calculate_unit_economy
import os

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 10000))


@app.before_request
def log_req():
    print(f"REQ: {request.method} {request.path}", flush=True)
    try:
        print("BODY:", request.get_data(as_text=True), flush=True)
    except Exception as exc:
        print("BODY READ ERROR:", exc, flush=True)


@app.route("/", methods=["GET"])
def root():
    return "OK", 200


@app.route("/webhook", methods=["GET", "POST", "HEAD"])
def webhook():
    if request.method == "HEAD":
        return "", 200

    if request.method == "GET":
        return "Webhook OK", 200

    update = request.json or {}
    print("UPDATE:", update, flush=True)

    # Callback buttons
    if "callback_query" in update:
        cb = update["callback_query"]
        chat_id = cb["message"]["chat"]["id"]
        data = cb["data"]

        if data.startswith("page_"):
            page = int(data.split("_")[1])
            show_products_page(chat_id, page)
            return "OK", 200

        if data.startswith("prod_"):
            pid = int(data.split("_")[1])
            info_resp = get_product_info(pid) or {}
            if info_resp.get("error"):
                send_message(chat_id, f"Ошибка при запросе товара: {info_resp.get('error')}")
                return "OK", 200

            info = info_resp.get("result") or {}
            if not info:
                send_message(chat_id, "Не удалось получить информацию о товаре. Проверьте API ключи и наличие товара.")
                return "OK", 200

            result = calculate_unit_economy(info)
            send_message(chat_id, result)
            return "OK", 200

        return "OK", 200

    # Plain messages (/products)
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    if text == "/products":
        show_products_page(chat_id, 1)
        return "OK", 200

    return "OK", 200


def show_products_page(chat_id, page):
    page_size = 10
    data = list_products(page, page_size) or {}

    if data.get("error"):
        send_message(chat_id, f"Ошибка при запросе списка товаров: {data.get('error')}")
        return

    result = data.get("result") or {}
    items = result.get("items") or []

    if not items:
        send_message(chat_id, "Не удалось получить список товаров. Убедитесь, что API ключи заданы и в кабинете есть товары.")
        return

    buttons = []
    for item in items:
        title = item.get("name") or f"Товар {item.get('product_id')}"
        pid = item.get("product_id")
        if pid is None:
            continue
        buttons.append({"text": title, "callback_data": f"prod_{pid}"})

    if not buttons:
        send_message(chat_id, "Не удалось построить список кнопок для товаров.")
        return

    nav = []
    if page > 1:
        nav.append({"text": "← Назад", "callback_data": f"page_{page - 1}"})
    if len(items) == page_size:
        nav.append({"text": "Вперед →", "callback_data": f"page_{page + 1}"})

    keyboard = [buttons[i:i + 1] for i in range(len(buttons))]
    if nav:
        keyboard.append(nav)

    send_keyboard(chat_id, "Выберите товар:", keyboard)

print("APP VERSION: 7", flush=True)
from flask import Flask, request
from telegram_api import send_message, send_keyboard
from ozon_api import list_products, get_product_info
from calculator import calculate_unit_economy
import os, json

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 10000))

@app.before_request
def log_req():
    print(f"REQ: {request.method} {request.path}", flush=True)
    try:
        print("BODY:", request.get_data(as_text=True), flush=True)
    except:
        pass


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

    # CALLBACK QUERY (кнопка нажата)
    if "callback_query" in update:
        cb = update["callback_query"]
        chat_id = cb["message"]["chat"]["id"]
        data = cb["data"]

        # страница перелистывания
        if data.startswith("page_"):
            page = int(data.split("_")[1])
            show_products_page(chat_id, page)
            return "OK", 200

        # выбор товара
        if data.startswith("prod_"):
            pid = int(data.split("_")[1])
            info = get_product_info(pid)
            result = calculate_unit_economy(info)
            send_message(chat_id, result)
            return "OK", 200

        return "OK", 200


    # обычное сообщение (например /products)
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    if text == "/products":
        show_products_page(chat_id, 1)
        return "OK", 200

    return "OK", 200



def show_products_page(chat_id, page):
    page_size = 10
    data = list_products(page, page_size)

    items = data.get("items", [])
    if not items:
        send_message(chat_id, "Товары не найдены.")
        return

    # формируем кнопки
    buttons = []
    for item in items:
        title = item.get("name", f"Товар {item.get('product_id')}")
        pid = item.get("product_id")
        buttons.append({"text": title, "callback_data": f"prod_{pid}"})

    # кнопки навигации
    nav = []
    if page > 1:
        nav.append({"text": "⬅️ Назад", "callback_data": f"page_{page - 1}"})
    if len(items) == page_size:
        nav.append({"text": "Вперед ➡️", "callback_data": f"page_{page + 1}"})

    keyboard = [buttons[i:i+1] for i in range(len(buttons))]
    if nav:
        keyboard.append(nav)

    send_keyboard(chat_id, "Выбери товар:", keyboard)

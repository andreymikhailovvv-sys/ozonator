import os
import requests

OZON_CLIENT_ID = os.getenv("OZON_CLIENT_ID")
OZON_API_KEY = os.getenv("OZON_API_KEY")


def get_product_data(offer_id):
    headers = {
        "Client-Id": OZON_CLIENT_ID,
        "Api-Key": OZON_API_KEY
    }

    url = "https://api-seller.ozon.ru/v2/product/info"
    payload = {"offer_id": offer_id}

    r = requests.post(url, json=payload, headers=headers)
    data = r.json()
    result = data.get("result", {})
    price_block = result.get("price", {})

    return {
        "name": result.get("name", "Неизвестный товар"),
        "price": float(price_block.get("price", 0)),
        "commission_rate": float(result.get("commission", 0.15)),
        "logistics": float(result.get("logistics", 0)),
        "storage": float(result.get("storage", 0)),
        "buy_price": float(result.get("buy_price", 0))
    }

import requests
import os

API_URL = "https://api-seller.ozon.ru"
CLIENT_ID = os.environ.get("OZON_CLIENT_ID")
API_KEY = os.environ.get("OZON_API_KEY")

HEADERS = {
    "Client-Id": CLIENT_ID,
    "Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def list_products(page=1, page_size=10):
    url = f"{API_URL}/v1/product/list"
    payload = {"page": page, "page_size": page_size}

    r = requests.post(url, json=payload, headers=HEADERS)
    print("LIST RAW:", r.text, flush=True)
    return r.json()


def get_product_info(product_id):
    url = f"{API_URL}/v2/product/info"
    payload = {"product_id": product_id}

    r = requests.post(url, json=payload, headers=HEADERS)
    print("INFO RAW:", r.text, flush=True)
    return r.json()

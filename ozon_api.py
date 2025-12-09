import os
import requests

API_URL = "https://api-seller.ozon.ru"
CLIENT_ID = os.environ.get("OZON_CLIENT_ID")
API_KEY = os.environ.get("OZON_API_KEY")


def _have_creds():
    if CLIENT_ID and API_KEY:
        return True
    print("OZON credentials are missing: set OZON_CLIENT_ID and OZON_API_KEY", flush=True)
    return False


def _headers():
    return {
        "Client-Id": CLIENT_ID,
        "Api-Key": API_KEY,
        "Content-Type": "application/json",
    }


def list_products(page=1, page_size=10):
    if not _have_creds():
        return {"error": "missing_credentials"}

    url = f"{API_URL}/v2/product/list"
    payload = {
        "page": page,
        "page_size": page_size,
        "filter": {"visibility": "ALL"},
        "sort_dir": "ASC",
        "sort_by": "product_id",
    }

    try:
        r = requests.post(url, json=payload, headers=_headers(), timeout=15)
    except requests.RequestException as exc:
        print("LIST REQUEST ERROR:", exc, flush=True)
        return {"error": str(exc)}

    print("LIST RAW:", r.text, flush=True)

    if r.status_code != 200:
        return {"error": f"status {r.status_code}", "details": r.text}

    try:
        data = r.json()
    except ValueError:
        return {"error": "invalid_json", "details": r.text}

    if data.get("error"):
        print("LIST API ERROR:", data.get("error"), flush=True)

    return data


def get_product_info(product_id):
    if not _have_creds():
        return {"error": "missing_credentials"}

    url = f"{API_URL}/v2/product/info"
    payload = {"product_id": product_id}

    try:
        r = requests.post(url, json=payload, headers=_headers(), timeout=15)
    except requests.RequestException as exc:
        print("INFO REQUEST ERROR:", exc, flush=True)
        return {"error": str(exc)}

    print("INFO RAW:", r.text, flush=True)

    if r.status_code != 200:
        return {"error": f"status {r.status_code}", "details": r.text}

    try:
        data = r.json()
    except ValueError:
        return {"error": "invalid_json", "details": r.text}

    if data.get("error"):
        print("INFO API ERROR:", data.get("error"), flush=True)

    return data

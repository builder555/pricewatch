import random
import httpx
from .__agents import agents

SITE = "www.canadiantire.ca"


def extract_subscription_key(html):
    keyword = "apim-subscriptionkey&#34"
    key_location = html.find(keyword)
    key_start = html.find("&#34;", key_location + len(keyword)) + 5
    key_end = html.find("&#34;", key_start)
    return html[key_start:key_end]


def fetch_price_from_api(subscription_key: str, sku: str, client: httpx.Client):
    url = "https://apim.canadiantire.ca/v1/product/api/v1/product/sku/PriceAvailability?lang=en_CA&storeId=126&cache=true"
    headers = {
        "authority": "apim.canadiantire.ca",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en;q=0.8",
        "bannerid": "CTR",
        "basesiteid": "CTR",
        "browse-mode": "OFF",
        "content-type": "application/json",
        "ocp-apim-subscription-key": subscription_key,
        "origin": "https://www.canadiantire.ca",
        "referer": "https://www.canadiantire.ca/",
        "user-agent": random.choice(agents),
        "x-web-host": "www.canadiantire.ca",
    }
    data = {"skus": [{"code": sku, "lowStockThreshold": 0}]}
    r = client.post(url, headers=headers, json=data, timeout=10)
    resp = r.json()
    return resp["skus"][0]["currentPrice"]["value"]


def get_price(url: str, client: httpx.Client) -> float:
    r = client.get(url, headers={"user-agent": random.choice(agents)}, timeout=10)
    subscription_key = extract_subscription_key(r.text)
    sku = url.split(".")[-2]
    return fetch_price_from_api(subscription_key, sku, client)

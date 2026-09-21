import httpx
import re

SITE = "www.costco.ca"


def get_price(url: str, client: httpx.Client) -> float:
    r = client.get(url, timeout=15)
    matches = re.findall(r'"priceCurrency":"[A-Z]{3}","price":([0-9.]+)', r.text)
    if not matches:
        raise Exception("Price not found")
    return float(matches[0])

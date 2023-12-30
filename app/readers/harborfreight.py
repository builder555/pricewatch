import random
import httpx
from .__agents import agents

SITE = "www.harborfreight.com"


def get_price(url: str, client: httpx.Client) -> float:
    headers = {
        "User-Agent": random.choice(agents),
    }
    r = client.get(url, headers=headers, timeout=10)
    text = r.text
    price_area_start = text.find("priceCurrency")
    price_line_start = text.find("price", price_area_start + 2)
    price_value_start = text.find(":", price_line_start) + 1
    price_value_end = text.find(",", price_value_start)
    price_value = text[price_value_start:price_value_end].strip('"')
    return float(price_value)

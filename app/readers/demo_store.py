import random
import httpx
from .__agents import agents

SITE = "www.homedepot.com"


def get_price(url: str, client: httpx.Client) -> float:
    headers = {
        "User-Agent": random.choice(agents),
        "authority": "www.homedepot.com",
    }
    r = client.get(url, headers=headers, timeout=10)
    text = r.text
    price_group_start = text.find('"price"')
    price_group_end = text.find(",", price_group_start)
    price_value_start = text.find(":", price_group_start) + 1
    price_value = text[price_value_start:price_group_end]
    return float(price_value)

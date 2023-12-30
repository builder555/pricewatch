import random
import re
import httpx
from .__agents import agents

SITE = "www.bestbuy.ca"


def get_price(url: str, client: httpx.Client) -> float:
    agent = random.choice(agents)
    r = client.get(url, headers={"User-Agent": agent}, timeout=10)
    html = r.text
    pattern = r'"priceWithEhf":(\d+\.\d+)'
    matches = re.findall(pattern, html)
    price = matches[0]
    return float(price.strip().strip("$").strip())

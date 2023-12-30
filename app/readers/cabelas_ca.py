import random
import httpx
import re
from .__agents import agents

SITE = "www.cabelas.ca"


def get_price(url: str, client: httpx.Client) -> float:
    agent = random.choice(agents)
    r = client.get(url, headers={"User-Agent": agent}, timeout=10)
    html = r.text
    pattern = r"price: (\d+\.\d+)"
    matches = re.findall(pattern, html)
    price = matches[0]
    return float(price.strip().strip("$").strip())

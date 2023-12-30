import random
import httpx
import re
from .__agents import agents

SITE = "www.costco.com"


def get_price(url: str, client: httpx.Client) -> float:
    agent = random.choice(agents)
    r = client.get(url, headers={"user-agent": agent}, timeout=5)
    html = r.text
    pattern = r"priceMin: '(\d+\.\d+)'"
    matches = re.findall(pattern, html)
    price = matches[0]
    return float(price.strip().strip("$").strip())

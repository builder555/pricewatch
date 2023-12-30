import random
import re
import httpx
from .__agents import agents

SITE = "www.bestbuy.com"


cookie = "intl_splash=false; intl_splash=false; ltc=%20; blue-assist-banner-shown=true; dtSa=-"


def get_price(url: str, client: httpx.Client) -> float:
    agent = random.choice(agents)
    r = client.get(url, headers={"User-Agent": agent, "cookie": cookie}, timeout=10)
    html = r.text
    pattern = r'"price\\":(\d+\.\d+)'
    matches = re.findall(pattern, html)
    price = matches[0]
    return float(price.strip().strip("$").strip())

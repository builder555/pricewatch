import random
import httpx
from .__agents import agents
from bs4 import BeautifulSoup

SITE = "atlas-machinery.com"


def get_price(url: str, client: httpx.Client) -> float:
    agent = random.choice(agents)
    r = client.get(url, headers={"User-Agent": agent}, timeout=10)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    price_element = soup.find("meta", {"property": "product:price:amount"})
    if not price_element:
        raise Exception('Could not find meta with prop="product:price:amount"')
    price = price_element.get("content")
    return float(price.strip().strip())

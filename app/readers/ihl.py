import random
import httpx
from bs4 import BeautifulSoup
from .__agents import agents

SITE = "ihlcanada.com"


def get_price(url: str, client: httpx.Client) -> float:
    r = client.get(
        url,
        headers={"User-Agent": random.choice(agents)},
        timeout=10,
        follow_redirects=True,
    )
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("meta", property="product:price:amount")
    if tag:
        price = tag["content"]  # type: ignore
        return float(price.strip().strip("$").strip())  # type: ignore
    raise ValueError("Could not extract price")

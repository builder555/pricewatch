import random
import httpx
from bs4 import BeautifulSoup
from .__agents import agents

SITE = "www.petvalu.ca"


def get_price(url: str, client: httpx.Client) -> float:
    r = client.get(url, headers={"User-Agent": random.choice(agents)}, timeout=10)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    price = soup.find("span", {"class": "price"}).text
    return float(price.strip().strip("$").strip())

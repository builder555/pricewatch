import random
import httpx
import re
from .__agents import agents
import base64

SITE = "www.costco.ca"


def is_base64(s: str) -> bool:
    try:
        return base64.b64encode(base64.b64decode(s)) == s.encode("utf-8")
    except Exception:
        return False


def extract_using_pattern(html: str, pattern: str) -> float | None:
    matches = re.findall(pattern, html)
    if len(matches) == 0:
        return None
    if is_base64(matches[0]):
        matches[0] = base64.b64decode(matches[0]).decode("utf-8")
    return float(matches[0].strip().strip("$").strip())


def get_price(url: str, client: httpx.Client) -> float:
    agent = random.choice(agents)
    r = client.get(url, headers={"user-agent": agent}, timeout=5)
    html = r.text
    patterns = [
        r"priceMin: '(\d+\.\d+)'",
        r"price: (\d+\.\d+)",
        r"price: '([A-Za-z0-9+/=]+)'",
    ]
    for pattern in patterns:
        price = extract_using_pattern(html, pattern)
        if price is not None:
            return price
    raise Exception("Price not found")

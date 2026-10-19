import re
from urllib.parse import urlparse
import httpx

SITE = "www.bestbuy.ca"
OFFERS_API = "https://www.bestbuy.ca/api/offers/v1/products/{sku}/offers"
# akamai stalls chrome/firefox agents (tls fingerprint mismatch), safari passes
AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/18.6 Safari/605.1.15"
)


def get_price(url: str, client: httpx.Client) -> float:
    # product pages are blocked by bot protection, but the offers api is not
    match = re.search(r"/(\d+)/?$", urlparse(url).path)
    if not match:
        raise Exception("SKU not found in url")
    r = client.get(
        OFFERS_API.format(sku=match.group(1)),
        headers={"User-Agent": AGENT},
        timeout=10,
    )
    r.raise_for_status()
    offers = r.json()
    if not offers:
        raise Exception("Price not found")
    offer = next((o for o in offers if o.get("isWinner")), offers[0])
    return float(offer["salePrice"])

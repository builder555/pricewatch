from urllib.parse import urlparse
import random
import httpx
from bs4 import BeautifulSoup
from .__agents import agents

SITE = "www.homedepot.ca"


def try_to_extract_using_bs(text: str) -> float:
    # sometimes doesn't work, depending on what HTML is returned
    soup = BeautifulSoup(text, "html.parser")
    price_element = soup.find("span", {"itemprop": "price"})
    if not price_element:
        raise Exception('Could not find span with itemprop="price"')
    price = price_element.text
    return float(price.strip().strip("$").strip())


def try_to_extract_using_text_search(text: str) -> float:
    # may not be the most accurate, but seems to always work
    price_group_start = text.find("currencyIso")
    price_value_start = text.find("$", price_group_start) + 1
    price_value_end = price_value_start
    while text[price_value_end].isdigit() or text[price_value_end] == ".":
        price_value_end += 1
    price_value = text[price_value_start:price_value_end]
    return float(price_value)


def extract_product_id(url: str) -> str:
    parsed_url = urlparse(url)
    last_segment = parsed_url.path.split("/")[-1]
    return last_segment


def try_to_extract_json(url: str, client: httpx.Client) -> float:
    headers = {
        "accept": "application/json, text/javascript, */*",
        "user-agent": random.choice(agents),
        "referer": url,
    }
    store_id = 7174
    product_id = extract_product_id(url)
    json_url = f"https://www.homedepot.ca/api/productsvc/v1/products/{product_id}/store/{store_id}?fields=BASIC_SPA&lang=en"
    r = client.get(json_url, headers=headers, timeout=10)
    jsn = r.json()
    return jsn["optimizedPrice"]["displayPrice"]["value"]


def get_price(url: str, client: httpx.Client) -> float:
    headers = {
        "User-Agent": random.choice(agents),
        "authority": "www.homedepot.ca",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "dnt": "1",
        "sec-ch-ua": '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
    }
    r = client.get(url, headers=headers, timeout=10)

    price_extractors = (
        (try_to_extract_json, url, client),
        (try_to_extract_using_bs, r.text),
        (try_to_extract_using_text_search, r.text),
    )
    price = 0.0
    for extractor in price_extractors:
        get_price_function, *args = extractor
        try:
            price = get_price_function(*args)  # type: ignore
        except Exception:
            pass
        finally:
            pass
        if price > 0.0:
            return price
    raise ValueError("Could not extract price")

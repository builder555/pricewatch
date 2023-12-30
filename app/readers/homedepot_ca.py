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


def get_price(url: str, client: httpx.Client) -> float:
    headers = {
        "User-Agent": random.choice(agents),
        "authority": "www.homedepot.ca",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "dnt": "1",
        "sec-ch-ua": '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
    }
    r = client.get(url, headers=headers, timeout=10)
    try:
        return try_to_extract_using_bs(r.text)
    except:
        return try_to_extract_using_text_search(r.text)

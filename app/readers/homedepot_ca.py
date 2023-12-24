import random
import requests
from bs4 import BeautifulSoup

SITE = "www.homedepot.ca"

agents = [
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
]


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


def get_price(url: str) -> float:
    headers = {
        "User-Agent": random.choice(agents),
        "authority": "www.homedepot.ca",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "dnt": "1",
        "sec-ch-ua": '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
    }
    r = requests.get(url, headers=headers, timeout=10)
    try:
        return try_to_extract_using_bs(r.text)
    except:
        return try_to_extract_using_text_search(r.text)

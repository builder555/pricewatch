import re
import httpx
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

SITE = "www.petvalu.ca"

OFFER_PRICE = re.compile(r'"@type":"Offer".*?"price":\s*([0-9]+(?:\.[0-9]+)?)')


def extract_price(html: str) -> float | None:
    normalized = html.replace('\\"', '"')
    match = OFFER_PRICE.search(normalized)
    if match is None:
        return None
    return float(match.group(1))


def get_price(url: str, client: httpx.Client) -> float:
    ops = Options()
    ops.add_argument("--headless")
    ops.binary_location = "/usr/bin/firefox-esr"
    dr = webdriver.Firefox(options=ops)
    price = None
    try:
        attempts = 10
        dr.get(url)
        while attempts > 0:
            price = extract_price(dr.page_source)
            if price is not None:
                break
            sleep(1)
            attempts -= 1
    finally:
        dr.quit()
    if price is None:
        raise Exception("Price not found")
    return price

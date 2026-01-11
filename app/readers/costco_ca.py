import httpx
import re
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep

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
    ops = Options()
    ops.add_argument("--headless")
    ops.binary_location = '/usr/bin/firefox-esr'
    dr = webdriver.Firefox(options=ops)
    price = None
    try:
        attempts = 10
        dr.get(url)
        while attempts > 0:
            try:
                el = dr.find_element(By.XPATH, "//*[@automation-id='productPriceOutput']")
                price = float(el.text.replace("$", ""))
                break
            except Exception:
                sleep(1)
                attempts -= 1
    finally:
        dr.quit()
    if price is None:
        raise Exception("Price not found")
    return price

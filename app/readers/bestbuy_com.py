import random
import requests
import re

SITE = 'www.bestbuy.com'

agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    ]

cookie = 'intl_splash=false; intl_splash=false; ltc=%20; blue-assist-banner-shown=true; dtSa=-'

def get_price(url: str) -> float:
    agent = random.choice(agents)
    r = requests.get(url, headers={'User-Agent': agent, 'cookie': cookie }, timeout=10)
    html = r.text
    pattern = r'"price\\":(\d+\.\d+)'
    matches = re.findall(pattern, html)
    price = matches[0]
    return float(price.strip().strip('$').strip())

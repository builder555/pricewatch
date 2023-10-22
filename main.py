from dataclasses import dataclass, asdict
import json
import os
from time import sleep
from datetime import datetime

from readers import demo_store
from notifiers import demo_notifier

def notify(msg: str):
    demo_notifier.notify(msg, 'test@example.com')

def get_price_extractor(site: str):
    readers = {
        demo_store.SITE: demo_store.get_price,
    }
    return readers[site]

@dataclass
class Item:
    name: str
    url: str
    last_price: float
    always_notify: bool
    def __dict__(self):
        return asdict(self)

def get_price(item: Item) -> float:
    kind = item.url.split('/')[2]
    extract_price = get_price_extractor(kind)
    return extract_price(item.url)

def get_items() -> list[Item]:
    items = []
    if not os.path.exists('items.json'):
        return []
    with open('items.json', 'r') as f:
        items = json.load(f)
    return [Item(**item) for item in items]

def save_items(items: list[Item]):
    with open('items.json', 'w+') as f:
        json.dump([item.__dict__() for item in items], f)

def main():
    items = get_items()
    for item in items:
        current_time = datetime.now()
        print(f'[{current_time}] Checking {item.name}...', end='')
        try:
            price = get_price(item)
        except:
            print('Error')
            continue
        print(f'${price}')
        sleep(2)
        if price != item.last_price:
            print('Price has changed!')
            notify(f'Price has changed for {item.name} from ${item.last_price} to ${price}. Check it out: {item.url}')
            item.last_price = price
        elif item.always_notify:
            notify(f'Price has not changed for {item.name}: ${price}')
    save_items(items)

if __name__ == '__main__':
    main()

from dataclasses import dataclass, asdict
import json
import os
from time import sleep
from datetime import datetime
import asyncio
from pathlib import Path
import importlib

from notifiers import telegram_notifier

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

class Modules:
    def __init__(self):
        self.modules = []
        module_files = Path('./readers').rglob('*.py')
        for module_file in module_files:
            module_name = module_file.stem
            module = importlib.import_module(f'readers.{module_name}')
            if hasattr(module, 'SITE'):
                self.modules.append(module)
    def __getitem__(self, key):
        for m in self.modules:
            if m.SITE in key:
                return m

async def notify(msg: str):
    await telegram_notifier.notify(msg)

def get_price_extractor(site: str):
    module = Modules()[site]
    if module is None:
        raise KeyError(f"No reader found for site '{site}'")
    return module.get_price

@dataclass
class Item:
    name: str
    url: str
    last_price: float
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

async def main():
    items = get_items()
    for item in items:
        current_time = datetime.now()
        print(f'[{current_time}] Checking {item.name}...', end='')
        retries = 10
        while retries > 0:
            try:
                price = get_price(item)
                break
            except KeyboardInterrupt:
                return
            except Exception:
                retries -= 1
        else:
            print('error')
            continue
        print(f'${price}')
        sleep(2)
        if price != item.last_price:
            print('Price has changed!')
            await notify(f'Price has changed for {item.name} from ${item.last_price} to ${price}. Check it out: {item.url}')
            item.last_price = price
    save_items(items)

if __name__ == '__main__':
    asyncio.run(main())

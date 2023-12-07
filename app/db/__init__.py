import os
import json
from dataclasses import dataclass, asdict

db_path = os.path.join(os.path.dirname(__file__), 'items.json')

@dataclass
class Item:
    name: str
    url: str
    last_price: float
    @property
    def __dict__(self):
        return asdict(self)
class ItemJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__dict__'):
            return o.__dict__
        return super().default(o)

def get_items() -> list[Item]:
    items = []
    if not os.path.exists(db_path):
        return []
    with open(db_path, 'r') as f:
        items = json.load(f)
    return [Item(**item) for item in items]

def save_items(items: list[Item]):
    with open(db_path, 'w+') as f:
        json.dump([item.__dict__ for item in items], f)

def delete_item(index: int):
    items = get_items()
    del items[index]
    save_items(items)

def add_item(item: Item):
    items = get_items()
    items.append(item)
    save_items(items)

def update_item(index: int, item: Item):
    items = get_items()
    items[index] = item
    save_items(items)

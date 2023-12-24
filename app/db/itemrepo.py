import os
import json
from .dataclasses import Item


class ItemRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_items_json(self) -> list[dict]:
        if not os.path.exists(self.db_path):
            return []
        with open(self.db_path, "r") as f:
            return json.load(f)

    def get_items(self) -> list[Item]:
        items = self.get_items_json()
        return [Item(**item) for item in items]

    def save_items(self, items: list[Item]):
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))
        with open(self.db_path, "w+") as f:
            json.dump([item.__dict__ for item in items], f)

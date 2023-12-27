import os
import json
from .dataclasses import Item


def is_data_old_format(data: list[dict]) -> bool:
    return len(data) > 0 and "prices" not in data[0]


def update_data_to_new_format(data: list[dict]) -> list[dict]:
    return [Item(**item).__dict__ for item in data]


class ItemRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_items_json(self) -> list[dict]:
        items = self.get_items()
        return [item.__dict__ for item in items]

    def get_items(self) -> list[Item]:
        if not os.path.exists(self.db_path):
            return []
        with open(self.db_path, "r") as f:
            items = json.load(f)
            return [Item(**item) for item in items]

    def save_items(self, items: list[Item]):
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))
        with open(self.db_path, "w+") as f:
            json.dump([item.__dict__ for item in items], f)

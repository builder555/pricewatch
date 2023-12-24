import copy
from .itemrepo import ItemRepository
from .dataclasses import Item


class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def get_items(self) -> list[Item]:
        return copy.deepcopy(self.repository.get_items())

    def add_item(self, item: Item):
        if not isinstance(item, Item):
            raise TypeError("item must be an instance of Item")
        items = self.get_items()
        items.append(item)
        self.repository.save_items(items)

    def delete_item(self, index: int):
        items = self.get_items()
        del items[index]
        self.repository.save_items(items)

    def update_item(self, index: int, item: Item):
        if not isinstance(item, Item):
            raise TypeError("item must be an instance of Item")
        items = self.get_items()
        items[index] = item
        self.repository.save_items(items)

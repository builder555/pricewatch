import os
from .dataclasses import Item
from .itemrepo import ItemRepository
from .itemservice import ItemService

db_path = os.path.join(os.path.dirname(__file__), "data/items.json")
item_repo = ItemRepository(db_path)
item_service = ItemService(item_repo)

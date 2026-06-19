import json
from datetime import datetime
from unittest.mock import mock_open, patch

import pytest

from .itemrepo import ItemRepository
from .dataclasses import Item


@pytest.fixture
def sample_items():
    return [{"name": "Item1", "url": "http://item1.com", "prices": []}]


def test_get_items_when_db_is_empty_returns_blank_list(tmp_path):
    repo = ItemRepository(str(tmp_path / "items.db"))
    items = repo.get_items()
    assert items == []


def test_save_items_and_get_items(sample_items, tmp_path):
    items = [Item(**item) for item in sample_items]
    repo = ItemRepository(str(tmp_path / "items.db"))
    repo.save_items(items)
    fetched_items = repo.get_items()
    assert len(fetched_items) == 1
    assert fetched_items[0].name == "Item1"


def test_can_get_items_as_json(sample_items, tmp_path):
    items = [Item(**item) for item in sample_items]
    repo = ItemRepository(str(tmp_path / "items.db"))
    repo.save_items(items)
    assert repo.get_items_json() == sample_items


def test_create_dir_if_not_exists(tmp_path):
    db_path = tmp_path / "data" / "items.db"
    repo = ItemRepository(str(db_path))
    repo.save_items([])
    assert (tmp_path / "data").exists()


def test_migrate_legacy_json(sample_items, tmp_path):
    legacy_path = tmp_path / "items.json"
    legacy_path.write_text(json.dumps(sample_items))
    repo = ItemRepository(str(tmp_path / "items.db"), legacy_json_path=str(legacy_path))
    items = repo.get_items_json()
    assert items == sample_items


def test_can_get_price_history():
    prices = [("2021-10-15T13:00:12", 10.0), ("2021-10-15T14:00:12", 15.0)]
    item = Item(name="item1", url="http://example.com", prices=prices)
    assert item.prices == prices


def test_setting_price_adds_it_to_history():
    item = Item(name="item1", url="http://example.com")
    with patch("app.db.dataclasses.datetime") as mock_datetime:
        assert item.prices == []
        mock_datetime.now.return_value = datetime(2021, 10, 15, 13, 0, 19)
        item.price = 10.0
        mock_datetime.now.return_value = datetime(2021, 10, 15, 15, 0, 19)
        item.price = 8.99
        assert item.prices == [
            ("2021-10-15T13:00:19Z", 10.0),
            ("2021-10-15T15:00:19Z", 8.99),
        ]


def test_can_get_current_price_for_item():
    prices = [("2021-10-15T13:00:12Z", 10.0), ("2021-10-15T14:00:12Z", 15.0)]
    item = Item(name="item1", url="http://example.com", prices=prices)
    assert item.price == 15.0

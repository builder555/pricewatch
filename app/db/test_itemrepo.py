import json
import pytest
from datetime import datetime
from unittest.mock import mock_open, patch
from .itemrepo import ItemRepository
from .dataclasses import Item


@pytest.fixture
def sample_items():
    return [{"name": "Item1", "url": "http://item1.com", "prices": []}]


def test_get_items_when_file_exists(sample_items):
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_items))), patch(
        "os.path.exists", return_value=True
    ):
        repo = ItemRepository("dummy_path")
        items = repo.get_items()
        assert len(items) == 1
        assert items[0].name == "Item1"


def test_save_items(sample_items):
    items = [Item(**item) for item in sample_items]
    m = mock_open()
    with patch("builtins.open", m), patch("os.path.exists", return_value=True):
        repo = ItemRepository("dummy_path")
        repo.save_items(items)
        m.assert_called_once_with("dummy_path", "w+")
        written_data = "".join(args[0] for args, _ in m().write.call_args_list)
        assert written_data == json.dumps(sample_items)


def test_can_get_items_as_json(sample_items):
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_items))), patch(
        "os.path.exists", return_value=True
    ):
        repo = ItemRepository("dummy_path")
        assert repo.get_items_json() == sample_items


def test_get_items_when_file_does_not_exist_returns_blank_list():
    with patch("os.path.exists", return_value=False):
        repo = ItemRepository("dummy_path")
        items = repo.get_items()
        assert items == []


def test_create_dir_if_not_exists():
    with patch("os.path.exists", return_value=False), patch("os.makedirs") as m, patch(
        "builtins.open"
    ):
        repo = ItemRepository("data/dummy_path")
        repo.save_items([])
        m.assert_called_once_with("data")


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

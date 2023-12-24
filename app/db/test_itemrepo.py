import json
from unittest.mock import mock_open, patch
from .itemrepo import ItemRepository
from .dataclasses import Item


def test_get_items_when_file_exists():
    sample_data = [{"name": "Item1", "url": "http://item1.com", "last_price": 10.0}]
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_data))), patch(
        "os.path.exists", return_value=True
    ):
        repo = ItemRepository("dummy_path")
        items = repo.get_items()

        assert len(items) == 1
        assert items[0].name == "Item1"


def test_get_items_when_file_does_not_exist_returns_blank_list():
    with patch("os.path.exists", return_value=False):
        repo = ItemRepository("dummy_path")
        items = repo.get_items()
        assert items == []


def test_save_items():
    expected_items = [{"name": "Item1", "url": "http://item1.com", "last_price": 10.0}]
    items = [Item(**item) for item in expected_items]
    m = mock_open()
    with patch("builtins.open", m), patch("os.path.exists", return_value=True):
        repo = ItemRepository("dummy_path")
        repo.save_items(items)

    m.assert_called_once_with("dummy_path", "w+")
    written_data = "".join(args[0] for args, _ in m().write.call_args_list)
    assert written_data == json.dumps(expected_items)


def test_can_get_items_as_json():
    sample_data = [{"name": "Item1", "url": "http://item1.com", "last_price": 10.0}]
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_data))), patch(
        "os.path.exists", return_value=True
    ):
        repo = ItemRepository("dummy_path")
        assert repo.get_items_json() == sample_data

def test_create_dir_if_not_exists():
    with patch("os.path.exists", return_value=False), patch("os.makedirs") as m, patch("builtins.open"):
        repo = ItemRepository("data/dummy_path")
        repo.save_items([])
        m.assert_called_once_with("data")

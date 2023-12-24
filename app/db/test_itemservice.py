import pytest
from .itemservice import ItemService
from .dataclasses import Item


@pytest.fixture
def fake_items():
    return [
        {"name": "Item1", "url": "http://example.com", "last_price": 100.0},
        {"name": "Item2", "url": "http://example.org", "last_price": 200.0},
    ]


@pytest.fixture
def mock_repository(fake_items):
    class FakeRepo:
        def __init__(self):
            self.__items = [Item(**item) for item in fake_items]

        def get_items(self):
            return self.__items

        def save_items(self, items):
            self.__items = items

    return FakeRepo()


@pytest.fixture
def service(mock_repository):
    return ItemService(mock_repository)


def test_get_items(service, fake_items):
    items = service.get_items()
    assert len(items) == 2
    for i in range(len(items)):
        assert items[i].name == fake_items[i]["name"]
        assert items[i].url == fake_items[i]["url"]
        assert items[i].last_price == fake_items[i]["last_price"]


def test_add_item(service):
    items_before_insert = service.get_items()
    new_item = Item(name="Item3", url="http://example.net", last_price=300.0)
    service.add_item(new_item)
    items_after_insert = service.get_items()
    assert len(items_after_insert) == len(items_before_insert) + 1
    assert items_after_insert[-1] == new_item


def test_passing_wrong_type_raises_exception(service):
    with pytest.raises(TypeError):
        service.add_item("not an Item")  # type: ignore


def test_update_item(service):
    new_item = Item(name="Item123Random", url="http://example.net", last_price=300.0)
    service.update_item(0, new_item)
    items = service.get_items()
    assert items[0] == new_item


def test_delete_item(service):
    items_before_delete = service.get_items()
    service.delete_item(0)
    items_after_delete = service.get_items()
    assert len(items_after_delete) == len(items_before_delete) - 1
    assert items_after_delete[0] == items_before_delete[1]

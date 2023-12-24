from dataclasses import dataclass


@dataclass(repr=True)
class Item:
    name: str
    url: str
    last_price: float

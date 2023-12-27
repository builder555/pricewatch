from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from copy import deepcopy


@dataclass
class Item:
    name: str
    url: str
    prices: List[Tuple[str, float]] = field(default_factory=list)

    def __init__(
        self,
        name: str,
        url: str,
        prices: List[Tuple[str, float]] = [],
        last_price: Optional[float] = None,
    ):
        self.name = name
        self.url = url
        self.prices = deepcopy(prices)
        if last_price is not None and len(prices) == 0:
            self.price = last_price

    @property
    def price(self) -> float:
        return self.prices[-1][1] if self.prices else 0.0

    @price.setter
    def price(self, value: float):
        timestamp = datetime.now().replace(microsecond=0).isoformat()
        self.prices.append((timestamp, value))

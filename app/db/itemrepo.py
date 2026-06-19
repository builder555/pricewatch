import json
import os
import sqlite3
from .dataclasses import Item


def is_data_old_format(data: list[dict]) -> bool:
    return len(data) > 0 and "prices" not in data[0]


def update_data_to_new_format(data: list[dict]) -> list[dict]:
    normalized_items = []
    for item in data:
        item = dict(item)
        if "prices" not in item:
            if "price" in item and "last_price" not in item:
                item["last_price"] = item.pop("price")
        normalized_items.append(Item(**item).__dict__)
    return normalized_items


class ItemRepository:
    def __init__(self, db_path: str, legacy_json_path: str | None = None):
        self.db_path = db_path
        self.legacy_json_path = legacy_json_path
        self._init_db()
        self._maybe_migrate_legacy_json()

    def _ensure_db_dir(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        self._ensure_db_dir()
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    position INTEGER NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    ts TEXT NOT NULL,
                    price REAL NOT NULL,
                    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_prices_item_id ON prices(item_id)"
            )

    def _maybe_migrate_legacy_json(self):
        if not self.legacy_json_path or not os.path.exists(self.legacy_json_path):
            return
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS count FROM items").fetchone()
            if row and row["count"] > 0:
                return
        with open(self.legacy_json_path, "r") as f:
            data = json.load(f)
        if is_data_old_format(data):
            data = update_data_to_new_format(data)
        items = [Item(**item) for item in data]
        self.save_items(items)

    def get_items_json(self) -> list[dict]:
        items = self.get_items()
        return [item.__dict__ for item in items]

    def get_items(self) -> list[Item]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT i.id, i.name, i.url, p.ts, p.price
                FROM items i
                LEFT JOIN prices p ON p.item_id = i.id
                ORDER BY i.position ASC, p.id ASC
                """
            ).fetchall()
        if not rows:
            return []
        items_by_id: dict[int, Item] = {}
        order: list[int] = []
        for row in rows:
            item_id = int(row["id"])
            if item_id not in items_by_id:
                items_by_id[item_id] = Item(
                    name=row["name"], url=row["url"], prices=[]
                )
                order.append(item_id)
            if row["ts"] is not None:
                items_by_id[item_id].prices.append((row["ts"], row["price"]))
        return [items_by_id[item_id] for item_id in order]

    def save_items(self, items: list[Item]):
        self._ensure_db_dir()
        with self._connect() as conn:
            conn.execute("DELETE FROM prices")
            conn.execute("DELETE FROM items")
            for position, item in enumerate(items):
                cursor = conn.execute(
                    "INSERT INTO items (name, url, position) VALUES (?, ?, ?)",
                    (item.name, item.url, position),
                )
                item_id = cursor.lastrowid
                if item.prices:
                    conn.executemany(
                        "INSERT INTO prices (item_id, ts, price) VALUES (?, ?, ?)",
                        [
                            (item_id, timestamp, price)
                            for timestamp, price in item.prices
                        ],
                    )

import os
from time import sleep
from datetime import datetime
import asyncio
import httpx
from app.notifiers import telegram_notifier, demo_notifier
from app.db import item_service
from app.readers import get_item_price_with_retries

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


async def notify(msg: str):
    await telegram_notifier.notify(msg)


async def main():
    items = item_service.get_items()
    with httpx.Client() as client:
        for index, item in enumerate(items):
            current_time = datetime.now()
            print(f"[{current_time}] Checking {item.name}...", end="")
            try:
                price = get_item_price_with_retries(item.url, client=client)
            except KeyboardInterrupt:
                return
            except Exception:
                print("error")
                continue
            print(f"${price}")
            sleep(2)
            if price != item.price:
                print("Price has changed!")
                msg = (
                    f"Price has changed for {item.name} "
                    + f"from ${item.price} to ${price}. "
                    + f"Check it out: {item.url}"
                )
                await notify(msg)
                item.price = price
                item_service.update_item(index, item)


if __name__ == "__main__":
    asyncio.run(main())

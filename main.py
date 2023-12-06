import os
from time import sleep
from datetime import datetime
import asyncio
from app.notifiers import telegram_notifier
from app.db import get_items, save_items
from app.readers import get_item_price_with_retries

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

async def notify(msg: str):
    await telegram_notifier.notify(msg)


async def main():
    items = get_items()
    for item in items:
        current_time = datetime.now()
        print(f'[{current_time}] Checking {item.name}...', end='')
        try:
            price = get_item_price_with_retries(item.url)
        except KeyboardInterrupt:
            return
        except Exception:
            print('error')
            continue
        print(f'${price}')
        sleep(2)
        if price != item.last_price:
            print('Price has changed!')
            await notify(f'Price has changed for {item.name} from ${item.last_price} to ${price}. Check it out: {item.url}')
            item.last_price = price
    save_items(items)

if __name__ == '__main__':
    asyncio.run(main())

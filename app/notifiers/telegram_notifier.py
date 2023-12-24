from telegram import Bot
import os


async def notify(text: str):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise Exception("Must specify TELEGRAM_TOKEN and TELEGRAM_CHAT_ID")
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=text)

from telegram import Bot
import os

async def notify(text:str):
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    await bot.send_message(chat_id=chat_id, text=text)

from data.config import ADMINS
import logging


async def on_startup_notify():
    from loader import bot
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text="Bot ishga tushdi!")
        except Exception as err:
            logging.exception(err)

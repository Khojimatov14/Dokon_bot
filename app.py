import sys
import asyncio
import logging
import middlewares, filters, handlers
from middlewares import ThrottlingMiddleware
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from loader import dp, bot, users_db, categories_db, products_db, carts_db


async def main():
    await on_startup_notify()
    await set_default_commands()
    dp.update.middleware.register(ThrottlingMiddleware())

    try:
        users_db.create_table_users()
    except Exception as err:
        print(err)
    try:
        categories_db.create_table_categories()
    except Exception as err:
        print(err)
    try:
        products_db.create_table_products()
    except Exception as err:
        print(err)
    try:
        carts_db.create_table_cart()
    except Exception as err:
        print(err)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

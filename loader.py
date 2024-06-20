from data import config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from utils import DatabaseUsers, DatabaseCategories, DatabaseProducts, DatabaseCarts

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

users_db = DatabaseUsers(path_to_db="data/allData.db")
categories_db = DatabaseCategories(path_to_db="data/allData.db")
products_db = DatabaseProducts(path_to_db="data/allData.db")
carts_db = DatabaseCarts(path_to_db="data/allData.db")

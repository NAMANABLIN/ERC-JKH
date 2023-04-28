from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import JKH_TOKEN

storage=MemoryStorage()
bot = Bot(token=JKH_TOKEN)
dp = Dispatcher(bot, storage=storage)
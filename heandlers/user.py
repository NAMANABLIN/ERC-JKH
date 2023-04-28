from aiogram import Dispatcher
from aiogram.types import Message

from create_bot import dp


async def echo(msg: Message):
    print(msg.location)
    await msg.answer(msg.text)


def register_heandlers_client(dp: Dispatcher):
    dp.register_message_handler(echo)

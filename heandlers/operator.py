from aiogram import Dispatcher, types
from keyboards import kb_registration, remove
from create_bot import bot
from data.defs_orm import get_user

from fsm import FSMCommunication_with_the_operator


async def talk_to_operator(msg: types.Message):
    user = await get_user(msg.from_id)
    await bot.forward_message(user.operator, message_id=msg.message_id)


def operator_heandlers_client(dp: Dispatcher):
    dp.register_message_handler(talk_to_operator,
                                state=FSMCommunication_with_the_operator.talk)

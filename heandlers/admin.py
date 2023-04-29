from aiogram import Dispatcher, types, filters
from keyboards import remove, kb_menu, kb_menu_for_operator
from data.defs_orm import get_user
from sqlalchemy.exc import IntegrityError
from data.defs_orm import update_user


async def add_operator(msg: types.Message):
    user = await get_user(msg.from_id)
    if user.is_admin:
        operator_id = msg.text.split()[1]
        await update_user(operator_id, is_operator=True)
        await msg.answer('Пользователь назначен оператором!')


async def delete_operator(msg: types.Message):
    user = await get_user(msg.from_id)
    if user.is_admin:
        operator_id = msg.text.split()[1]
        await update_user(operator_id, is_operator=False)
        await msg.answer('Пользователь больше не оператор!')


async def show_id(msg: types.Message):
    await msg.answer(msg.from_id)


def menu_heandlers_client(dp: Dispatcher):
    dp.register_message_handler(add_operator, filters.Command('add_operator'))
    dp.register_message_handler(delete_operator, filters.Command('delete_operator'))
    dp.register_message_handler(show_id, commands=['show_me_id'])

from aiogram import Dispatcher, types
from keyboards import kb_registration, remove

async def change_address(msg: types.Message):
    await msg.answer(
        'Введите свой адрес, можете воспользоваться, кнопкой в меню:', reply_markup=kb_registration)

def menu_heandlers_client(dp: Dispatcher):
    dp.register_message_handler(change_address)

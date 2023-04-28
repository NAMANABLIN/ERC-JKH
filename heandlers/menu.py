from aiogram import Dispatcher, types,filters
from keyboards import kb_registration, remove, kb_menu

async def change_address(msg: types.Message):
    await msg.answer(
        'Введите свой адрес, можете воспользоваться, кнопкой в меню:', reply_markup=kb_registration)

async def show_menu(msg:types.Message):
    await msg.answer('Меню', reply_markup=kb_menu)

def menu_heandlers_client(dp: Dispatcher):
    dp.register_message_handler(change_address,filters.Text('Изменить адрес'))
    dp.register_message_handler(show_menu)

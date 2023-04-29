from aiogram import Dispatcher, types, filters
from keyboards import remove, kb_menu, kb_menu_for_operator
from data.defs_orm import get_user
from sqlalchemy.exc import IntegrityError


async def change_address(msg: types.Message):
    await msg.answer(
        'Введите свой адрес, в таком формате:\n'
         'Улица, номер дома, номер квартиры\n'
         'Пример: Артёма, 162, 10')


async def show_menu(msg: types.Message):
    try:
        user = await get_user(msg.from_id)
        if user.is_admin:
            await msg.answer('Меню:\n'
                             'Дополнительные команды:\n'
                             'Назначить кого-то оператором, введите "/add_operator <его айди>"\n'
                             'Убрать кого-то из операторов, введите "/delete_operator <его айди>"\n'
                             '(Вписывать без "" и без <>)', reply_markup=kb_menu_for_operator)
        elif user.is_operator:
            await msg.answer('Меню', reply_markup=kb_menu_for_operator)
        else:
            await msg.answer('Меню', reply_markup=kb_menu)
    except IntegrityError:
        await msg.answer('Вы ещё не зарегистрированны, для начала, заврешите регистрацию')


def menu_heandlers_client(dp: Dispatcher):
    dp.register_message_handler(change_address, filters.Text('Изменить адрес'))
    dp.register_message_handler(show_menu, commands=['menu', 'меню'])

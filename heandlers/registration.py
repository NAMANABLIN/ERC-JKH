from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram import Dispatcher
from data.defs_orm import create_user, update_user
from keyboards import kb_register
from sqlalchemy.exc import IntegrityError


class FSMReg(StatesGroup):
    address = State()
    is_the_data_correct = State()


async def start(msg: types.Message):
    try:
        await create_user(msg.from_id)
        await FSMReg.address.set()
        await msg.answer('Добро пожаловать в ERC_JKH')
        await msg.answer('Введите свой адрес, можете воспользоваться, кнопкой в меню:', reply_markup=kb_register)
    except IntegrityError:
        await msg.answer('Вы уже зарегистрированы, если хотите изменить свооё местоположение, то пишите что-то')


async def send_address(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = msg.text
    await FSMReg.next()
    await msg.answer(f'Ваш адрес точно {msg.text}?\n'
                     f'Введите "да" или "нет"')


async def check_correctness(msg: types.Message, state: FSMContext):
    message_text = msg.text
    if message_text == 'да':
        async with state.proxy() as data:
            await update_user(msg.from_id, address=data['address'])
        await msg.answer('Вы зарегистрированы!')
        await state.finish()
    elif message_text == 'нет':
        await FSMReg.last()
    else:
        await msg.answer('Введите "да" или "нет"')


def register_heandlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state=None)
    dp.register_message_handler(send_address, state=FSMReg.address)
    dp.register_message_handler(check_correctness, state=FSMReg.is_the_data_correct)

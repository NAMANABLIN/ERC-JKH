from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from data.defs_orm import create_user, update_user
from sqlalchemy.exc import IntegrityError
from fsm import FSMReg
from keyboards import kb_menu



async def start(msg: types.Message):
    try:
        await create_user(msg.from_id)
        await FSMReg.address.set()
        await msg.answer('Добро пожаловать в ERC_JKH')
        await msg.answer('Введите свой адрес, в таком формате:\n'
                         'Улица, номер дома, номер квартиры\n'
                         'Пример: Артёма, 162, 10')
    except IntegrityError:
        await msg.answer('Вы уже зарегистрированы, если хотите изменить своё местоположение, '
                         'то напишите "Изменить местоположение" или зайдите в /menu')


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
        await msg.answer('Вы зарегистрированы!', reply_markup=kb_menu)
        await state.finish()
    elif message_text == 'нет':
        await msg.answer('Введите свой адрес, в таком формате:\n'
                         'Улица, номер дома, номер квартиры\n'
                         'Пример: Артёма, 162, 10')
        await FSMReg.first()
    else:
        await msg.answer('Введите "да" или "нет"')


def register_heandlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state=None)
    dp.register_message_handler(send_address, state=FSMReg.address)
    dp.register_message_handler(check_correctness, state=FSMReg.is_the_data_correct)

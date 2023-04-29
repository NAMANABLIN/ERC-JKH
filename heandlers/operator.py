from aiogram import Dispatcher, types, filters
from keyboards import kb_dialogue_with_operator, remove, kb_menu
from aiogram.dispatcher import FSMContext
from fsm import FSMCommunication_with_operator
from create_bot import bot
from data.defs_orm import get_user, update_user, get_users_report

from fsm import FSMCommunication_with_operator

from aiogram.dispatcher.filters import IsReplyFilter

# class ReplyFilterBot(BoundFilter):
#     async def check(self, msg: types.Message):
#         try:
#             if msg.reply_to_message.from_user.id == bot.id:
#                 print(1)
#                 return True
#         except Exception:
#             pass
async def start_dialogue_with_operator(msg: types.Message):
    await update_user(msg.from_id, waiting_for_operator=True)
    await msg.answer('Напишите вашу проблему в одном сообщении, скоро вам ответит оператор\n'
                     'Оператору будет виден ваш никнейм в телеграм\n'
                     'Когда захотите завершить разговор, нажмите на кнопку',
                     reply_markup=kb_dialogue_with_operator)
    await FSMCommunication_with_operator.first_message.set()


async def first_msg2operator(msg: types.Message, state: FSMContext):
    await update_user(msg.from_id, message2operator=msg.text)
    await FSMCommunication_with_operator.next()


async def talk2operator(msg: types.Message, state: FSMContext):
    if msg.text == 'Завершить разговор':
        user = await get_user(msg.from_id)
        await msg.answer('Диалог закончен!\n'
                         'Надеюсь вам ответили на ваш вопрос', reply_markup=kb_menu)
        await bot.send_message(user.operator, text='Пользователь завершил разговор')
        await update_user(msg.from_id, waiting_for_operator=False, message2operator='', operator=0)
        await state.finish()
    else:
        user = await get_user(msg.from_id)
        await bot.forward_message(user.operator, message_id=msg.message_id, from_chat_id=msg.from_id)


async def start_dialogue_with_user(msg: types.Message):
    operator = await get_user(int(msg.from_id))
    if operator.is_operator:
        msg_texts = msg.text.split()
        user_id=msg_texts[1]
        operator_message = " ".join(msg_texts[2:])
        await update_user(user_id,
                          waiting_for_operator=True,
                          operator=msg.from_id)
        await bot.send_message(user_id, text=operator_message)

async def finish_dialogue_with_user(msg: types.Message):
    operator = await get_user(msg.from_id)
    if operator.is_operator:
        msg_texts = msg.text.split()
        user_id=msg_texts[1]
        await update_user(user_id,
                          waiting_for_operator=False,
                          operator=0)
        await msg.answer('Вы завершили разговор с пользователем')
        await bot.send_message(user_id, text='Оператор завершил с вами разговор')
async def operator_message_handler(msg: types.Message):
    await bot.send_message(msg.reply_to_message.reply_to_message.from_id,
                           text=msg.text)
async def check_reports(msg:types.Message):
    answer = []
    for x in await get_users_report():
        answer.append(f'{x.id} / {x.address}\n{x.message2operator}')
    await msg.answer('Текущие репорты:\n'+'\n\n'.join(answer))
def operator_heandlers_client(dp: Dispatcher):
    dp.register_message_handler(start_dialogue_with_operator, filters.Text('Написать оператору'))
    dp.register_message_handler(first_msg2operator, state=FSMCommunication_with_operator.first_message)
    dp.register_message_handler(talk2operator, state=FSMCommunication_with_operator.talk)
    dp.register_message_handler(start_dialogue_with_user, filters.Command('start_dialogue'))
    dp.register_message_handler(finish_dialogue_with_user, filters.Command('finish_dialogue'))
    dp.register_message_handler(operator_message_handler, is_reply=True)
    dp.register_message_handler(check_reports, filters.Text('Посмотреть кому нужна помощь'))


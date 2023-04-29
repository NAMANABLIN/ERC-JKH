from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_menu.row(
    KeyboardButton('Изменить адрес'),
    KeyboardButton('Написать оператору')
)

kb_menu_for_operator = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_menu_for_operator.row(
    KeyboardButton('Изменить адрес'),
    KeyboardButton('Написать оператору')
).row(
    KeyboardButton('Посмотреть кому нужна помощь')
)

kb_dialogue_with_operator = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_dialogue_with_operator.row(
    KeyboardButton('Завершить разговор')
)
remove = ReplyKeyboardRemove()



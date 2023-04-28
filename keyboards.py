from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb_registration = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_registration.row(
    KeyboardButton('Отправить свою геолокацию', request_location=True))

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.row(
    KeyboardButton('Изменить адрес'),
    KeyboardButton('Написать оператору')
)
remove = ReplyKeyboardRemove()



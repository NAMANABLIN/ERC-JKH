from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb_register = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_register.row(
    KeyboardButton('Отправить свою геолокацию', request_location=True))

remove = ReplyKeyboardRemove()

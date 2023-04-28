from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMReg(StatesGroup):
    address = State()
    is_the_data_correct = State()



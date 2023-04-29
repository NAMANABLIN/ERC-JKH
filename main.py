from create_bot import dp
from aiogram.utils import executor
from data.defs_orm import init_app

from heandlers import admin, menu, registration, operator

menu.menu_heandlers_client(dp)
registration.register_heandlers_client(dp)
admin.menu_heandlers_client(dp)
operator.operator_heandlers_client(dp)

async def on_startup(_):
    print('Бот запущен')


executor.start_polling(dp, skip_updates=True, on_startup=init_app)

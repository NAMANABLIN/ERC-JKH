from data.database import async_db_session
from data.models import User
from sqlalchemy import exc


async def init_app(_):
    await async_db_session.init()


async def create_user(id):
    await User.create(id=id)
    user = await User.get(id)
    return user.id


async def update_user(id, address=None):
    await User.update(id, address=address)
    user = await User.get(id)
    return user.id


async def get_user(id=None):
    try:
        info = await User.get(id)
        return info
    except exc.NoResultFound:
        return "Пользователь не зарегистрирован"

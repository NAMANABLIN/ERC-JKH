from data.database import async_db_session
from data.models import User


async def init_app(_):
    await async_db_session.init()
    # await async_db_session.create_all()


async def create_user(id):
    await User.create(id=id)
    user = await User.get(id)
    return user.id


async def update_user(id, **kwargs):
    await User.update(id, **kwargs)
    user = await User.get(id)
    return user.id


async def get_user(id, **kwargs):
    info = await User.get(id, **kwargs)
    return info
async def get_users_report():
    info = await User.many_get(waiting_for_operator=True)
    return info
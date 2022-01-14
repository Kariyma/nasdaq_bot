from asyncpg import UniqueViolationError

from utils.db_api.database_gino import db_gino
from utils.db_api.schemas.user import User


async def add_user(user_id: int, name: str, email: str = None):
    try:

        user = User(user_id=user_id, name=name, email=email)
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    return await User.query.gino.all()


async def select_user(user_id: int):
    return await User.query.where(User.user_id == user_id).gino.first()


async def count_users():
    return await db_gino.func.count(User.user_id).gino.scalar()


async def update_user_email(user_id, email):
    user = await User.get(user_id)
    await user.update(email=email).apply()

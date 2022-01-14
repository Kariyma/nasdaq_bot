import asyncio

from data import config
from utils.db_api import quick_commands
from utils.db_api.database_gino import db_gino


async def test_gino():
    await db_gino.set_bind(config.POSTGRES_URI)
    await db_gino.gino.drop_all()
    await db_gino.gino.create_all()

    print("Добавляем пользователей")
    await quick_commands.add_user(1, "One", "email")
    await quick_commands.add_user(2, "Vasya", "vv@gmail.com")
    await quick_commands.add_user(3, "1", "1")
    await quick_commands.add_user(4, "1", "1")
    await quick_commands.add_user(5, "John", "john@mail.com")
    print("Готово")

    users = await quick_commands.select_all_users()
    print(f"Получил всех пользователей: {users}")

    count_users = await quick_commands.count_users()
    print(f"Всего пользователей: {count_users}")

    user = await quick_commands.select_user(user_id=5)
    print(f"Получил пользователя: {user}")

loop = asyncio.get_event_loop()
loop.run_until_complete(test_gino())
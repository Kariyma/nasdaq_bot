from aiogram import executor

from loader import dp, db, db_gino
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.db_api import database_gino


async def on_startup(dispatcher):

    print("Подключаем БД")
    await database_gino.on_startup(dp)
    print("Готово")

    print("Чистим базу данных")
    await db_gino.gino.drop_all()
    # await db_gino.gino.drop_all(tables=[User.__table__], checkfirst=True)
    print("Готово")

    print("Создаём таблицы")
    await db_gino.gino.create_all()
    print("Готово")

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

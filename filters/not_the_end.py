from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class NotTheEnd(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.text != '/break'
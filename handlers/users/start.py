from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Command

import asyncpg

from loader import dp, bot, db
from utils.db_api.user import User
from utils.google.tests import test_email, test_spreadsheet_id

from utils.db_api import quick_commands as commands
from states import Form
from filters import NotTheEnd


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    async with state.proxy() as data:
        data["name"] = name
    await message.answer(f'Здравствуйте, {message.from_user.full_name}!')
    user = await commands.select_user(message.from_user.id)
    print(user)
    if user:
        email = user.email
        await message.answer(
            "\n".join(
                [
                    f'Ваш запрос на мониториг действует.',
                    f'Ваш Google Email для доступа к таблице {email}.\n\n'
                    f'Вы можете изменить свой Google Email с помощью команды \email'
                ]))
    else:
        await message.answer(
                "\n".join(
                    [
                        'Для запуска мониторинга необходимы дополнительные данные.',
                        'Пришлите мне свой Google Email.\n\n'
                        'Вы также можете прислать мне команду /break '
                        'чтобы отказаться от запуска монторинга'
                    ]))
        await Form.email.set()


@dp.message_handler(Command("break"), state=Form.email)
async def the_end(message: types.Message, state: FSMContext):
    await message.answer('Вы прервали формирование запроса на мониторинг.')
    await state.finish()


@dp.message_handler(NotTheEnd(), state=Form.email)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    if test_email(answer):
        data = await state.get_data()
        name = data.get('name')
        email = answer
        try:
            await commands.add_user(user_id=message.from_user.id,
                                    name=name, email=email)
            count = await commands.count_users()
        except asyncpg.exceptions.UniqueViolationError:
            pass
        await message.answer('Благодарю Вам.\n'
                             'Мониторинг включен.')
        await state.finish()
    else:
        await message.answer('К сожалению введёный email некорректный. \n'
                             'Пожалуйста в пришлите Ваш Google email. \n\n'
                             'Вы также можете прислать мне /break '
                             'чтобы отказаться от запуска монторинга.')



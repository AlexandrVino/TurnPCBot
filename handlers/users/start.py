from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from utils.db_api.sql import create_pool


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    result = await db.get_user(message.from_user.values['id'])
    if result is None:
        data = [message.from_user.id, message.from_user.language_code, None]
        await db.add_user(*data)
    await message.answer(f"Hi, {message.from_user.full_name}!")

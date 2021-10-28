from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """
    :param message: aiogram.types.Message
    :returns: None
    function, which will register new user
    """
    result = await db.get_user(message.from_user.values['id'])
    if result is None:
        data = [message.from_user.id, message.from_user.language_code, None]
        await db.add_user(*data)
    await message.answer(f"Hi, {message.from_user.full_name}!")

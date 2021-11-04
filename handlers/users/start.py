from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from utils.misc.get_dict import get_dict


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """
    :param message: aiogram.types.Message
    :returns: None
    function, which will register new user
    """
    result = await db.get_user(message.from_user.values['id'])
    if result is None:
        await db.add_user(**await get_dict(**message.from_user.values))
    await message.answer(f"Hi, {message.from_user.full_name}!")

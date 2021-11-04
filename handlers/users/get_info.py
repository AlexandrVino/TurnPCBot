import json

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, db
from utils.misc.get_dict import get_dict


@dp.message_handler(Command('get_info'))
async def get_info(message: types.Message) -> types.Message.answer:
    """
    :param message: aiogram.types.Message - user message
    :returns None or info about incorrect data:
    function, which will return info about user
    """

    user_data = await db.get_user_or_create(**await get_dict(**message.from_user.values))
    computers = json.loads(user_data.get('computers') if user_data.get('computers') is not None else '[]')
    server = user_data.get('server')

    if computers:
        string = (
                " " * 8 + "{}:\n" +
                " " * 16 + "Mac = {}\n" +
                " " * 16 + "Ip = {}\n"
        )

        comps = '\n\n' + '\n\n'.join(map(lambda computer: string.format(*computer.values()), computers))
    else:
        comps = "You haven't any computer yet"

    mess = (
        f"Id: {message.from_user.id}\n"
        f"Username: {message.from_user.username}\n"
        f"Language: {message.from_user.language_code}\n"
        f"Computers: {comps}\n"
        f"Server: {server if server is not None else 'You not set server'}\n"
    )
    return await message.answer(mess, disable_web_page_preview=True)

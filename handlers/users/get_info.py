import json

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, db


@dp.message_handler(Command('get_info'))
async def get_info(message: types.Message) -> types.Message.answer:
    """
    :param message: aiogram.types.Message
    :returns None or info about incorrect data:
    function, which will be create sql database
    """

    user_data = await db.get_user_or_create(**{
        'chat_id': message.from_user.values['id'],
        'language_code': message.from_user.values['language_code'],
        'computers': None,
        'server': None
    })

    computers = user_data.get('computers')
    if computers is not None:
        computers = json.loads(computers)

        comps = '\n\n'.join(['\n'.join(
            [f'        {key.capitalize()} = {value}' if key != 'name' else f'    {value}:'
             for key, value in computer.items()]) for computer in computers])
    else:
        comps = "You haven't any computer yet"

    server = user_data.get('server')
    mess = (
        f"Username: {message.from_user.username}\n"
        f"Language: {message.from_user.language_code}\n"
        f"Computers: \n\n{comps}\n\n"
        f"Server: {server if server is not None else 'You not set server'}\n"
    )
    return await message.answer(mess, disable_web_page_preview=True)

import logging

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, db

from re import findall, match
import json
from utils.db_api.sql import create_pool


@dp.message_handler(Command('add_pc'))
async def on_pc(message: types.Message):
    """

    """
    try:
        search = '[0-9A-F]{2}.' * 5 + '[0-9A-F]{2}'

        data = [item.split('=') for item in message.text.strip().split()[1:]]
        data = {key: value for key, value in data}

        if len(data['mac']) == 12:
            data['mac'] = '-'.join([data['mac'][i:i + 2] for i in range(0, 12, 2)])

        data["mac"] = findall(search, data['mac'])[0]

        assert match(search, data['mac'])

    except (IndexError, AssertionError):
        await message.answer('Incorrect MAC address!')
        return await message.answer('Example: "/add_pc [0A-00-27-00-00-04]"\n"-" can be also ":", "." and other')

    result = await db.get_user(message.from_user.id)
    if result is not None:
        user_pc = json.loads(result.get('comps'))
    else:
        reg_data = [message.from_user.values['id'], message.from_user.values['language_code'], []]
        await db.add_user(*reg_data)
        user_pc = []

    if user_pc is None:
        user_pc = []

    if any([item.get("mac") == data["mac"] for item in user_pc]):
        return await message.answer("This PC have already added")

    user_pc += [data]
    user_pc = json.dumps(user_pc)

    await db.update_user_comps(user_pc, message.from_user.values['id'])
    return await message.answer("Computer added successfully")

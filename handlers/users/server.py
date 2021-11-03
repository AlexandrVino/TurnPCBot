from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from requests import get

from loader import dp, db
from states.add_server import *
from utils.misc.get_dict import get_dict


@dp.message_handler(Command('set_server'))
async def set_server(message: types.Message) -> types.Message.answer:
    """
    :param message: aiogram.types.Message
    :returns None or info about incorrect data:
    function, which will be create sql database
    """

    await AddServerForm.protocol.set()
    return await message.answer("Please write server protocol (Example: http, https) or server address")


@dp.message_handler(state=AddServerForm.protocol)
async def process_protocol(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    Process computer name
    :param message: aiogram.types.Message - message, which send user
    :param state: aiogram.dispatcher.FSMContext - storage with data
    """
    protocol = message.text.strip()
    accept_protocols = ('http', 'https')
    if any(pr in protocol for pr in accept_protocols):
        try:
            data = get(protocol + '/try_connect', json={"message": 'try connect'})
            assert data.json()['status'] == 200
            kwargs = await get_dict(**message.from_user.values, server=protocol)
            await db.update_user_server(**kwargs)
            await state.finish()
            return await message.answer("Server added successfully")
        except BaseException:

            mess = (
                "Error\nIt can be called because of:\n"
                "1. Incorrect server address\n"
                "2. Server discard connection\n"
                "3. Incorrect answer "
                "(<a href='https://github.com/AlexandrVino/TurnPCBot/blob/master/README.md#server'>"
                "see it for more info</a>)"
            )

            return await message.answer(mess, disable_web_page_preview=True)
    if protocol not in accept_protocols:
        return await message.answer("Protocol must be http or https")

    async with state.proxy() as server_data:
        server_data['protocol'] = protocol

    await AddServerForm.hostname.set()
    return await message.answer("Please write server host")


@dp.message_handler(state=AddServerForm.hostname)
async def process_hostname(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    Process computer mac address
    """

    hostname = message.text.strip()

    async with state.proxy() as server_data:
        server_data['hostname'] = hostname

    await AddServerForm.port.set()
    return await message.answer("Please write server port")


@dp.message_handler(state=AddServerForm.port)
async def process_port(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    Process computer ip address (on LAN)
    """
    port = message.text

    async with state.proxy() as server_data:
        server_data['port'] = port
        kwargs = await get_dict(**message.from_user.values, server='{}://{}:{}'.format(*server_data._data.values()))
    await db.update_user_server(**kwargs)
    await db.update_user_server(**kwargs)
    await state.finish()

    return await message.answer("Server added successfully")

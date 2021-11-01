import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from states.add_server import *
from loader import dp, db
from requests import get
from re import findall, match
import json


@dp.message_handler(Command('set_server'))
async def add_pc(message: types.Message) -> types.Message.answer:
    """
    :param message: aiogram.types.Message
    :returns None or info about incorrect data:
    function, which will be create sql database
    """

    await AddServerForm.protocol.set()
    return await message.answer("Please write server protocol (Example: http, https) or server address")


@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    return await message.answer('You cancelled this action.')


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
            kwargs = {
                'chat_id': message.from_user.values['id'],
                'language_code': message.from_user.values['language_code'],
                'computers': None,
                'server': protocol
            }
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
async def process_mac(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    Process computer mac address
    """

    hostname = message.text.strip()

    async with state.proxy() as server_data:
        server_data['hostname'] = hostname

    await AddServerForm.port.set()
    return await message.answer("Please write server port")


@dp.message_handler(state=AddServerForm.port)
async def process_ip(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    Process computer ip address (on LAN)
    """
    port = message.text

    async with state.proxy() as server_data:
        server_data['port'] = port
        kwargs = {
            'chat_id': message.from_user.values['id'],
            'language_code': message.from_user.values['language_code'],
            'computers': None,
            'server': '{}://{}:{}'.format(*server_data._data.values())
        }

    await db.update_user_server(**kwargs)
    await state.finish()

    return await message.answer("Server added successfully")

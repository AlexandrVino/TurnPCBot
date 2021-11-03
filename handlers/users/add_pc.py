import json
import logging
from re import findall

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, db
from states.computer import *
from utils.misc.get_dict import get_dict


@dp.message_handler(Command('add_pc'))
async def add_pc(message: types.Message) -> types.Message.answer:
    """
    :param message: aiogram.types.Message - user message
    :returns: types.Message.answer
    function, which will start add_pc state and ask computer name
    """

    await AddPcForm.name.set()
    return await message.answer("Please write computer name")


@dp.message_handler(state=AddPcForm.name)
async def process_name(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    Process computer name
    :param message: aiogram.types.Message - user message - message, which send user 
    :param state: aiogram.dispatcher.FSMContext - storage with data
    :return: types.Message.answer
    function, which will ask computer mac address
    """
    computer_name = message.text
    user_pc = json.loads(await db.get_user_computers(**await get_dict(**message.from_user.values)))

    if any([item.get("name") == computer_name for item in user_pc]):
        return await message.answer("PC with this name have already added")

    async with state.proxy() as computer_data:
        computer_data['user_pc'] = user_pc
        computer_data['name'] = message.text

    await AddPcForm.mac_address.set()
    return await message.answer("Please write computer mac address")


@dp.message_handler(state=AddPcForm.mac_address)
async def process_mac(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    Process computer name
    :param message: aiogram.types.Message - user message - message, which send user
    :param state: aiogram.dispatcher.FSMContext - storage with data
    :return: types.Message.answer
    function, which will ask computer ip address
    """

    message_text = message.text

    try:
        search = '[0-9A-F]{2}.' * 5 + '[0-9A-F]{2}'

        if len(message_text) == 12:
            message_text = '-'.join([message_text[i:i + 2] for i in range(0, 12, 2)])
        message_text = findall(search, message_text)[0]

    except IndexError:
        await message.answer('Incorrect MAC address!')
        return await message.answer(
            'Example: 00-11-22-33-44-55"\n"-" can be also ":", "." and other')

    async with state.proxy() as computer_data:
        if any([item.get("mac") == message_text for item in computer_data['user_pc']]):
            return await message.answer("PC with this mac address have already added")
        computer_data['mac'] = message_text

    await AddPcForm.ip_address.set()
    return await message.answer("Please write computer ip address")


@dp.message_handler(state=AddPcForm.ip_address)
async def process_ip(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    Process computer name
    :param message: aiogram.types.Message - user message - message, which send user
    :param state: aiogram.dispatcher.FSMContext - storage with data
    :return: types.Message.answer
    function, which will add computer to database
    """
    message_text = message.text

    try:
        message_text = [int(item) for item in message_text.split('.') if item.isdigit()]
        assert len(message_text) == 4

    except AssertionError:
        await message.answer('Incorrect IP address!\nExample: 192.168.255.255')

    kwargs = await get_dict(**message.from_user.values)
    user_pc = await db.get_user_computers(**kwargs)
    user_pc = json.loads(user_pc)

    async with state.proxy() as computer_data:
        if any([item.get("ip") == message.text for item in computer_data['user_pc']]):
            return await message.answer("PC with this ip address have already added")
        computer_data['ip'] = message.text
        user_pc += [{key: value for key, value in computer_data._data.items() if key != 'user_pc'}]
        user_pc = json.dumps(user_pc)
    kwargs['computers'] = user_pc
    await db.update_user_computers(**kwargs)
    await state.finish()

    return await message.answer("Computer added successfully")

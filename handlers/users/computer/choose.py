import json
import logging

from aiogram import types
from aiogram.dispatcher.filters import Command
from wakeonlan import send_magic_packet

from data.config import BOT_NAME
from keyboards.inline.callback_datas import add_pc_callback
from loader import dp, db
from keyboards.inline.my_pc import get_pc_keyboard

from utils.misc.client import send_packet
from utils.misc.get_dict import get_dict


@dp.message_handler(Command('choose_pc'))
async def choose_computer(message: types.Message) -> types.Message.answer:
    """
    :param message: aiogram.types.Message - user message
    :returns: types.Message.answer
    Allow user to cancel any action
    """

    data = await db.get_user_computers(chat_id=message.from_user.id)
    data = json.loads(data)
    if any(data):
        return await message.answer(f"Choose any of computers:", reply_markup=await get_pc_keyboard(data, callback='add'))
    else:
        return await message.answer(f"You haven't any computers yet")


@dp.callback_query_handler(add_pc_callback.filter())
async def on_pc_callback(call: types.CallbackQuery, callback_data: dict) -> None:
    """
    :param call: aiogram.types.CallbackQuery - callback (button which push user)
    :param callback_data: dict - data about computer
    :returns: types.Message.answer
    function, which will wake up computer
    """

    await call.answer(cache_time=60)
    _, name, mac, _ = callback_data.values()

    if BOT_NAME == 'TurnOnPcBot':
        kwargs = await get_dict(**call.from_user.values)
        host = await db.get_user_server(**kwargs) + '/wake_up'
        if host == '':
            await call.message.answer(f"You haven't server yet")
            return
        data = await send_packet(url=host, data={'mac': mac})
        if data:
            await call.message.answer(f'Computer <i><b>"{name}"</b></i> wake up')
        else:
            mess = (
                "Error\nIt can be called because of:\n"
                "1. Incorrect server address\n"
                "2. Server discard connection\n"
                "3. Incorrect answer "
                "(<a href='https://github.com/AlexandrVino/TurnPCBot/blob/master/README.md#server'>"
                "see it for more info</a>)"
            )
            await call.message.answer(mess, disable_web_page_preview=True)
    else:
        send_magic_packet(mac)


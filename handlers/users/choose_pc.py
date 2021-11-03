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
async def choose_computer(message: types.Message):
    """
    :param message: aiogram.types.Message
    :returns: None
    """

    data = await db.get_user_computers(chat_id=message.from_user.id)
    data = json.loads(data)
    if any(data):
        await message.answer(f"Choose any of computers:", reply_markup=await get_pc_keyboard(data, callback='add'))
    else:
        await message.answer(f"You haven't any computers yet")


@dp.callback_query_handler(add_pc_callback.filter())
async def on_pc_callback(call: types.CallbackQuery, callback_data: dict):
    """
    :param call: aiogram.types.CallbackQuery
    :param callback_data: dict
    :returns: None
    function, which will wake pc
    """

    await call.answer(cache_time=60)
    _, name, mac, _ = callback_data.values()
    logging.info(callback_data)

    if BOT_NAME == 'TurnOnPcBot':
        kwargs = await get_dict(**call.from_user.values)
        host = await db.get_user_server(**kwargs)
        data = await send_packet(url=host, data={'mac': mac})
        if data:
            await call.message.answer(f'Computer <i><b>"{name}"</b></i> wake up')
        else:
            logging.error("some err")
    else:
        send_magic_packet(mac)


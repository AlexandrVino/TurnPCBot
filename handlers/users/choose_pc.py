import json
import logging

from aiogram import types
from aiogram.dispatcher.filters import Command
from wakeonlan import send_magic_packet

from data.config import BOT_NAME
from keyboards.inline.callback_datas import my_pc_callback
from loader import dp, db
from keyboards.inline.my_pc import get_pc_keyboard

from utils.misc.client import send_packet


@dp.message_handler(Command('choose_pc'))
async def choose_computer(message: types.Message):
    """
    :param message: aiogram.types.Message
    :returns: None
    """

    data = await db.get_user_computers(chat_id=message.from_user.id)
    data = json.loads(data)
    if any(data):
        await message.answer(f"Choose any of computers:", reply_markup=await get_pc_keyboard(data))
    else:
        await message.answer(f"You haven't any computers yet")


@dp.callback_query_handler(my_pc_callback.filter())
async def on_pc_callback(call: types.CallbackQuery, callback_data: dict):
    """
    :param call: aiogram.types.CallbackQuery
    :param callback_data: dict
    :returns: None
    function, which will wake pc
    """

    await call.answer(cache_time=60)
    tag, name, mac, ip = callback_data.values()
    logging.info(callback_data)

    if BOT_NAME == 'TurnOnPcBot':
        host = 'web'  # Write your company server address (Example: 127.0.0.1:5000)
        data = await send_packet(url=f'http://{host}/wake_up', data={'mac': mac})
        if data:
            await call.message.answer(f'Computer <i><b>"{name}"</b></i> wake up')
        else:
            logging.error("some err")
    else:
        send_magic_packet(mac)


@dp.callback_query_handler(text='cancel')
async def cancel(call: types.CallbackQuery):
    """
    :param call: aiogram.types.CallbackQuery
    :returns: None
    function, which will cancel keyboard
    """
    await call.answer(cache_time=60)
    await call.answer(f'You canceled this action', show_alert=True)
    await call.message.edit_reply_markup()
    await call.message.edit_text(f'You canceled this action')

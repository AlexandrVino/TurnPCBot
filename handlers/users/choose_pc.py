import json

from aiogram import types
from aiogram.dispatcher.filters import Command
from wakeonlan import send_magic_packet

from keyboards.inline.callback_datas import my_pc_callback
from loader import dp, db
from keyboards.inline.my_pc import get_pc_keyboard


@dp.message_handler(Command('choose_pc'))
async def choose_computer(message: types.Message):
    """
    :param message: aiogram.types.Message
    :returns: None
    """

    data = await db.get_user_comps(chat_id=message.from_user.id)
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
    send_magic_packet(mac)
    await call.message.answer(f'Computer <i><b>"{name}"</b></i> wake up')


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

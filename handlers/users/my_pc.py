import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from wakeonlan import send_magic_packet

from keyboards.inline.callback_datas import my_pc_callback
from loader import dp
from keyboards.inline.my_pc import get_pc_keyboard


@dp.message_handler(Command('on_pc'))
async def on_pc(message: types.Message):
    data = [
        {'name': 'comp_1', 'mac': 'A8-A1-59-25-B8-6A'},
        {'name': 'comp_2', 'mac': 'E0-D5-5E-88-FD-AA'},
        {'name': 'comp_3', 'mac': '0C-84-DC-8D-82-49'}
    ]
    await message.answer(f"Choose any of computers:", reply_markup=await get_pc_keyboard(data))


@dp.callback_query_handler(my_pc_callback.filter())
async def on_pc_callback(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    tag, name, mac = callback_data.values()
    send_magic_packet(mac)
    await call.message.answer(f'Computer <i><b>"{name}"</b></i> wake up')


@dp.callback_query_handler(text='cancel')
async def cancel(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.answer(f'You canceled this action', show_alert=True)
    await call.message.edit_reply_markup()
    await call.message.edit_text(f'You canceled this action')

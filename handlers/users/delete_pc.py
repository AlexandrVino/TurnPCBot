import json

from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.callback_datas import delete_pc_callback
from keyboards.inline.my_pc import get_pc_keyboard
from loader import dp, db
from utils.misc.get_dict import get_dict


@dp.message_handler(Command('delete_pc'))
async def choose_computer(message: types.Message):
    """
    :param message: aiogram.types.Message - user message
    :returns: None
    """

    data = await db.get_user_computers(chat_id=message.from_user.id)
    data = json.loads(data)
    if any(data):
        await message.answer(f"Choose any of computers:",
                             reply_markup=await get_pc_keyboard(map(lambda x: {'name': x['name']}, data),
                                                                callback='delete'))
    else:
        await message.answer(f"You haven't any computers yet")


@dp.callback_query_handler(delete_pc_callback.filter())
async def on_pc_callback(call: types.CallbackQuery, callback_data: dict):
    """
    param call: aiogram.types.CallbackQuery - callback (button which push user)
    :param callback_data: dict
    :returns: None
    function, which will delete pc
    """

    await call.answer(cache_time=60)
    _, name = callback_data.values()

    kwargs = await get_dict(**call.from_user.values)
    kwargs['computers'] = json.dumps(
        [pc for pc in json.loads(await db.get_user_computers(**kwargs)) if pc['name'] != name])
    await db.update_user_computers(**kwargs)

    data = await db.get_user_computers(chat_id=call.from_user.id)
    data = json.loads(data)
    if any(data):
        await call.message.edit_reply_markup(
            reply_markup=await get_pc_keyboard(map(lambda x: {'name': x['name']}, data),
                                               callback='delete'))

    else:
        await call.message.edit_reply_markup()
        await call.message.edit_text(f'Delete successfully!')

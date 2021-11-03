from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db


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

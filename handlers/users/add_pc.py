import logging

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command('add_pc'))
async def on_pc(message: types.Message):
    """

    """
    try:
        mac_new_pc = message.text.strip().split()[1]
        if len(mac_new_pc) == 17:
            sep = mac_new_pc[2]
            mac_new_pc = mac_new_pc.replace(sep, '-')
        assert len(mac_new_pc) == 17

    except (IndexError, AssertionError):
        await message.answer('Incorrect MAC address!')
        return await message.answer('Example: "/add_pc 0A-00-27-00-00-04"\n"-" can be also ":", "." and other')

    '''cursor = CONNECTION.cursor()
    cursor.execute(f"""SELECT comps FROM public.userinfo WHERE chat_id = {message.from_user.values['id']}""")
    user_pc = cursor.fetchone()

    if user_pc[0] is not None and mac_new_pc in user_pc[0].split(','):
        return await message.answer(message.from_user['id'], "This PC have already added")

    user_pc = ','.join(list(user_pc) + [mac_new_pc]) if user_pc[0] is not None else mac_new_pc

    cursor.execute(
        f"""UPDATE public.userinfo SET comps='{user_pc}' WHERE chat_id = '{message.from_user.values['id']}' ;""")
    CONNECTION.commit()'''
    return await message.answer("Computer added successfully")

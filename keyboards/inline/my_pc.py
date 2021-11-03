from keyboards.inline.callback_datas import delete_pc_callback, add_pc_callback
from loader import dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_pc_keyboard(data: [dict], callback: str) -> InlineKeyboardMarkup or bool:
    """
    ::param data: list with json objects (name: str - name of a computer, mac: str - MAC address of current pc)
    ::param data:example: [{'name': 'My_PC', 'mac': 'A1-B2-C3-D4-E5-F6'}]
    ::returns: inline keyboard with computers added to the list
    """
    method = delete_pc_callback if callback == 'delete' else add_pc_callback

    keyboard = InlineKeyboardMarkup(row_width=2)

    for button_data in data:
        keyboard.insert(InlineKeyboardButton(button_data['name'], callback_data=method.new(**button_data)))
    keyboard.row(InlineKeyboardButton('Cancel', callback_data='cancel'))

    return keyboard



from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    """
    :param message: aiogram.types.Message
    :returns: message with bot skills
    function, which will send bot skills
    """
    text = (
        "List of commands: ",
        "/start - Start dialog",
        "/help - Get bot skills",
        "/set_server reset you server address",
        "/get_info return info about your account",
        "/delete_pc Display user's computers for delete",
        "/choose_pc Display user's computers for wake up",
        "/cancel Cancel any action",
        "/add_pc - Adding pc to user list"
    )

    await message.answer("\n".join(text))

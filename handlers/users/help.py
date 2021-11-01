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
        "/host reset you server address",
        "/me return info about your account",
        "/choose_pc Display user's computers",
        "/add_pc mac=[0A-00-27-00-00-04] name=MyComputer - Adding pc to user list"
    )

    await message.answer("\n".join(text))

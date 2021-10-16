from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("List of commands: ",
            "/start - Start dialog",
            "/on_pc Display user's computers",
            "/add_pc [0A-00-27-00-00-04] - Adding pc to user list",
            "/help - Get bot skills")

    await message.answer("\n".join(text))

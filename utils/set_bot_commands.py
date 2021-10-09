from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Launch bot"),
            types.BotCommand("help", "Display help"),
            types.BotCommand("on_pc", "Display user's computers"),
        ]
    )

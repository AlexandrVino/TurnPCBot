from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    """
    :param dp: Dispatcher
    :returns: None
    function, which will reset bot command
    """
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Launch bot"),
            types.BotCommand("help", "Display help"),
            types.BotCommand("choose_pc", "Display user's computers"),
            types.BotCommand("add_pc", "Adding pc to user list"),
        ]
    )

from aiogram.dispatcher.filters.state import State, StatesGroup


class AddServerForm(StatesGroup):
    protocol = State()
    hostname = State()
    port = State()

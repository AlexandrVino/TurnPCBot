from aiogram.dispatcher.filters.state import State, StatesGroup


class AddPcForm(StatesGroup):
    name = State()
    mac_address = State()
    ip_address = State()

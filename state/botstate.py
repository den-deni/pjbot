from aiogram.fsm.state import State, StatesGroup


class BotState(StatesGroup):
    key = State()
    user_data = State()
    file_data = State()
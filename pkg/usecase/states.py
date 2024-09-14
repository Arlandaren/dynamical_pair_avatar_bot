from aiogram.fsm.state import State, StatesGroup

class States(StatesGroup):
    forward = State()
    number = State()
    password = State()
    code = State()
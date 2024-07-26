from aiogram.fsm.state import StatesGroup, State


class MyStates(StatesGroup):
    wait_list = State()
    done = State()


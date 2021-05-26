from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    action_state = State()
    specialization_state = State()
    doctor_select_state=State()
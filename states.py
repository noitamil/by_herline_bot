from aiogram.fsm.state import State, StatesGroup


class OrderFlow(StatesGroup):
    choosing_size = State()

    entering_first_name = State()
    entering_last_name = State()
    entering_phone = State()
    entering_contact = State()

    confirming_order = State()

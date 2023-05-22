from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    deposit = State()
    withdrawal = State()
    ymoney = State()
    crypto = State()
    contract = State()

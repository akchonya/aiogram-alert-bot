from aiogram.fsm.state import StatesGroup, State

class StatesDrawVahta(StatesGroup):
    GET_CHAR = State()
    GET_ROW = State()
    GET_COLUMN = State()

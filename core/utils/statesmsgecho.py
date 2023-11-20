from aiogram.fsm.state import StatesGroup, State


class StatesMsgEcho(StatesGroup):
    GET_MSG = State()
    GET_MSG_PIN = State()

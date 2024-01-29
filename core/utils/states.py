from aiogram.fsm.state import StatesGroup, State


class StatesDrawVahta(StatesGroup):
    GET_CHAR = State()
    GET_ROW = State()
    GET_COLUMN = State()


class StatesVahta(StatesGroup):
    GET_PHOTO = State()


class StatesMsgEcho(StatesGroup):
    GET_MSG = State()
    GET_MSG_PIN = State()


class StatesSell(StatesGroup):
    GET_ADVERT = State()
    CONFIRM = State()

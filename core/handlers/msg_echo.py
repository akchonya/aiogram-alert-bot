from os import getenv
from dotenv import load_dotenv

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from core.utils.statesmsgecho import StatesMsgEcho


load_dotenv()
ADMIN_ID = getenv("ADMIN_ID")
DORM_CHAT_ID = getenv("DORM_CHAT_ID")


async def get_msg(message: types.Message, state: FSMContext):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer("Send a message to the chat:")
        await state.set_state(StatesMsgEcho.GET_MSG)
    else:
         await message.answer("You are not authorized.")

async def msg_echo(message: types.Message, state: FSMContext, bot: Bot):
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=DORM_CHAT_ID)
        await message.answer("Done")
    except TypeError:
        pass
    await state.clear()


async def get_msg_pin(message: types.Message, state: FSMContext):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer("Send a message to the chat:")
        await state.set_state(StatesMsgEcho.GET_MSG_PIN)
    else:
         await message.answer("You are not authorized.")

async def msg_echo_pin(message: types.Message, state: FSMContext, bot: Bot):
    try:
        # Send a copy of the received message
        msg = await message.send_copy(chat_id=DORM_CHAT_ID)
        await bot.pin_chat_message(DORM_CHAT_ID, msg.message_id, True)
        await message.answer("Done")
    except TypeError:
        pass
    await state.clear()
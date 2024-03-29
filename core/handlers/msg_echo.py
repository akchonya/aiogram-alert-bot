"""
/msg_echo and /msg_echo_pin are admin commands
You can send or send and pin any message to the chat
on behalf of the bot
"""

from aiogram import F, Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.utils.states import StatesMsgEcho
from core.filters.basic import isAdmin
from core.utils.config import DORM_CHAT_ID


msg_echo_router = Router()
msg_echo_pin_router = Router()


@msg_echo_router.message(isAdmin(), Command("msg_echo"))
async def get_msg(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Send a message or type /cancel to cancel.", reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(StatesMsgEcho.GET_MSG)


@msg_echo_router.message(Command("cancel"), StatesMsgEcho.GET_MSG)
@msg_echo_router.message(F.text.casefold() == "cancel", StatesMsgEcho.GET_MSG)
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("/msg_echo is cancelled.")


@msg_echo_router.message(StatesMsgEcho.GET_MSG)
async def process_chars(message: Message, state: FSMContext, bot: Bot) -> None:
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=DORM_CHAT_ID)
        await message.answer("Message is sent.")
    except TypeError:
        pass
    await state.clear()


@msg_echo_pin_router.message(isAdmin(), Command("msg_echo_pin"))
async def get_msg_pin(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Send a message or type /cancel to cancel.", reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(StatesMsgEcho.GET_MSG_PIN)


@msg_echo_pin_router.message(Command("cancel"), StatesMsgEcho.GET_MSG_PIN)
@msg_echo_pin_router.message(F.text.casefold() == "cancel", StatesMsgEcho.GET_MSG_PIN)
async def cancel_handler_pin(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("/msg_echo_pin is cancelled.")


@msg_echo_pin_router.message(StatesMsgEcho.GET_MSG_PIN)
async def process_chars_pin(message: Message, state: FSMContext, bot: Bot) -> None:
    try:
        # Send a copy of the received message
        msg = await message.send_copy(chat_id=DORM_CHAT_ID)
        await bot.pin_chat_message(DORM_CHAT_ID, msg.message_id, True)
        await message.answer("Message is sent and pinned.")
    except TypeError:
        await message.answer("Something went wrong. Try again.")
    await state.clear()

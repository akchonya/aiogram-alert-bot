from pillow_bot.helpers import pillow_draw

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from core.keyboards.draw_vahta_kb import vahta_chars_kb, vahta_rows_kb, vahta_columns_kb
from core.filters.basic import isAdmin
from core.utils.config import DORM_CHAT_ID
from core.utils.states import StatesDrawVahta


draw_vahta_router = Router()


@draw_vahta_router.message(isAdmin(), Command("draw_vahta"))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(StatesDrawVahta.GET_CHAR)
    await message.answer(
        "Pick a characher or type /cancel to cancel.",
        reply_markup=vahta_chars_kb,
        resize_keyboard=True,
    )


# A cancelation option
@draw_vahta_router.message(isAdmin(), Command("cancel"))
@draw_vahta_router.message(isAdmin(), F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "/draw_vahta is cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


# Set appropriate answers
chars = ("biblio", "commie", "diana", "eblan", "lyarva")


@draw_vahta_router.message(StatesDrawVahta.GET_CHAR, F.text.casefold().in_(chars))
async def process_chars(message: Message, state: FSMContext) -> None:
    await state.set_state(StatesDrawVahta.GET_ROW)
    await state.update_data(char=message.text)
    await message.answer(
        f"OK, you picked {message.text}. Now choose a row:", reply_markup=vahta_rows_kb
    )


# Adress any unwanted answers
@draw_vahta_router.message(StatesDrawVahta.GET_CHAR)
async def process_unknown_char(message: Message) -> None:
    await message.reply("WTF is that?! Choose from options below or type /cancel")


# Set appropriate answers
rows = ("1", "2", "3", "4", "5", "6")


@draw_vahta_router.message(StatesDrawVahta.GET_ROW, F.text.in_(rows))
async def process_row(message: Message, state: FSMContext) -> None:
    await state.set_state(StatesDrawVahta.GET_COLUMN)
    await state.update_data(row=message.text)
    await message.answer(
        f"OK, you picked row {message.text}. Now choose a column:",
        reply_markup=vahta_columns_kb,
    )


# Adress any unwanted answers
@draw_vahta_router.message(StatesDrawVahta.GET_ROW)
async def process_unknown_row(message: Message) -> None:
    await message.reply("WTF is that?! Choose from options below or type /cancel")


# Set appropriate answers
columns = ("1", "2", "3", "4", "5", "6", "7")


@draw_vahta_router.message(StatesDrawVahta.GET_COLUMN, F.text.in_(columns))
async def process_row_pin(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.answer(
        f"OK, you picked column {message.text}. Drawing..",
        reply_markup=ReplyKeyboardRemove(),
    )

    # Get the data from previous states
    context_data = await state.get_data()
    char = context_data.get("char")
    row = int(context_data.get("row"))
    column = int(message.text)

    # Use the function to draw
    await pillow_draw(char, row, column)
    # Send messages to an admin and the chat
    await message.answer("Done. Use /vahta to check")
    await bot.send_message(DORM_CHAT_ID, "/vahta оновлена.")
    await state.clear()


# Adress any unwanted answers
@draw_vahta_router.message(StatesDrawVahta.GET_COLUMN)
async def process_unknown_column(message: Message) -> None:
    await message.reply("WTF is that?! Choose from options below or type /cancel")

from os import getenv
from dotenv import load_dotenv

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from core.utils.statesdrawvahta import StatesDrawVahta

from pillow_bot.helpers import pillow_draw



load_dotenv()
ADMIN_ID = getenv("ADMIN_ID")


async def get_cell(message: types.Message, state: FSMContext):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer("Choose a char from\n biblio, commie, diana, eblan, lyarva")
        await state.set_state(StatesDrawVahta.GET_CHAR)
    else:
         await message.answer("You are not authorized.")

async def get_char(message: types.Message, state: FSMContext):
    await message.answer(f"Great. Char: {message.text}\n Now choose a row:")
    await state.update_data(char=message.text)
    await state.set_state(StatesDrawVahta.GET_ROW)

async def get_row(message: types.Message, state: FSMContext):
     await message.answer(f"OK. Row: {message.text}\nNow choose a column:")
     await state.update_data(row=message.text)
     await state.set_state(StatesDrawVahta.GET_COLUMN)
    
async def draw(message: types.Message, state: FSMContext):
    await message.answer(f"Got it. Column: {message.text}")
    context_data = await state.get_data()
    char = context_data.get("char")
    row = int(context_data.get("row"))
    column = int(message.text)
    await pillow_draw(char, row, column)
    await message.answer("Done. Use /vahta to check")
    await state.clear()


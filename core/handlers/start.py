from aiogram import types, Router
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start", "help"))
async def start_handler(message: types.Message):
    await message.answer(f"ало, {message.from_user.first_name}! я не знаю чим тобі допомогти")

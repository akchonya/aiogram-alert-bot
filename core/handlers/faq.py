from aiogram import types, Router
from aiogram.filters import Command

faq_router = Router()


@faq_router.message(Command("faq"))
async def start_handler(message: types.Message):
    await message.answer(f"https://telegra.ph/Dormitory-3-09-10")

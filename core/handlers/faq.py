"""
/faq sends a link to the FAQ article
"""


from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove


faq_router = Router()


@faq_router.message(Command("faq"))
async def faq_handler(message: types.Message):
    await message.answer(
        "https://telegra.ph/Dormitory-3-09-10", reply_markup=ReplyKeyboardRemove()
    )

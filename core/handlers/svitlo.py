"""
/faq sends a link to the FAQ article
"""


from aiogram import Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message


router = Router()


@router.message(Command("svitlo"))
async def svitlo_handler(message: Message):
    await message.answer(
        "https://telegra.ph/Dormitory-3-09-10", reply_markup=ReplyKeyboardRemove()
    )

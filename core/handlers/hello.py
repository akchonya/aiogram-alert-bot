"""
    answers "ні", "Ні", "нІ", "НІ"
"""


from aiogram import Router, F
from aiogram.types import ReplyKeyboardRemove, Message

router = Router()


@router.message(F.text == "ні")
async def hi_lower_handler(message: Message):
    await message.reply("неllo", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "НІ")
async def hi_upper_handler(message: Message):
    await message.reply("НЕLLO", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Ні")
async def hi_cap_handler(message: Message):
    await message.reply("Нello", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "нІ")
async def hi_crazy_handler(message: Message):
    await message.reply("нEllO", reply_markup=ReplyKeyboardRemove())

"""
Commands to send stickers to the chat
"""


from aiogram import types, Router
from aiogram.filters import Command
from random import randint

router = Router()


@router.message(Command("bunt"))
async def bunt_sticker(message: types.Message):
    await message.answer_sticker(
        sticker="CAACAgIAAxkBAAEYRLBjKfNf9QtXKpeiBrBcSp5BNP2rwAACKiEAAgnVUUlHhGyMxOT0wykE"
    )


@router.message(Command("rusoriz"))
async def rusorizt_sticker(message: types.Message):
    stickers = (
        "CAACAgIAAxkBAAEouIZlmyH78U-XzgbGxcVSZY8rykCLjAAC2xEAAheC6EjvAoFgb4_29jQE",
        "CAACAgIAAxkBAAEmExNlCHyRvioQXW0ipPfqt9SK1nxGfwACUDcAAggFQEhQ1W5cnK9FlzAE",
    )
    await message.answer_sticker(stickers[randint(0, 1)])


@router.message(Command("concert"))
async def concert_handler(message: types.Message):
    voice = types.FSInputFile("concert.ogg")
    await message.reply_voice(voice=voice, caption="💃🕺💃🕺💃🕺💃🕺💃🕺")

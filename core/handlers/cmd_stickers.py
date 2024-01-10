"""
Commands to send stickers to the chat
"""

import os
from random import randint

from aiogram import Router, types
from aiogram.filters import Command

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
    dir_path = "concert"
    number_of_files = len(
        [
            entry
            for entry in os.listdir(dir_path)
            if os.path.isfile(os.path.join(dir_path, entry))
        ]
    )

    voice = types.FSInputFile(f"concert/audio{randint(1, number_of_files)}.ogg")
    await message.answer_voice(voice=voice, caption="💃🕺💃🕺💃🕺💃🕺💃🕺")

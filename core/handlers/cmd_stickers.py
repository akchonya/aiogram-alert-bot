from aiogram import types, Router
from aiogram.filters import Command

bunt_sticker_router = Router()
rusoriz_sticker_router = Router()

@bunt_sticker_router.message(Command("bunt"))
async def bunt_sticker(message: types.Message):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEYRLBjKfNf9QtXKpeiBrBcSp5BNP2rwAACKiEAAgnVUUlHhGyMxOT0wykE")



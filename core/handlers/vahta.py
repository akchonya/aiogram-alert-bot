from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

vahta_router = Router()


@vahta_router.message(Command("vahta"))
async def vahta_handler(message: types.Message):
    photo = types.FSInputFile("pillow_bot/vahta.jpg")
    await message.answer_photo(photo=photo, caption="Прошу! Усе що знаю про графік наших (ваших) вахтерів:",
                               reply_markup=ReplyKeyboardRemove())



'''
/vahta sends a picture of watchmen's schedule to the chat 
'''


from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

vahta_router = Router()


@vahta_router.message(Command("vahta"))
async def vahta_handler(message: types.Message):
    photo = types.FSInputFile("pillow_bot/vahta.png")
    await message.answer_photo(photo=photo, caption="Прошу! Усе що знаю про графік наших (ваших) вахтерів:",
                               reply_markup=ReplyKeyboardRemove())

@vahta_router.message(F.text.casefold().contains("хто на вахті"))
async def vahta_text_handler(message: types.Message):
    photo = types.FSInputFile("pillow_bot/vahta.png")
    await message.answer_photo(photo=photo, caption="мені здалося, чи ви запитали хто на вахті? 🧐\n" +
                               "якщо так - тримайте ось графік вахтерів на сьогодні.\n\n" +
                               "а на майбутнє - користуйтеся /vahta")


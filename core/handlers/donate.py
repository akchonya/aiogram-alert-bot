"""
/donate sends donation details 
"""


from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove


donate_router = Router()


@donate_router.message(Command("donate"))
async def donate_handler(message: types.Message):
    await message.answer(
        "<b>Донати приймаються на карти:</b> "
        + "\nприват: 5168752084032468 \nмоно: 4441111136306531\n\n"
        + "шукайте себе на <a href='https://telegra.ph/doshka-poshani-LNU-Dorm-3-10-11'>дошці пошани</a> потім!",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )

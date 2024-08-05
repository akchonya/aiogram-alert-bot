"""
/start greets a user
/help sends a list of aavailable commands
"""

from aiogram import types, Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardRemove

from ..utils.config import ADMIN_IDS


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        f"<b>привіт, {html.unparse(message.from_user.first_name)} 😎</b>\n"
        + "я - ботік помічник для третього гурту лну.\n"
        + "можеш подивитися усі доступні команди в меню.\n\n"
        + f"якщо маєш питання чи пропозиції - <a href='tg://user?id={ADMIN_IDS[0]}'>звертайся</a>",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(
        f"<b>привіт, {message.from_user.first_name}!</b>\n\n"
        + "<b>ось список доступних команд:</b>\n"
        + "• /faq присилає корисну статтю\n"
        + "• /vahta - графік вахтерів\n"
        + "• /bunt i /rusoriz кидають відповідні стікери\n"
        + "• /weather_now i /weather_today показують погоду зараз і на сьогодні відповідно\n"
        + "• за допомогою /donate можеш підтримати розробницю бота\n\n"
        + f"якщо маєш питання чи пропозиції - <a href='tg://user?id={ADMIN_IDS[0]}'>звертайся</a>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )


empty_router = Router()


@empty_router.message()
async def empty():
    pass

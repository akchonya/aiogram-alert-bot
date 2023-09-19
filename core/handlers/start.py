from aiogram import types, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardRemove


start_router = Router()
help_router = Router()

@start_router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(f"<b>привіт, {message.from_user.first_name}!</b>\n" +
                         "я - ботік помічник для третього гурту лну.\n" +
                         "можеш подивитися усі доступні команди в меню.\n\n" +
                         "якщо маєш питання чи пропозиції - звертайся до @FleshkaXDude",
                         reply_markup=ReplyKeyboardRemove())

@help_router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(f"<b>привіт, {message.from_user.first_name}!</b>\n\n" +
                         "<b>ось список доступних команд:</b>\n" +
                         "• /faq присилає корисну статтю\n" +
                         "• /vahta - графік вахтерів\n" +
                         "• /bunt i /rusoriz кидають відповідні стікери\n" +
                         "• за допомогою /donate можеш підтримати розробницю бота\n\n" +
                         "якщо маєш питання чи пропозиції - звертайся до @FleshkaXDude",
                         parse_mode="HTML",
                         reply_markup=ReplyKeyboardRemove())

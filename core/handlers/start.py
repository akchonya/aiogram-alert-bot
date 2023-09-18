from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove


start_router = Router()

@start_router.message(Command("start", "help"))
async def start_handler(message: types.Message):
    await message.answer(f"<b>привіт, {message.from_user.first_name}!</b>\n" +
                         "я - ботік помічник для третього гурту лну.\n" +
                         "можеш подивитися усі доступні команди в меню.\n\n" +
                         "якщо маєш питання чи пропозиції - звертайся до @FleshkaXDude",
                         reply_markup=ReplyKeyboardRemove())

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message


router = Router()


@router.message(Command("sell"))
async def sell_handler(message: Message):
    print(message.chat.id)
    if message.chat.type == "private":
        await message.answer(
            "ок зараз будемо створювать..",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer("створити оголошення можна лише в пп у ботіка. ")

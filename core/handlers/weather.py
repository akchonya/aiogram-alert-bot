from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, F
from core.utils.config import OWM_API
from core.utils.async_weather import weather_now, weather_forecast

router = Router()


@router.message(Command("weather_now"))
async def now(message: Message):
    response = await weather_now(OWM_API)

    await message.answer(response)


@router.message(Command("weather_today"))
async def today(message: Message):
    response = await weather_forecast(OWM_API)
    await message.answer(response)


@router.message(F.text.casefold().contains("погод"))
async def weather_text_handler(message: Message):
    await now(message)

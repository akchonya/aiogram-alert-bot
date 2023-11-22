import logging
from datetime import datetime

import python_weather
from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp.client_exceptions import ClientConnectorError
from python_weather.enums import Locale


async def getweather():
    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(
        unit=python_weather.METRIC, locale=Locale.UKRAINIAN
    ) as client:
        # fetch a weather forecast from a city
        return await client.get("Lviv")


router = Router()


@router.message(Command("weather_now"))
async def weather_now_handler(message: Message):
    weather = await getweather()

    msg = (
        f"{html.bold('погода зараз')}:\n"
        f"🌡 {weather.current.temperature}°C (відчувається як {weather.current.feels_like}°C)\n"
        f"📝 {weather.current.description.lower()}\n\n"
    )

    await message.answer(msg)


@router.message(Command("weather_today"))
async def weather_today_handler(message: Message):
    try:
        weather = await getweather()
    except ClientConnectorError as e:
        logging.error(f"Error fetching weather: {e}")
        await message.answer("⚠️ сервер з погодою не відповідає, спробуйте пізніше")

    initial_msg = msg = f"{html.bold('прогноз на сьогодні:')}\n"
    forecast = [i for i in weather.forecasts][0]

    for i, hourly in enumerate(forecast.hourly):
        if datetime.now().time() < hourly.time:
            msg += "🔸🔹"[i % 2]
            msg += f" {html.bold('{:02d}:{:02d}'.format(hourly.time.hour, hourly.time.minute))}: {hourly.temperature}°C, {hourly.description.lower()}\n"

    if msg == initial_msg:
        msg += "🙄 нема вже шо прогрозувати, ви час бачили? до завтра!!"

    await message.answer(msg)


@router.message(F.text.casefold().contains("погод"))
async def weather_text_handler(message: Message):
    await weather_now_handler(message)

"""
/faq sends a link to the FAQ article
"""

from pytz import timezone
from datetime import datetime
from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message


time_periods = (
    "1:00-3:00",
    "3:00-5:00",
    "5:00-7:00",
    "7:00-9:00",
    "9:00-11:00",
    "11:00-13:00",
    "13:00-15:00",
    "15:00-17:00",
    "17:00-19:00",
    "19:00-21:00",
    "21:00-23:00",
    "23:00-1:00",
)

GREEN = 0
WHITE = 1
RED = 2

emojis = {0: "🟢", 1: "⚪", 2: "🔴"}

MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6

schedule = {
    MON: (
        GREEN,
        GREEN,
        WHITE,
        RED,
        GREEN,
        GREEN,
        GREEN,
        GREEN,
        WHITE,
        RED,
        GREEN,
        GREEN,
    ),
    TUE: (
        WHITE,
        RED,
        GREEN,
        GREEN,
        GREEN,
        GREEN,
        WHITE,
        RED,
        GREEN,
        GREEN,
        GREEN,
        GREEN,
    ),
    WED: (
        GREEN,
        GREEN,
        GREEN,
        GREEN,
        WHITE,
        RED,
        GREEN,
        GREEN,
        GREEN,
        GREEN,
        WHITE,
        RED,
    ),
    THU: (
        GREEN,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
    ),
    FRI: (
        RED,
        WHITE,
        GREEN,
        GREEN,
        GREEN,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
        GREEN,
        GREEN,
    ),
    SAT: (
        GREEN,
        GREEN,
        GREEN,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
        GREEN,
        GREEN,
        RED,
        WHITE,
    ),
    SUN: (
        GREEN,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
        GREEN,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
    ),
}


async def check_current_period(now, time_periods):
    now = now.time()

    def is_time_in_period(now, start_str, end_str):
        start = datetime.strptime(start_str, "%H:%M").time()
        end = datetime.strptime(end_str, "%H:%M").time()

        if start <= end:
            return start <= now < end
        else:
            # Handle the period that spans midnight
            return now >= start or now < end

    # Check which period the current time is in
    current_period = None
    for period in time_periods:
        start_str, end_str = period.split("-")
        if is_time_in_period(now, start_str, end_str):
            current_period = period
            break

    return current_period


router = Router()


@router.message(Command("faq"))
async def faq_handler(message: Message):
    await message.answer(
        "https://telegra.ph/Dormitory-3-09-10", reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("svitlo"))
async def svitlo_handler(message: Message):
    now = datetime.now(tz=timezone("Europe/Kiev"))

    time = await check_current_period(now, time_periods)

    time_index = time_periods.index(time)

    weekday = now.weekday()

    await message.answer(
        f"{emojis[schedule[weekday][time_index]]} {html.bold(f'{time}')}\n{html.link('актуальна інформація', 'https://telegra.ph/Dormitory-3-09-10#електрохарчування')}",
        disable_web_page_preview=True,
    )

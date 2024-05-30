"""
/faq sends a link to the FAQ article
"""

from datetime import datetime
from datetime import time as dtime

from pytz import timezone
from aiogram.enums import ParseMode
from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import (
    Message,
)


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

emojis = {GREEN: "🟢", WHITE: "⚪", RED: "🔴"}

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


schedule_2 = {
    MON: (
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
    TUE: (
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
    WED: (
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
    THU: (
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
    FRI: (
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
    SAT: (
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
    SUN: (
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


async def create_message(schedule, now, heading=None, footer=None, full=False):
    time = await check_current_period(now, time_periods)

    if full:
        time_index = -1
    else:
        time_index = time_periods.index(time)

    weekday = now.weekday()

    if full:
        weekday = (weekday + 1) % 7

    start_time = dtime(0, 0)  # 00:00
    end_time = dtime(1, 0)  # 01:00

    # Extract the current time's hour and minute
    if full:
        current_time = dtime(22, 0)
    else:
        current_time = now.time()

    # Check if the current time is within the range
    if start_time <= current_time < end_time:
        weekday = (weekday - 1) % 7

    if heading:
        text = f"{heading}\n➖➖➖➖➖➖➖➖➖\n"
    else:
        text = ""

    if not full:
        text += f"{emojis[schedule[weekday][time_index]]} {html.bold(f'{time}')}\n"

        text += "➖➖➖➖➖➖➖➖➖\n"

    for i_time in time_periods:
        empty = True
        i_time_index = time_periods.index(i_time)

        if i_time_index > time_index:
            text += f"{emojis[schedule[weekday][i_time_index]]} {f'{html.bold(time_periods[i_time_index])}'}\n"
            empty = False

    if not empty:
        text += "➖➖➖➖➖➖➖➖➖\n"

    if footer:
        text += f"{footer}"

    return text


router = Router()


@router.message(Command("faq"))
async def faq_handler(message: Message):
    await message.answer("https://telegra.ph/Dormitory-3-09-10")


@router.message(Command("svitlo"))
async def svitlo_handler(message: Message):
    now = datetime.now(tz=timezone("Europe/Kiev"))

    text = await create_message(
        schedule=schedule,
        now=now,
        heading=f"{html.bold('💡 група 3.2')}",
        footer=f"{html.link('ℹ️ актуальна інформація', 'https://t.me/svitlo_dorm3')}",
    )

    await message.answer(text=text, disable_web_page_preview=True)


@router.message(Command("svitlo2"))
async def svitlo2_handler(message: Message):
    now = datetime.now(tz=timezone("Europe/Kiev"))

    text = await create_message(
        schedule=schedule_2,
        now=now,
        heading=f"{html.bold('💧 група 2.2')}",
        footer=f"{html.link('ℹ️ актуальна інформація', 'https://t.me/svitlo_dorm3')}",
    )

    await message.answer(text=text, disable_web_page_preview=True)


@router.message(Command("next_svitlo"))
async def next_svitlo_handler(message: Message):
    now = datetime.now(tz=timezone("Europe/Kiev"))

    text = await create_message(
        schedule=schedule,
        now=now,
        heading=f"{html.bold('💡 графік групи 3.2 на завтра')}",
        footer=f"{html.link('ℹ️ актуальна інформація', 'https://t.me/svitlo_dorm3')}",
        full=True,
    )

    await message.answer(text=text, disable_web_page_preview=True)


@router.message(Command("next_svitlo2"))
async def next_svitlo2_handler(message: Message):
    now = datetime.now(tz=timezone("Europe/Kiev"))

    text = await create_message(
        schedule=schedule_2,
        now=now,
        heading=f"{html.bold('💧 графік групи 2.2 на завтра')}",
        footer=f"{html.link('ℹ️ актуальна інформація', 'https://t.me/svitlo_dorm3')}",
        full=True,
    )

    await message.answer(text=text, disable_web_page_preview=True)

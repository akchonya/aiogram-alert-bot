"""
/faq sends a link to the FAQ article
"""

from datetime import datetime, timedelta
from datetime import time as dtime

from pytz import timezone
from aiogram import Router, html, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message,
)

from core.utils.config import SVITLO_CHANNEL_ID

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
        WHITE,
        WHITE,
        RED,
        GREEN,
        GREEN,
        GREEN,
        WHITE,
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
        WHITE,
        WHITE,
        RED,
        GREEN,
        GREEN,
        GREEN,
        WHITE,
    ),
    WED: (
        GREEN,
        WHITE,
        GREEN,
        WHITE,
        WHITE,
        RED,
        GREEN,
        GREEN,
        GREEN,
        WHITE,
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
        WHITE,
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
        WHITE,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
        WHITE,
        GREEN,
    ),
    SAT: (
        WHITE,
        GREEN,
        WHITE,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
        WHITE,
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
        WHITE,
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
        WHITE,
        WHITE,
        RED,
        GREEN,
        GREEN,
        GREEN,
        WHITE,
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
        WHITE,
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
        WHITE,
        WHITE,
        RED,
        GREEN,
        GREEN,
        GREEN,
        WHITE,
    ),
    THU: (
        WHITE,
        GREEN,
        WHITE,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
        WHITE,
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
        WHITE,
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
        WHITE,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
        WHITE,
        GREEN,
    ),
    SUN: (
        WHITE,
        GREEN,
        WHITE,
        GREEN,
        RED,
        WHITE,
        GREEN,
        GREEN,
        WHITE,
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

    print(time_index)
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

    if time_index == 11:
        text = await create_message(
            schedule,
            now - timedelta(hours=2),
            heading=text + html.bold("📄 графік після 00:00"),
            full=True,
        )

    if footer:
        text += f"{footer}"

    return text


async def next_svitlo(chat_id: int, bot: Bot):
    now = datetime.now(tz=timezone("Europe/Kiev"))

    text = await create_message(
        schedule=schedule,
        now=now,
        heading=f"{html.bold('💡 графік групи 3.2 на завтра')}",
        footer=f"{html.link('ℹ️ актуальна інформація', 'https://t.me/svitlo_dorm3')}",
        full=True,
    )

    await bot.send_message(chat_id=chat_id, text=text, disable_web_page_preview=True)


async def next_svitlo2(chat_id: int, bot: Bot):
    now = datetime.now(tz=timezone("Europe/Kiev"))

    text = await create_message(
        schedule=schedule_2,
        now=now,
        heading=f"{html.bold('💧 графік групи 2.2 на завтра')}",
        footer=f"{html.link('ℹ️ актуальна інформація', 'https://t.me/svitlo_dorm3')}",
        full=True,
    )

    await bot.send_message(chat_id=chat_id, text=text, disable_web_page_preview=True)


router = Router()


@router.message(Command("faq"))
async def faq_handler(message: Message):
    await message.answer("https://telegra.ph/Dormitory-3-09-10")


@router.message(Command("svitlo"))
@router.message(Command("svitlo2"))
@router.message(Command("next_svitlo"))
@router.message(Command("next_svitlo2"))
async def svitlo(message: Message):
    text = f"{html.bold(html.link('ℹ️ актуальна інформація по світлу на день тут', 'https://t.me/svitlo_dorm3'))}\n\n⚠ {html.link(html.bold('тижневі графіки'), 'https://telegra.ph/Dormitory-3-09-10#%D0%B5%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D1%85%D0%B0%D1%80%D1%87%D1%83%D0%B2%D0%B0%D0%BD%D0%BD%D1%8F')} світла тимчасово не працюють"

    await message.answer(f"{text}", disable_web_page_preview=True)


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
async def next_svitlo_handler(message: Message, bot: Bot):
    await next_svitlo(chat_id=message.chat.id, bot=bot)


@router.message(Command("next_svitlo2"))
async def next_svitlo2_handler(message: Message, bot: Bot):
    await next_svitlo2(chat_id=message.chat.id, bot=bot)


@router.message(Command("next_post"))
async def next_handler(message: Message, bot: Bot):
    await next_svitlo(chat_id=SVITLO_CHANNEL_ID, bot=bot)
    await next_svitlo2(chat_id=SVITLO_CHANNEL_ID, bot=bot)

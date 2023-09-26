'''
A command that starts checking for alerts updates using Alerts in UA API
Accessed only by an admin
'''


import asyncio
import datetime
import logging

from os import getenv
from dotenv import load_dotenv
from alerts_in_ua import AsyncClient as AsyncAlertsClient
from aiogram import types, Router
from aiogram.filters import Command
from aiogram import Bot
from core.filters.basic import isAdmin


# Getting the admin id, dorm chat id and the api token from .env
load_dotenv()
ALERTS_TOKEN = getenv("ALERTS_TOKEN")
DORM_CHAT_ID = getenv("DORM_CHAT_ID")

alerts_router = Router()

@alerts_router.message(isAdmin(), Command("alerts"))
async def alerts_handler(message: types.Message, bot: Bot):
    # Setting a status variable
    lviv_status = "start"
    # msg is a variable to remember an id of pinned message to unpin it in the future
    msg = None
    while True:
        # Connent to the API
        alerts_client = AsyncAlertsClient(token=ALERTS_TOKEN)
        active_alerts = await alerts_client.get_air_raid_alert_statuses_by_oblast()
        # Get the Lviv status
        lviv = str([alert for alert in active_alerts if alert.location_title == "Львівська область"][0])[:-17]
        logging.info(lviv)
        print(lviv)

        # If status changed - send the message to admin 
        if lviv_status != lviv:
            lviv_status = lviv

            dt_now = datetime.datetime.now()
            formatted_date = f"{dt_now.year}-{dt_now.month}-{dt_now.day}|{dt_now.hour}:{dt_now.minute}:{dt_now.second}"

            await message.answer(f"[{formatted_date}] Alert update: {lviv}",
                                reply_markup=types.ReplyKeyboardRemove())
            # If there is an alert - send and pin the video, then send a corresponding message 
            if lviv == "active":
                msg = await bot.send_video(DORM_CHAT_ID, 
                                            video="BAACAgIAAxkBAAEmP_5lEKxi8qw07LBtzAZTZfRz9l-NxAACNx4AAmqumUr1ey8JH10sPDAE")
                await bot.pin_chat_message(DORM_CHAT_ID, msg.message_id, True)
                await bot.send_message(DORM_CHAT_ID, "🚨 <b>ТРИВОГА!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!</b>\n" +
                                    "ПАКУЙТЕ СМАКОЛИКИ І У СХОВИЩЕ \n\n" +
                                    "<tg-spoiler>або під ковдру на свій страх і ризик</tg-spoiler>", 
                                    parse_mode="HTML")
            # Else - unpin message if there is one
            else:
                if msg != None:
                    await bot.send_message(DORM_CHAT_ID, "✅ ВІДБІЙ ТРИВОГИ")
                    await bot.unpin_chat_message(DORM_CHAT_ID, msg.message_id)

        # Check for updates every 30 sec
        await asyncio.sleep(30)

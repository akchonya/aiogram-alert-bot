import asyncio
import datetime

from os import getenv
from dotenv import load_dotenv
from alerts_in_ua import AsyncClient as AsyncAlertsClient
from aiogram import types, Router
from aiogram.filters import Command
from aiogram import Bot

load_dotenv()
ALERTS_TOKEN = getenv("ALERTS_TOKEN")
DORM_CHAT_ID = getenv("DORM_CHAT_ID")

alerts_router = Router()

@alerts_router.message(Command("alerts"))
async def alerts_handler(message: types.Message, bot: Bot):
    zapor_status = "start"
    msg = None
    while True:
        alerts_client = AsyncAlertsClient(token=ALERTS_TOKEN)
        active_alerts = await alerts_client.get_air_raid_alert_statuses_by_oblast()
        zapor = str([alert for alert in active_alerts if alert.location_title == "Запорізька область"][0])[:-18]
        print(f"[{datetime.datetime.now()}] {zapor}")
        if zapor_status != zapor:
            zapor_status = zapor
            await message.answer(f"Update!! {zapor}")
            if zapor == "active":
                msg = await bot.send_video(DORM_CHAT_ID, 
                                video="BAACAgIAAxkBAAEmB3JlBgLAVXsNL-BTjEMPE6Pk4YBN_AACNx4AAmqumUr1ey8JH10sPDAE", 
                                caption="🚨 ТРИВОГА!!!!!")
                await bot.pin_chat_message(DORM_CHAT_ID, msg.message_id, True)
            else:
                if msg != None:
                    await bot.send_message(DORM_CHAT_ID, "✅ ВІДБІЙ ТРИВОГИ")
                    await bot.unpin_chat_message(DORM_CHAT_ID, msg.message_id)
            
        await asyncio.sleep(60)

"""
This example shows how to use webhook on behind of any reverse proxy (nginx, traefik, ingress etc.)
"""
import logging
import sys
from os import getenv
from dotenv import load_dotenv
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from core.handlers.start import start_router
from core.handlers.alerts import alerts_router
from core.handlers.faq import faq_router
from core.handlers.vahta import vahta_router
from core.handlers.draw_vahta import draw_vahta_router
from core.handlers.cmd_stickers import bunt_sticker_router, rusoriz_sticker_router
from core.handlers import update_vahta, msg_echo
from core.utils.statesvahta import StatesVahta
# from core.utils.statesdrawvahta import StatesDrawVahta
from core.utils.statesmsgecho import StatesMsgEcho


load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
BOT_TOKEN = getenv("BOT_TOKEN")

# Webserver settings
# bind localhost only to prevent any external access
WEB_SERVER_HOST = getenv("WEB_SERVER_HOST")
# Port for incoming request from reverse proxy. Should be any available port
WEB_SERVER_PORT = 8350

# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
# Secret key to validate requests from Telegram (optional)
WEBHOOK_SECRET = getenv("WEBHOOK_SECRET")
# Base URL for webhook will be used to generate webhook URL for Telegram,
# in this example it is used public DNS with HTTPS support
BASE_WEBHOOK_URL = getenv("BASE_WEBHOOK_URL")


async def on_startup(bot: Bot) -> None:
    # If you have a self-signed SSL certificate, then you will need to send a public
    # certificate to Telegram
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)


def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    dp.message.register(update_vahta.get_photo, Command(commands="update_vahta"))
    dp.message.register(update_vahta.save_photo, StatesVahta.GET_PHOTO)

    # dp.message.register(draw_vahta.get_cell, Command(commands="draw_vahta"))
    # dp.message.register(draw_vahta.get_char, StatesDrawVahta.GET_CHAR)
    # dp.message.register(draw_vahta.get_row, StatesDrawVahta.GET_ROW)
    # dp.message.register(draw_vahta.draw, StatesDrawVahta.GET_COLUMN)

    dp.message.register(msg_echo.get_msg, Command(commands="msg_echo"))
    dp.message.register(msg_echo.msg_echo, StatesMsgEcho.GET_MSG)

    dp.message.register(msg_echo.get_msg_pin, Command(commands="msg_echo_pin"))
    dp.message.register(msg_echo.msg_echo_pin, StatesMsgEcho.GET_MSG_PIN)

    # ... and all other routers should be attached to Dispatcher
    dp.include_router(start_router)
    dp.include_router(alerts_router)
    dp.include_router(faq_router)
    dp.include_router(vahta_router)
    dp.include_router(draw_vahta_router)
    dp.include_router(bunt_sticker_router)
    dp.include_router(rusoriz_sticker_router)
    
    

    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
import logging
import sys
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from core.handlers.start import start_router, help_router
from core.handlers.alerts import alerts_router, alerts_handler
from core.handlers.faq import faq_router
from core.handlers.vahta import vahta_router
from core.handlers.draw_vahta import draw_vahta_router
from core.handlers.update_vahta import update_vahta_router
from core.handlers.admin_panel import admin_panel_router
from core.handlers.cmd_stickers import bunt_sticker_router, rusoriz_sticker_router
from core.handlers.donate import donate_router
from core.handlers.msg_echo import msg_echo_router, msg_echo_pin_router
from core.handlers.new_member import new_member_router
from core.utils.commands import set_commands
from core.utils.config import BOT_TOKEN, WEB_SERVER_HOST, BASE_WEBHOOK_URL, WEBHOOK_SECRET



# Port for incoming request from reverse proxy. 
WEB_SERVER_PORT = 8443

# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
# Secret key to validate requests from Telegram (optional)


async def on_startup(bot: Bot) -> None:
    await set_commands(bot)
    # Set webhook 
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", 
                          secret_token=WEBHOOK_SECRET,
                          allowed_updates=["message", "chat_member"] # allow updates needed
                          )
    


def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()

    # ... and all other routers should be attached to Dispatcher
    dp.include_router(start_router)
    dp.include_router(alerts_router)
    dp.include_router(faq_router)
    dp.include_router(vahta_router)
    dp.include_router(bunt_sticker_router)
    dp.include_router(rusoriz_sticker_router)
    dp.include_router(admin_panel_router)
    dp.include_router(msg_echo_router)
    dp.include_router(msg_echo_pin_router)
    dp.include_router(donate_router)
    dp.include_router(new_member_router)
    dp.include_router(help_router)
    dp.include_router(update_vahta_router)
    dp.include_router(draw_vahta_router)

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
        secret_token=WEBHOOK_SECRET
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
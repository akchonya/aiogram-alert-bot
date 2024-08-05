import logging
import sys
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from core.middlewares.alina import AlinaMiddleware
from core.middlewares.ivan import IvanMiddleware
from core.handlers.start import router as start_router
from core.handlers.alerts import alerts_router
from core.handlers.faq import router as faq_router
from core.handlers.vahta import vahta_router
from core.handlers.draw_vahta import draw_vahta_router
from core.handlers.update_vahta import update_vahta_router
from core.handlers.admin_panel import admin_panel_router
from core.handlers.cmd_stickers import router as stickers_router
from core.handlers.donate import donate_router
from core.handlers.msg_echo import msg_echo_router, msg_echo_pin_router
from core.handlers.new_member import new_member_router
from core.handlers.hello import router as hello_router
from core.handlers.sell import router as sell_router
from core.handlers.weather import router as weather_router
from core.handlers.start import empty_router
from core.utils.commands import set_commands
from core.utils.config import (
    BOT_TOKEN,
    WEB_SERVER_HOST,
    BASE_WEBHOOK_URL,
    WEBHOOK_SECRET,
    WEB_SERVER_PORT,
)


# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
# Secret key to validate requests from Telegram (optional)


async def on_startup(bot: Bot) -> None:
    await set_commands(bot)
    # Set webhook
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET,
        allowed_updates=[
            "message",
            "chat_member",
            "callback_query",
            "channel_post",
        ],  # allow updates needed
    )


def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher(alert_status="no_alert")
    dp.message.middleware(AlinaMiddleware())
    dp.message.middleware(IvanMiddleware())
    # ... and all other routers should be attached to Dispatcher
    dp.include_routers(
        start_router,
        alerts_router,
        faq_router,
        vahta_router,
        stickers_router,
        admin_panel_router,
        msg_echo_router,
        msg_echo_pin_router,
        donate_router,
        new_member_router,
        update_vahta_router,
        draw_vahta_router,
        hello_router,
        weather_router,
        sell_router,
        empty_router,
    )

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
        dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET
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

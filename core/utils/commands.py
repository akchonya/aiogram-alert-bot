from os import getenv
from dotenv import load_dotenv

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat


load_dotenv()
ADMIN_ID = getenv("ADMIN_ID")

commands = [
        BotCommand(
            command="start",
            description="початок роботи"
        ),
        BotCommand(
            command="help",
            description="допомога наймолодшим"
        ),
        BotCommand(
            command="faq",
            description="корисна стаття"
        ),
        BotCommand(
            command="vahta",
            description="графік вахтерів"
        ),
        BotCommand(
            command="bunt",
            description="бунт"
        ),
        BotCommand(
            command="rusoriz",
            description="русоріз"
        ),
        BotCommand(
            command="donate",
            description="донати на підтримку бота"
        )
    ]

admin_commands = commands.append(
    BotCommand(
        command="draw_vahta",
        description="додати вахтера на графік"
    )
)

async def set_commands(bot: Bot):
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    await bot.set_my_commands(admin_commands, BotCommandScopeChat(int, ADMIN_ID.split(", ")))
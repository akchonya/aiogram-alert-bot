from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
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

    await bot.set_my_commands(commands, BotCommandScopeDefault())
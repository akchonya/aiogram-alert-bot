from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from core.utils.config import ADMIN_ID


ADMIN_ID = list(map(int, ADMIN_ID.split(", ")))
MODER = int(ADMIN_ID[1])
ADMIN = int(ADMIN_ID[0])

user_commands = [
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

moderator_commands = user_commands + [
        BotCommand(
            command="draw_vahta",
            description="додати вахтера на графік"
        )
    ]

admin_commands = user_commands + [
        BotCommand(
            command="admin_panel",
            description="admin_panel"
        )
    ]

async def set_commands(bot: Bot):
    await bot.set_my_commands(user_commands, BotCommandScopeDefault())
    await bot.set_my_commands(moderator_commands, scope=BotCommandScopeChat(chat_id=MODER))
    await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=ADMIN))

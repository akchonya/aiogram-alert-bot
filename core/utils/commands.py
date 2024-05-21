from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from core.utils.config import ADMIN_IDS


MODER = int(ADMIN_IDS[1])
ADMIN = int(ADMIN_IDS[0])

user_commands = [
    BotCommand(command="start", description="початок роботи"),
    BotCommand(command="help", description="допомога наймолодшим"),
    BotCommand(command="faq", description="корисна стаття"),
    BotCommand(command="vahta", description="графік вахтерів"),
    BotCommand(command="bunt", description="бунт"),
    BotCommand(command="rusoriz", description="русоріз"),
    BotCommand(command="donate", description="донати на підтримку бота"),
    BotCommand(command="weather_now", description="погода зараз"),
    BotCommand(command="weather_today", description="прогноз на сьогодні"),
    BotCommand(command="concert", description="без коментарів"),
    BotCommand(command="svyato", description="свята сьогодні"),
    BotCommand(command="svitlo", description="показати зону за графіком"),
    BotCommand(command="svitlo2", description="світло в 2.2 групі"),
]

moderator_commands = user_commands + [
    BotCommand(command="draw_vahta", description="додати вахтера на графік"),
    BotCommand(command="update_vahta", description="оновити фон вахти"),
]

admin_commands = user_commands + [
    BotCommand(command="admin_panel", description="admin_panel"),
]


async def set_commands(bot: Bot):
    await bot.set_my_commands(user_commands, BotCommandScopeDefault())
    await bot.set_my_commands(
        moderator_commands, scope=BotCommandScopeChat(chat_id=MODER)
    )
    await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=ADMIN))

"""
/start greets a user
/help sends a list of aavailable commands
"""

from aiogram import F, Bot, types, Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime, timedelta
from pytz import timezone
from ..utils.config import ADMIN_IDS
from core.utils.commands import user_commands, moderator_commands, admin_commands


router = Router()


# Collect all bot commands across scopes
COMMANDS = {
    cmd.command
    for cmd in (
        list(user_commands)
        + list(moderator_commands)
        + list(admin_commands)
    )
}


def is_real_command(text: str) -> bool:
    if not text or not text.startswith("/"):
        return False
    
    words = text.split()
    token = words[0]  # first word like /cmd@Bot
    token_wo_slash = token[1:]
    if "@" in token_wo_slash:
        base, botname = token_wo_slash.split("@", 1)
        # Only allow commands directed to this bot explicitly
        if botname != "DormitoryFAQBot":
            return False
    else:
        base = token_wo_slash
    
    # Check if command is valid
    if base not in COMMANDS:
        return False
    
    # If there are arguments, check if they contain lowercase
    if len(words) > 1:
        arguments = " ".join(words[1:])  # everything after the command
        if any(c.islower() for c in arguments):
            return False  # Mute if arguments contain lowercase
    
    return True


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        f"<b>привіт, {html.unparse(message.from_user.first_name)} 😎</b>\n"
        + "я - ботік помічник для третього гурту лну.\n"
        + "можеш подивитися усі доступні команди в меню.\n\n"
        + f"якщо маєш питання чи пропозиції - <a href='tg://user?id={ADMIN_IDS[0]}'>звертайся</a>",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(
        f"<b>привіт, {message.from_user.first_name}!</b>\n\n"
        + "<b>ось список доступних команд:</b>\n"
        + "• /faq присилає корисну статтю\n"
        + "• /vahta - графік вахтерів\n"
        + "• /bunt i /rusoriz кидають відповідні стікери\n"
        + "• /weather_now i /weather_today показують погоду зараз і на сьогодні відповідно\n"
        + "• за допомогою /donate можеш підтримати розробницю бота\n\n"
        + f"якщо маєш питання чи пропозиції - <a href='tg://user?id={ADMIN_IDS[0]}'>звертайся</a>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )


empty_router = Router()


@empty_router.message(F.dice, F.forward_date, F.chat.type == "supergroup")
async def forward_from(message: types.Message, bot: Bot):
    now = datetime.now()

    result = now + timedelta(hours=6)

    try:
        await bot.restrict_chat_member(
            message.chat.id,
            message.from_user.id,
            types.ChatPermissions(
                can_send_messages=False,
                can_send_audios=False,
                can_send_documents=False,
                can_send_photos=False,
                can_send_videos=False,
                can_send_video_notes=False,
                can_send_voice_notes=False,
                can_send_other_messages=False,
                can_send_polls=False,
            ),
            until_date=result,
        )
        await message.reply("😇 ви шо тут самі хитрі? мут х2")
    except Exception as e:
        print(e)


# @empty_router.message(
#     F.dice.emoji == "🎰", F.dice.value != 64, F.chat.type == "supergroup"
# )
# async def dice(message: types.Message, bot: Bot):
#     # Get the current datetime
#     now = datetime.now()

#     result = now + timedelta(hours=3)

#     try:~
#         await bot.restrict_chat_member(
#             message.chat.id,
#             message.from_user.id,
#             types.ChatPermissions(
#                 can_send_messages=False,
#                 can_send_audios=False,
#                 can_send_documents=False,
#                 can_send_photos=False,
#                 can_send_videos=False,
#                 can_send_video_notes=False,
#                 can_send_voice_notes=False,
#                 can_send_other_messages=False,
#                 can_send_polls=False,
#             ),
#             until_date=result,
#         )
#         await message.reply("📵 нєпавєзло.. спробуйте за три годинки, а поки в мутік!")
#     except Exception as e:
#         print(e)


# @empty_router.message(F.dice.emoji == "🎰", F.chat.type == "supergroup")
# async def dice_win(message: types.Message):
#     await message.reply("🍾 на годиннику шо 15 травня? звідки у нас тут переможець??")


@empty_router.message(F.via_bot)
@empty_router.message(F.dice)
async def dice_delete(message: types.Message):
    await message.delete()


@empty_router.message(F.chat.type == "supergroup")
async def caps_lock_day_handler(message: types.Message, bot: Bot):
    # Check if today is October 22nd
    tz = timezone("Europe/Kiev")
    current_time = datetime.now(tz)
    
    print(f"DEBUG: Current date: {current_time.month}/{current_time.day}")
    print(f"DEBUG: Message text: '{message.text}'")
    print(f"DEBUG: Message caption: '{message.caption}'")
    
    if current_time.month == 10 and current_time.day == 22:
        # Check both text and caption for lowercase
        text_to_check = None
        
        if message.text:
            is_cmd = is_real_command(message.text)
            print(f"DEBUG: Text is_real_command: {is_cmd}")
            if not is_cmd:
                text_to_check = message.text
        elif message.caption:
            is_cmd = is_real_command(message.caption)
            print(f"DEBUG: Caption is_real_command: {is_cmd}")
            if not is_cmd:
                text_to_check = message.caption
            
        print(f"DEBUG: text_to_check: '{text_to_check}'")
        if text_to_check:
            has_lower = any(c.islower() for c in text_to_check)
            print(f"DEBUG: has_lowercase: {has_lower}")
            
        if text_to_check and any(c.islower() for c in text_to_check):
            print("DEBUG: MUTING USER!")
            # Mute user for 1 hour
            mute_until = current_time + timedelta(hours=1)
            
            try:
                await bot.restrict_chat_member(
                    message.chat.id,
                    message.from_user.id,
                    types.ChatPermissions(
                        can_send_messages=False,
                        can_send_audios=False,
                        can_send_documents=False,
                        can_send_photos=False,
                        can_send_videos=False,
                        can_send_video_notes=False,
                        can_send_voice_notes=False,
                        can_send_other_messages=False,
                        can_send_polls=False,
                    ),
                    until_date=mute_until,
                )
                await message.reply("СЬОГОДНІ ДЕНЬ КАПС ЛОКУ. ХТО ПИШЕ ЛОВЕРКЕЙСОМ МУТ НА ГОДИНУ.")
            except Exception as e:
                print(f"Error muting user: {e}")


@empty_router.message(F.from_user.id == ADMIN_IDS[0], F.chat.type == "private")
async def empty(message: types.Message):
    await message.reply(message.html_text, parse_mode=None)

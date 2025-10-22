"""
Caps Lock Day Middleware
Mutes users for 1 hour if they write lowercase on October 22nd
"""

from datetime import datetime, timedelta
from pytz import timezone
from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher.middlewares import BaseMiddleware
from core.utils.commands import user_commands, moderator_commands, admin_commands


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


class CapsLockMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Only process messages
        if not isinstance(event, Message):
            return await handler(event, data)
        
        message = event
        
        # Only process supergroup messages
        if message.chat.type != "supergroup":
            return await handler(event, data)
        
        # Check if today is October 22nd
        tz = timezone("Europe/Kiev")
        current_time = datetime.now(tz)
        
        if current_time.month == 10 and current_time.day == 22:
            # Check both text and caption for lowercase
            text_to_check = None
            
            if message.text and not is_real_command(message.text):
                text_to_check = message.text
            elif message.caption and not is_real_command(message.caption):
                text_to_check = message.caption
                
            if text_to_check and any(c.islower() for c in text_to_check):
                # Get bot from data
                bot = data.get("bot")
                if not bot:
                    return await handler(event, data)
                
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
                    # If can't mute (admin), delete message and send admin message
                    print(f"Error muting user: {e}")
                    try:
                        await message.delete()
                        await message.answer("АДМІН ПИШЕ ЛОВЕРКЕЙСОМ???? НА МИЛО!!!!!!!!!")
                    except Exception as delete_error:
                        print(f"Error deleting message: {delete_error}")
                
                # Don't process further handlers
                return
        
        return await handler(event, data)

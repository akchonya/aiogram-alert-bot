from aiogram import F, Router

from aiogram.types import Message, ContentType


new_member_router = Router()

@new_member_router.chat_member(F.NEW_CHAT_MEMBERS)


async def new_member(message: Message):
        
        await message.answer(f"<b>привіт, {new_member}!</b>" +
                    "\n\nможеш подивитися список доступних команд " +
                    "в полі набору повідомлення. рекомендую /faq " +
                    "до прочитання.",
                    parse_mode="HTML")
        
        await message.answer(sticker="CAACAgEAAxkBAAEl4stk_3hElRTvbfzR3L9EhEBPnLhFHgACjQEAAnY3dj9reH69o4xWqTAE")
        

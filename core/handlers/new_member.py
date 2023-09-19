from aiogram import F, Router
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated


new_member_router = Router()

@new_member_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: ChatMemberUpdated):
        
        await event.answer(f"<b>привіт, {event.new_chat_member.user.first_name}!</b>" +
                    "\n\nможеш подивитися список доступних команд " +
                    "в полі набору повідомлення. рекомендую /faq " +
                    "до прочитання.",
                    parse_mode="HTML")

        await event.answer_sticker(sticker="CAACAgEAAxkBAAEl4stk_3hElRTvbfzR3L9EhEBPnLhFHgACjQEAAnY3dj9reH69o4xWqTAE")

        

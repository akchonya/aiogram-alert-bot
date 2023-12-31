from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from core.utils.config import ALINA_ID


class AlinaMiddleware(BaseMiddleware):
    def is_alina(self, event: Message) -> bool:
        return event.from_user.id == ALINA_ID

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not self.is_alina(event):
            return await handler(event, data)
        await event.answer(
            "❕ Аліна нарешті створила <a href='https://t.me/zakkarnb'>канал</a>, підписуйтеся",
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        return await handler(event, data)

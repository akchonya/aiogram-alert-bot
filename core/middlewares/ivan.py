from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from core.utils.config import IVAN_ID, IVAN_CHANNEL_ID


class IvanMiddleware(BaseMiddleware):
    def is_ivan(self, event: Message) -> bool:
        return event.from_user.id == IVAN_ID

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not self.is_ivan(event):
            return await handler(event, data)
        await event.forward(IVAN_CHANNEL_ID)
        return await handler(event, data)

"""
A filter to check whether user_id is in admin list
"""

from aiogram.types import Message
from aiogram.filters import Filter
from core.utils.config import ADMIN_IDS


class isAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMIN_IDS

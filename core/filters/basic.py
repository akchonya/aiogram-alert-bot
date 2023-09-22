'''
A filter to check whether user_id is in admin list
'''


from os import getenv
from dotenv import load_dotenv
from aiogram.types import Message
from aiogram.filters import Filter


load_dotenv()
ADMIN_ID = getenv("ADMIN_ID")


class isAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in list(map(int, ADMIN_ID.split(", ")))
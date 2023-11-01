'''
A command that shows an admin panel to an authorized user
'''


from aiogram import Router
from aiogram.filters import Command

from aiogram.types import (
    Message
)

from core.keyboards.admin_panel_kb import admin_panel_kb
from core.filters.basic import isAdmin


admin_panel_router = Router()

@admin_panel_router.message(isAdmin(), Command("admin_panel"))
async def admin_panel(message: Message):
    await message.answer(
        f"Hi, {message.from_user.first_name}! There is a list of admin commands:",
        reply_markup=admin_panel_kb
    )

        

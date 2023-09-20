'''
A command that shows an admin panel to an authorized user
'''


from aiogram import Router, F
from aiogram.filters import Command

from os import getenv
from dotenv import load_dotenv

from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)

from core.keyboards.admin_panel_kb import admin_panel_kb


# Get the admin id
load_dotenv()
ADMIN_ID = getenv("ADMIN_ID")

admin_panel_router = Router()

@admin_panel_router.message(Command("admin_panel"))
async def admin_panel(message: Message):
    # Check if it's actually admin 
    if message.from_user.id == int(ADMIN_ID):
        await message.answer(
            f"Hi, {message.from_user.first_name}! There is a list of admin commands:",
            reply_markup=admin_panel_kb
        )
    else:
        await message.answer(
            f"Hi, {message.from_user.first_name}! You are not authorized.",
            reply_markup=ReplyKeyboardRemove())
        

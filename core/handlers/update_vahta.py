from os import getenv
from dotenv import load_dotenv

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from core.utils.statesvahta import StatesVahta


load_dotenv()
ADMIN_ID = getenv("ADMIN_ID")


async def get_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer("Send a photo for vahta bg:")
        await state.set_state(StatesVahta.GET_PHOTO)
    else:
         await message.answer("You are not authorized.")

async def save_photo(message: types.Message, state: FSMContext, bot: Bot):
        if message.from_user.id == int(ADMIN_ID):
            fileID = message.photo[-1].file_id
            file_info = await bot.get_file(fileID)
            downloaded_file = await bot.download_file(file_info.file_path)

            with open("pillow_bot/vahta.jpg", 'wb') as new_file:
                new_file.write(downloaded_file.getvalue())

            await message.answer("Done. Use /vahta to check")
            await state.clear()
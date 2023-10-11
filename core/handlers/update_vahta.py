'''
/update_vahta is for changing the bg pic of /draw_vahta's pillow_bot function
'''


from os import getenv
from dotenv import load_dotenv

from aiogram import types, Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from core.utils.statesvahta import StatesVahta
from core.filters.basic import isAdmin


# Setting  the function and FSM
async def get_photo(message: types.Message, state: FSMContext):
    # Checking for admin's id 
    if message.from_user.id == 257750513:
        await message.answer("Send a photo for vahta bg or /cancel to cancel.",
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(StatesVahta.GET_PHOTO)
    else:
         await message.answer("You are not authorized.")

async def save_photo(message: types.Message, state: FSMContext, bot: Bot):
        if message.from_user.id == 257750513:
            current_state = await state.get_state()
        
            # A cancel option
            if message.text in ("/cancel", "cancel"):
                if current_state is None:
                    return

                await state.clear()
                await message.answer("/update_vahta is canceled.")
                return

            # Saving the picture locally 
            fileID = message.photo[-1].file_id
            file_info = await bot.get_file(fileID)
            downloaded_file = await bot.download_file(file_info.file_path)

            with open("pillow_bot/vahta.jpg", 'wb') as new_file:
                new_file.write(downloaded_file.getvalue())

            # Sending admin a success message 
            await message.answer("Done. Use /vahta to check")
            await state.clear()


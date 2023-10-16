'''
/update_vahta is for changing the bg pic of /draw_vahta's pillow_bot function
'''

from aiogram import types, Bot, Router, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from core.utils.statesvahta import StatesVahta
from core.filters.basic import isAdmin
from aiogram.filters import Command


update_vahta_router = Router()


@update_vahta_router.message(isAdmin(), Command("update_vahta"))
async def get_photo(message: types.Message, state: FSMContext):
    await message.answer("Send a photo for vahta bg or /cancel to cancel.",
                            reply_markup=ReplyKeyboardRemove())
    await state.set_state(StatesVahta.GET_PHOTO)

# A cancelation option
@update_vahta_router.message(isAdmin(), StatesVahta.GET_PHOTO, Command("cancel"))
@update_vahta_router.message(isAdmin(), StatesVahta.GET_PHOTO, F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "/update_vahta is cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

@update_vahta_router.message(StatesVahta.GET_PHOTO)
async def save_photo(message: types.Message, state: FSMContext, bot: Bot):
        # Saving the picture locally 
        fileID = message.photo[-1].file_id
        file_info = await bot.get_file(fileID)
        downloaded_file = await bot.download_file(file_info.file_path)

        with open("pillow_bot/vahta.png", 'wb') as new_file:
            new_file.write(downloaded_file.getvalue())

        # Sending admin a success message 
        await message.answer("Done. Use /vahta to check")
        await state.clear()


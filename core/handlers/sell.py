from aiogram import Router, F, Bot, html
from aiogram.fsm.context import FSMContext
from core.utils.states import StatesSell as States
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardRemove,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from core.utils.config import DORM_CHAT_ID, ADMIN_IDS
from aiogram_album.ttl_cache_middleware import TTLCacheAlbumMiddleware
from aiogram_album import AlbumMessage
from core.keyboards.sell_ikb import user_ikb, admin_ikb, AdminAction, Action, UserAction
from aiogram.types.callback_query import CallbackQuery


router = Router()
TTLCacheAlbumMiddleware(router=router)

MAIN_ADMIN_ID = ADMIN_IDS[0]


@router.message(Command("sell"))
async def sell_handler(message: Message, state: FSMContext):
    print(message.chat.id)
    if message.chat.type == "private":
        await message.answer(
            "ок зараз будемо створювать. відправте постік або натисніть /cancel",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(States.GET_ADVERT)
    else:
        await message.answer("створити оголошення можна лише в пп у ботіка. ")


@router.message(Command("cancel"), States.GET_ADVERT)
@router.message(F.text.casefold() == "cancel", States.GET_ADVERT)
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("відмінено!! можете спробувати ще раз через /sell")


@router.message(States.GET_ADVERT, F.media_group_id)
async def media_group_handler(message: AlbumMessage):
    await message.answer("наразі можна доєднати лише одну картинку, спробуйте ще раз.")


# TODO
# send it to an admin for confirmation
@router.message(States.GET_ADVERT)
async def get_advert_handler(message: Message, state: FSMContext, bot: Bot):
    ikb = await admin_ikb(message.from_user.id)

    try:
        # Send a copy of the received message
        text = f"нове оголошення від {html.bold(html.unparse(message.from_user.full_name))} (@{message.from_user.username}):"
        await bot.send_message(MAIN_ADMIN_ID, text=text)
        await message.send_copy(chat_id=MAIN_ADMIN_ID, reply_markup=ikb)
        await message.answer("оголошення відправлено на затвердження")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("шось пішло у вас не так. відправте якось інакше..")
        return

    await state.clear()


@router.callback_query(AdminAction.filter(F.action == Action.accept))
async def accept_handler(query: CallbackQuery, callback_data: AdminAction):
    ikb = await user_ikb(callback_data.user_id)
    await query.message.send_copy(DORM_CHAT_ID, reply_markup=ikb)
    await query.answer()


@router.callback_query(AdminAction.filter(F.action == Action.decline))
async def decline_handler(
    query: CallbackQuery, callback_data: AdminAction, state: FSMContext
):
    await query.message.answer("напишіть причину відмови:")
    await state.update_data(user_id=callback_data.user_id)
    await state.set_state(States.CONFIRM)
    await query.answer()


@router.message(States.CONFIRM)
async def confirm_handler(message: Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    user_id = int(context_data.get("user_id"))
    text = f"ваше оголошення відхилено! причина: \n\n{message.text}"
    await bot.send_message(chat_id=user_id, text=text)
    await state.clear()


@router.callback_query(UserAction.filter())
async def delete_handler(query: CallbackQuery, callback_data: UserAction):
    if callback_data.user_id == query.from_user.id:
        await query.message.delete()

    else:
        await query.answer("ви не власник оголошення")

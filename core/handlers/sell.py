from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from core.utils.states import StatesSell as States
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardRemove,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from core.utils.config import DORM_CHAT_ID


async def delete_ikb(id: int):
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="видалити ❌",
                    callback_data=f"{id}",
                )
            ]
        ]
    )

    return ikb


router = Router()


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
    await message.answer("/msg_echo is cancelled.")


@router.message(States.GET_ADVERT, F.media_group_id)
async def media_group_handler(message: Message):
    # TODO
    pass


# TODO
# send it to an admin for confirmation
@router.message(States.GET_ADVERT)
async def get_advert_handler(message: Message, state: FSMContext):
    ikb = await delete_ikb(message.from_user.id)

    try:
        # Send a copy of the received message
        msg = await message.send_copy(chat_id=message.from_user.id, reply_markup=ikb)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer(
            "вибачте шось пішло у вас не так. відправте якось інакше.."
        )

    await state.clear()

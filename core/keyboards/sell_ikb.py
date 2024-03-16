from enum import Enum
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
)
from aiogram.filters.callback_data import CallbackData


class Action(str, Enum):
    accept = "✔"
    decline = "❌"


class AdminAction(CallbackData, prefix="adm"):
    action: Action
    user_id: int


class UserAction(CallbackData, prefix="user"):
    user_id: int


async def admin_ikb(user_id: int):
    builder = InlineKeyboardBuilder()
    for action in Action:
        builder.button(
            text=action.value, callback_data=AdminAction(action=action, user_id=user_id)
        )
    return builder.as_markup()


async def user_ikb(user_id: int):
    builder = InlineKeyboardBuilder()
    # TODO
    # something about privated users........
    builder.button(text="📞 зв'язатися", url=f"tg://user?id={user_id}")
    builder.button(
        text="❌ видалити оголошення", callback_data=UserAction(user_id=user_id)
    )

    return builder.as_markup()

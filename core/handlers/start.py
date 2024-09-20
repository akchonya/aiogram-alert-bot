"""
/start greets a user
/help sends a list of aavailable commands
"""

from aiogram import F, Bot, types, Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime, timedelta
from ..utils.config import ADMIN_IDS


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        f"<b>привіт, {html.unparse(message.from_user.first_name)} 😎</b>\n"
        + "я - ботік помічник для третього гурту лну.\n"
        + "можеш подивитися усі доступні команди в меню.\n\n"
        + f"якщо маєш питання чи пропозиції - <a href='tg://user?id={ADMIN_IDS[0]}'>звертайся</a>",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(
        f"<b>привіт, {message.from_user.first_name}!</b>\n\n"
        + "<b>ось список доступних команд:</b>\n"
        + "• /faq присилає корисну статтю\n"
        + "• /vahta - графік вахтерів\n"
        + "• /bunt i /rusoriz кидають відповідні стікери\n"
        + "• /weather_now i /weather_today показують погоду зараз і на сьогодні відповідно\n"
        + "• за допомогою /donate можеш підтримати розробницю бота\n\n"
        + f"якщо маєш питання чи пропозиції - <a href='tg://user?id={ADMIN_IDS[0]}'>звертайся</a>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )


empty_router = Router()

@empty_router.message(
    F.dice, F.forward_from, F.chat.type == "supergroup"
)
async def forward_from(message: types.Message, bot: Bot):
    now = datetime.now()

    result = now + timedelta(hours=6)

    try:
        await bot.restrict_chat_member(
            message.chat.id,
            message.from_user.id,
            types.ChatPermissions(
                can_send_messages=False,
                can_send_audios=False,
                can_send_documents=False,
                can_send_photos=False,
                can_send_videos=False,
                can_send_video_notes=False,
                can_send_voice_notes=False,
                can_send_other_messages=False,
                can_send_polls=False,
            ),
            until_date=result,
        )
        await message.reply("😇 ви шо тут самі хитрі? мут х2")
    except Exception as e:
        print(e)


@empty_router.message(
    F.dice.emoji == "🎰", F.dice.value != 64, F.chat.type == "supergroup"
)
async def dice(message: types.Message, bot: Bot):
    # Get the current datetime
    now = datetime.now()

    result = now + timedelta(hours=3)

    try:
        await bot.restrict_chat_member(
            message.chat.id,
            message.from_user.id,
            types.ChatPermissions(
                can_send_messages=False,
                can_send_audios=False,
                can_send_documents=False,
                can_send_photos=False,
                can_send_videos=False,
                can_send_video_notes=False,
                can_send_voice_notes=False,
                can_send_other_messages=False,
                can_send_polls=False,
            ),
            until_date=result,
        )
        await message.reply("📵 нєпавєзло.. спробуйте за три годинки, а поки в мутік!")
    except Exception as e:
        print(e)


@empty_router.message(F.dice.emoji == "🎰", F.chat.type == "supergroup")
async def dice_win(message: types.Message):
    await message.reply("🍾 на годиннику шо 15 травня? звідки у нас тут переможець??")


# @empty_router.message()
# async def empty():
#     pass

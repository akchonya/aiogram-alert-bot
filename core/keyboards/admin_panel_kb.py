from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)


admin_panel_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="/update_vahta"),
        KeyboardButton(text="/draw_vahta")
        ],
    [
        KeyboardButton(text="/msg_echo"),
        KeyboardButton(text="/msg_echo_pin")
    ],
    [
        KeyboardButton(text="/alerts")
    ]
],
resize_keyboard=True)
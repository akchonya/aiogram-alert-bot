from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)


vahta_chars_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="biblio"),
        KeyboardButton(text="commie")
        ],
    [
        KeyboardButton(text="diana"),
        KeyboardButton(text="eblan")
    ],
    [
        KeyboardButton(text="lyarva")
    ],
],
resize_keyboard=True
)

vahta_rows_kb = ReplyKeyboardMarkup(keyboard=[
    KeyboardButton(text="1"),
    KeyboardButton(text="2"),
    KeyboardButton(text="3"),
    KeyboardButton(text="4"),
    KeyboardButton(text="5"),
    KeyboardButton(text="6")
],
resize_keyboard=True)

vahta_columns_kb = ReplyKeyboardMarkup(keyboard=[
    KeyboardButton(text="1"),
    KeyboardButton(text="2"),
    KeyboardButton(text="3"),
    KeyboardButton(text="4"),
    KeyboardButton(text="5"),
    KeyboardButton(text="6"),
    KeyboardButton(text="7")
],
resize_keyboard=True)
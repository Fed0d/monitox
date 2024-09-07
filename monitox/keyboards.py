from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_texts = {
    "start_dialog": "Начать диалог 🚀",
    "stop_dialog": "Завершить диалог 🛑",
    "help": "Помощь ❓",
}

start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=button_texts["start_dialog"])],
        [KeyboardButton(text=button_texts["help"])],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню.",
)

stop_dialog = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=button_texts["stop_dialog"])]],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню.",
)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Да ✅"), KeyboardButton(text="Нет ❌")]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True)

    return keyboard
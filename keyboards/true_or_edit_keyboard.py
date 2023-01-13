from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Верно ✅"), KeyboardButton(text="Изменить ✍️")]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True)

    return keyboard
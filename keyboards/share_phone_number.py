from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Поделиться ☏", request_contact=True), KeyboardButton(text="Не делиться ❌")]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True)

    return keyboard
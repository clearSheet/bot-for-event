from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Настройка квиза"), KeyboardButton(text="Стенд️")],
        [KeyboardButton(text="Инф. о пользователях")]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True)

    return keyboard
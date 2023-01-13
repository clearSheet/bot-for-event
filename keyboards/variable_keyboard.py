from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard(var1, var2, var3, var4) -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=var1), KeyboardButton(text=var2)],
        [KeyboardButton(text=var3), KeyboardButton(text=var4)]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True)

    return keyboard
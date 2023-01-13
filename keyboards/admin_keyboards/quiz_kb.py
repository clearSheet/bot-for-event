from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# def keyboard() -> ReplyKeyboardMarkup:
#     kb = [
#         [KeyboardButton(text="Добавить вопрос"), KeyboardButton(text="Отобразить вопросы")],
#         [KeyboardButton(text="Удалить вопросы квиза")]
#     ]
#
#     keyboard = ReplyKeyboardMarkup(keyboard=kb,
#                                    resize_keyboard=True)
#
#     return keyboard


def edit_quiz() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text='Добавить вопрос'), KeyboardButton(text='Просмотреть вопросы')],
        [KeyboardButton(text='Удалить вопросы')]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True)

    return keyboard
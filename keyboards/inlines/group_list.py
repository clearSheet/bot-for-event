from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup


def keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text='Первая группа', url='123.com')]
    ]

    return kb

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup


# def keyboard(var1, var2, var3, var4) -> InlineKeyboardMarkup:
#     kb = [
#         [InlineKeyboardButton(text=var1, callback='var1'), InlineKeyboardButton(text=var2, callback='var2')],
#         [InlineKeyboardButton(text=var3, callback='var3'), InlineKeyboardButton(text=var4, callback='var4')],
#         [InlineKeyboardButton(text='Отменить', callback='cancel')]
#     ]
#
#     return kb

def keyboard(var1, var2, var3, var4, question_num):
    builder = InlineKeyboardBuilder()

    prefx = 'question_' + str(question_num) + '_'

    # builder.row(InlineKeyboardButton(text=var1, callback_data=f'{prefx}var1'),
    #             InlineKeyboardButton(text=var2, callback_data=f'{prefx}var2'))
    #
    # builder.row(InlineKeyboardButton(text=var3, callback_data=f'{prefx}var3'),
    #             InlineKeyboardButton(text=var4, callback_data=f'{prefx}var4'))

    builder.row(InlineKeyboardButton(text=var1, callback_data=f'{prefx}var1'))

    builder.row(InlineKeyboardButton(text=var2, callback_data=f'{prefx}var2'))

    builder.row(InlineKeyboardButton(text=var3, callback_data=f'{prefx}var3'))

    builder.row(InlineKeyboardButton(text=var4, callback_data=f'{prefx}var4'))


    builder.row(InlineKeyboardButton(text='Отменить', callback_data='cancel_quiz'))


    return builder.as_markup()


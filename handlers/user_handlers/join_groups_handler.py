from random import randint

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import FSInputFile
from aiogram import types


from aiogram import Router, types
from aiogram.types import Message

from keyboards.inlines import group_list


router = Router()

builder = InlineKeyboardBuilder()
builder.row(InlineKeyboardButton(text="Telegram-канал Test IT", url="https://t.me/testit_tms"))
builder.row(InlineKeyboardButton(text="Telegram-канал TeamStorm", url="https://t.me/teamstorm_io"))
builder.row(InlineKeyboardButton(text="Проверить вступление в группы", callback_data="check_subscribe"))


@router.message(text='👥 Вступить в группы')
async def show_rules_of_event(message: Message):
    await message.answer('Список в группы для вступления', reply_markup=builder.as_markup())


@router.callback_query(text="check_subscribe")
async def send_random_value(callback: types.CallbackQuery):
    # await callback.message.answer('Сообщение о проверки вступил ли пользователь в группы')
    from bot import bot
    from bot import db

    # Первая
    user_channel_status = await bot.get_chat_member(
        chat_id=-1001494347823,
        user_id=callback.from_user.id
    )

    if user_channel_status.status == 'member':
        await callback.message.answer('Вы вступили в группу Test IT! ✅')
        await db.edit_status_group_test_it(
            user_id=str(callback.from_user.id),
            status=1
        )
    else:
        await callback.message.answer('Пока вы еще не в группе Test IT! ❌')
        await db.edit_status_group_test_it(
            user_id=str(callback.from_user.id),
            status=0
        )

    # Вторая
    user_channel_status = await bot.get_chat_member(
        chat_id=-1001642376655,
        user_id=callback.from_user.id
    )

    if user_channel_status.status == 'member':
        await callback.message.answer('Вы вступили в группу TeamStorm! ✅')
        await db.edit_status_group_teamstorm(
            user_id=str(callback.from_user.id),
            status=1
        )

    else:
        await callback.message.answer('Пока вы еще не в группе TeamStorm! ❌')
        await db.edit_status_group_teamstorm(
            user_id=str(callback.from_user.id),
            status=0
        )

    user_info1 = await db.get_one_user_info(callback.from_user.id)
    user_info1 = user_info1[0]
    review1 = user_info1[7]
    user_lvl1 = user_info1[9]
    email1 = user_info1[10]
    post_path1 = user_info1[12]
    friends_count1 = user_info1[14]
    in_test_it1 = user_info1[15]
    in_teamstorm1 = user_info1[16]
    quiz_status1 = user_info1[17]

    answer = 'Поздравляем с получением нового уровня!'
    photo = FSInputFile(f'data/users_lvl_presets/{user_lvl1}_level.jpg')

    if in_test_it1 == 1 and friends_count1 >= 2 and user_lvl1 == 0:
        await db.lvl_up_user(callback.from_user.id)
        await callback.message.answer_photo(photo=photo, caption=answer)
    if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 4 and user_lvl1 == 1:
        await db.lvl_up_user(callback.from_user.id)
        await callback.message.answer_photo(photo=photo, caption=answer)
    if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 6 and user_lvl1 == 2 and quiz_status1 == 1 and post_path1 and email1:
        await db.lvl_up_user(callback.from_user.id)
        await callback.message.answer_photo(photo=photo, caption=answer)
    if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 8 and user_lvl1 == 3 and quiz_status1 == 1 and post_path1 and email1 and review1:
        await db.lvl_up_user(callback.from_user.id)
        await callback.message.answer_photo(photo=photo, caption=answer)

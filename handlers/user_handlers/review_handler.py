from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards import true_or_edit_keyboard, main_working
from keyboards.inlines import back_to_main_menu


router = Router()

builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text="Отправить отзыв", callback_data="send_review")
)


class Get_Review(StatesGroup):
    get_review = State()
    confirm_review = State()
    get_email = State()
    confirm_email = State()


@router.message(text='✍️ Написать отзыв')
async def show_rules_of_event(message: Message, state: FSMContext):
    await message.answer("Нам будет полезно и приятно прочитать отзыв о работе нашей команды. "
                         "Присылай свои впечатления от общения с нами или о компании в целом.\n\n"
                         "Например: «Было интересно пообщаться! Ребята на стенде рассказали о "
                         "крутых фишках системы» или «Ваши штормовые игры — это нечто!"
                         " Хочу больше игр».",
                         reply_markup=builder.as_markup())


@router.callback_query(text='send_review')
async def get_review(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        'Отправьте свой отзыв в текстовом поле ниже 👇🏻',
        reply_markup=back_to_main_menu.keyboard()
    )

    await state.set_state(Get_Review.get_review)


@router.message(Get_Review.get_review)
async def confirm(message: Message, state: FSMContext):
    await state.update_data(review=message.text)

    await message.answer(
        f'Твой отзыв будет выглядеть вот так:\n\n'
        f'{message.text}\n\n'
        f'Все верно?',
        reply_markup=true_or_edit_keyboard.keyboard()
    )

    await state.set_state(Get_Review.confirm_review)


@router.message(Get_Review.confirm_review)
async def confirm_review(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        from bot import db

        await message.answer('Большое спасибо за отзыв!',
                             reply_markup=main_working.keyboard())

        data = await state.get_data()
        review = data['review']

        await db.add_review(
            review=review,
            user_id=message.from_user.id
        )

        await state.clear()

        # ____----____----____----____----____----____----____----____----____----
        from bot import db

        user_info1 = await db.get_one_user_info(message.from_user.id)
        user_info1 = user_info1[0]
        review1 = user_info1[7]
        user_lvl1 = user_info1[9]
        email1 = user_info1[10]
        post_path1 = user_info1[12]
        friends_count1 = user_info1[14]
        in_test_it1 = user_info1[15]
        in_teamstorm1 = user_info1[16]
        quiz_status1 = user_info1[17]

        if in_test_it1 == 1 and friends_count1 >= 2 and user_lvl1 == 0:
            await db.lvl_up_user(message.from_user.id)
            await message.answer('Поздравляем с получением нового уровня!')

        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 4 and user_lvl1 == 1:
            await db.lvl_up_user(message.from_user.id)
            await message.answer('Поздравляем с получением нового уровня!')

        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 6 and user_lvl1 == 2 and quiz_status1 == 1 and post_path1 and email1:
            await db.lvl_up_user(message.from_user.id)
            await message.answer('Поздравляем с получением нового уровня!')

        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 8 and user_lvl1 == 3 and quiz_status1 == 1 and post_path1 and review1:
            await db.lvl_up_user(message.from_user.id)
            await message.answer('Поздравляем с получением нового уровня!')
        # ____----____----____----____----____----____----____----____----____----

    elif message.text == "Изменить ✍️":
        await message.answer('Пожалуйста введи корректный отзыв 👇',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(Get_Review.get_review)
    else:
        await message.answer('Пожалуйста используйте клавиатуру для ответа 👇',
                             reply_markup=true_or_edit_keyboard.keyboard())
        await state.set_state(Get_Review.confirm_review)





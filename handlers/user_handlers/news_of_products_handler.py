from aiogram import Router, types
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters import Text


from keyboards import true_or_edit_keyboard, main_working
from keyboards.inlines import back_to_main_menu


router = Router()

builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text="Test IT", callback_data="news_test_it"),
    InlineKeyboardButton(text="TeamStorm", callback_data="news_team_storm")
)

builder.row(
    InlineKeyboardButton(text="Оба продукта", callback_data="news_oba"),
    InlineKeyboardButton(text="Не хочу получать рассылок", callback_data="news_no")
)


class GetNews(StatesGroup):
    get_email = State()
    confirm_email = State()

    get_category = State()
    confirm_category = State()


@router.message(text='📲 Новости по продуктам')
async def show_rules_of_event(message: Message, state: FSMContext):
    await message.answer('Новости по каким продуктам тебе были бы интересны?',
                         reply_markup=builder.as_markup())


@router.callback_query(Text(text_startswith="news_"))
async def get_category(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    if answer == 'news_test_it':
        await state.update_data(category='news_test_it')

        await state.set_state(GetNews.get_email)
        await callback.message.answer('Спасибо за интерес к нашим продуктам!\n'
                                      'Отправь свой email, что мы могли прислать '
                                      'тебе подборку новостных материалов и статей.\n'
                                      'P.S. И никакого спама!',
                                      reply_markup=back_to_main_menu.keyboard())
    elif answer == 'news_team_storm':
        await state.update_data(category='news_team_storm')

        await state.set_state(GetNews.get_email)
        await callback.message.answer('Спасибо за интерес к нашим продуктам!\n'
                                      'Отправь свой email, что мы могли прислать '
                                      'тебе подборку новостных материалов и статей.\n'
                                      'P.S. И никакого спама!',
                                      reply_markup=back_to_main_menu.keyboard())
    elif answer == 'news_oba':
        await state.update_data(category='news_team_storm and news_test_it')

        await state.set_state(GetNews.get_email)
        await callback.message.answer('Спасибо за интерес к нашим продуктам!\n'
                                      'Отправь свой email, что мы могли прислать '
                                      'тебе подборку новостных материалов и статей.\n'
                                      'P.S. И никакого спама!',
                                      reply_markup=back_to_main_menu.keyboard())
    else:
        await callback.message.answer('Если захочешь получать наши сообщения - возвращайся!',
                                         reply_markup=main_working.keyboard())

        await state.clear()


@router.message(GetNews.get_email)
async def get_email(message: Message, state: FSMContext):
    if '@' in message.text:
        await message.answer(
            f'Ты указал\n\n'
            f'{message.text}\n\n'
            f'В качестве Email-дреса, верно',
            reply_markup=true_or_edit_keyboard.keyboard()
        )

        await state.update_data(email=message.text)
        await state.set_state(GetNews.confirm_email)
    else:
        await message.answer(
            text='Пожалуйста отправь Email в корректном формате, что бы получать наши новости',
            reply_markup=back_to_main_menu.keyboard()
        )
        await state.set_state(GetNews.get_email)


@router.message(GetNews.confirm_email)
async def confirm_email(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        from bot import db

        data = await state.get_data()
        category = data['category']
        email = data['email']

        await db.add_email_and_category(
            user_id=message.from_user.id,
            email=email,
            category=category
        )
        await state.clear()
        await message.answer('Отлично, мы сохранили данные 🔥', reply_markup=main_working.keyboard())

    elif message.text == 'Изменить ✍️':
        await message.answer('Отправь корректный Email, на который мы будем отправлять новости!')
        await state.set_state(GetNews.get_email)
    else:
        await message.answer('Пожалуйста используй клавиатуру для ответа',
                             reply_markup=true_or_edit_keyboard.keyboard())
        await state.set_state(GetNews.confirm_email)

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



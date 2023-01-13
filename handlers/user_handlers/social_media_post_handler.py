from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards import main_working

router = Router()

class GetScreen(StatesGroup):
    get_screen_state = State()


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text="Отправить скриншот", callback_data="post_screen")
)

cancel_key = InlineKeyboardBuilder()
cancel_key.row(
    InlineKeyboardButton(text="Отменить отправку", callback_data="post_cancel")
)


@router.message(text='#️⃣ Пост в соц. сетях')
async def show_rules_of_event(message: Message):
    await message.answer('Опубликуй пост с нашего стенда в любой соц.сети с '
                         'хештегом #testittms и отправь скриншот публикации в бот',
                         reply_markup=builder.as_markup())


@router.callback_query(text='post_screen')
async def get_screen(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Отправьте скриншот поста с использованием хэштега #testittms',
                                  reply_markup=cancel_key.as_markup())
    await state.set_state(GetScreen.get_screen_state)


@router.message(GetScreen.get_screen_state)
async def get_screen(message: Message, state: FSMContext):
    try:
        from bot import bot
        from bot import db

        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)

        await bot.download_file(file.file_path, f'data/post_screens/{message.from_user.id}_post_photo.jpg')

        await db.add_post_photo_path(
            user_id=str(message.from_user.id),
            post_photo_path=f'data/post_screens/{message.from_user.id}_post_photo.jpg'
        )

        await message.answer('Мы получили ваш скриншот с постом, большое спасибо!')
        await state.clear()

        # ____----____----____----____----____----____----____----____----____----
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

    except TypeError:
        await message.answer('Пожалуйста отправьте фото, на котором размещен пост с хэштегом',
                             reply_markup=cancel_key.as_markup())


@router.callback_query(text='post_cancel')
async def cancel_post_send(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Если вы все таки решите сделать пост и отправить скриншот обязательно возвращайтесь!',
                                  reply_markup=main_working.keyboard())

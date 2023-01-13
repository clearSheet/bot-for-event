from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards import main_working
from keyboards.inlines import back_to_main_menu

router = Router()


class GetResume(StatesGroup):
    start_get_resume = State()
    get_resume = State()


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text="Отменить отправку", callback_data="send_resume_cancel")
)


text_ruler = 'В случае, если вы захотите с нами сотрудничать - ' \
             'отправьте резюме в удобном для вас формате:\n\n' \
             ' - PDF\n' \
             ' - ULR (ссылка на удобную для вас платформу)\n' \
             ' - IMG (Изображение с необходимой информацией)'


@router.message(GetResume.start_get_resume)
@router.message(text='💼 Отправить резюме')
async def send_resume(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text_ruler, reply_markup=back_to_main_menu.keyboard())

    await state.set_state(GetResume.get_resume)


@router.message(GetResume.get_resume)
async def get_resume(message: Message, state: FSMContext):
    from bot import db
    from bot import bot

    running = True

    if running:
        try:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)

            await bot.download_file(file.file_path, f'data/user_resume/{message.from_user.id}_resume_photo.jpg')

            await db.add_user_resume(
                user_id=str(message.from_user.id),
                resume_path=f'data/user_resume/{message.from_user.id}_resume_photo.jpg'
            )

            await message.answer('Большое спасибо, мы с вами свяжемся 🤝', reply_markup=main_working.keyboard())

            running = False
        except TypeError:
            pass

    if running:
        try:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)

            file_name = message.document.file_name
            format = file_name[file_name.find('.') + 1:]

            if format == 'pdf':
                await bot.download_file(file.file_path, f'data/user_resume/{message.from_user.id}_resume_{file_name}')
                await db.add_user_resume(
                    user_id=str(message.from_user.id),
                    resume_path=f'data/user_resume/{message.from_user.id}_resume_{file_name}'
                )

                await state.clear()
                await message.answer('Большое спасибо, мы с вами свяжемся 🤝', reply_markup=main_working.keyboard())
                running = False
            else:
                await message.answer(text_ruler, reply_markup=back_to_main_menu.keyboard())
                await state.set_state(GetResume.get_resume)
                running = False
        except AttributeError:
            pass

    if running:
        try:
            if "https" in message.text:
                await db.add_user_resume(
                    user_id=str(message.from_user.id),
                    resume_path=message.text
                )

                await state.clear()
                await message.answer('Большое спасибо, мы с вами свяжемся 🤝', reply_markup=main_working.keyboard())
                running = False
            else:
                await message.answer(text_ruler, reply_markup=back_to_main_menu.keyboard())
                await state.set_state(GetResume.get_resume)
                running = False
        except TypeError:
            await message.answer(text_ruler, reply_markup=builder.as_markup())

    if running:
        await message.answer('Я не знаю что делать, я хочу смерти')
        running = False
        await state.set_state(GetResume.get_resume)


@router.callback_query(text='send_resume_cancel')
async def send_resume_cancel(callback: CallbackQuery):
    await callback.message.answer('Как только захотите поделиться резюме - обязательно возвращайтесь!',
                                  reply_markup=main_working.keyboard())
from aiogram import Router
from aiogram.types import Message

from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.dispatcher.fsm.context import FSMContext


from keyboards.admin_keyboards import main_admin_kb
from keyboards.admin_keyboards import quiz_kb
from keyboards import yes_or_no_keyboard


from config import check_admin


router = Router()


@router.message(text='Настройка квиза')
async def show_questions(message: Message):
    if await check_admin(message.from_user.id):
        await message.answer('Выбирите пункт меню',
                             reply_markup=quiz_kb.edit_quiz())


@router.message(text='Просмотреть вопросы')
async def show_questions(message: Message):
    if await check_admin(message.from_user.id):
        from bot import db

        arr_questions = await db.show_quiz_questions()
        msg = ''

        for item in arr_questions:
            msg += f'Вопрос: {item[0]}, ответ: {item[1]}\n\n'

        await message.answer(msg, parse_mode="HTML")


class DeleteQuestions(StatesGroup):
    yes_or_no = State()


@router.message(text='Удалить вопросы')
async def show_questions(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer('Вы действительно хотите удалить вопросы?',
                             reply_markup=yes_or_no_keyboard.keyboard())

        await state.set_state(DeleteQuestions.yes_or_no)


@router.message(DeleteQuestions.yes_or_no)
async def yes_or_no(message: Message, state: FSMContext):
    if message.text == 'Да ✅':
        from bot import db
        await db.delete_all_questin()
        await state.clear()
        await message.answer('Данные о вопросах удалены',
                             reply_markup=main_admin_kb.keyboard())
    elif message.text == 'Нет ❌':
        await message.answer('Удаление не произведено',
                             reply_markup=main_admin_kb.keyboard())
        await state.clear()
    else:
        await message.answer('Пожалуйста выбирите ответ при помощи клавиатуры')
        await state.set_state(DeleteQuestions.yes_or_no)



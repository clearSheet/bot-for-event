import asyncio

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State

from keyboards import true_or_edit_keyboard
from keyboards import variable_keyboard

from keyboards.admin_keyboards import quiz_kb
# from keyboards import


from config import check_admin

router = Router()


class AddNewQuizQuestion(StatesGroup):
    get_question = State()
    edit_get_question = State()

    get_1_variant = State()
    edit_get_1_variant = State()

    get_2_variant = State()
    edit_get_2_variant = State()

    get_3_variant = State()
    edit_get_3_variant = State()

    get_4_variant = State()
    edit_get_4_variant = State()

    get_right_variant = State()
    edit_get_right_variant = State()

    get_about = State()
    edit_get_about = State()

    get_photo = State()
    edit_get_photo = State()


@router.message(text='Добавить вопрос')
async def add_quiz(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer('Введите вопрос', reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddNewQuizQuestion.get_question)


@router.message(AddNewQuizQuestion.get_question)
async def get_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(f'Вопрос будет таким\n\n{message.text}\n\nВерно?',
                         reply_markup=true_or_edit_keyboard.keyboard())
    await state.set_state(AddNewQuizQuestion.edit_get_question)


@router.message(AddNewQuizQuestion.edit_get_question)
async def edit_get_question(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        await state.set_state(AddNewQuizQuestion.get_1_variant)
        await message.answer('Введите первый вариант ответа', reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Изменить ✍️':
        await state.set_state(AddNewQuizQuestion.get_question)
        await message.answer('Введите вопрос', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Пожалуйста выберете ответ кнопкой')
        await state.set_state(AddNewQuizQuestion.edit_get_question)


# _______________1
@router.message(AddNewQuizQuestion.get_1_variant)
async def get_1_variant(message: Message, state: FSMContext):
    await state.update_data(variant_1=message.text)
    await message.answer(f'Первый вариант\n\n{message.text}\n\nВерно?',
                         reply_markup=true_or_edit_keyboard.keyboard())
    await state.set_state(AddNewQuizQuestion.edit_get_1_variant)


@router.message(AddNewQuizQuestion.edit_get_1_variant)
async def edit_get_1_variant(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        await state.set_state(AddNewQuizQuestion.get_2_variant)
        await message.answer('Введите второй вариант ответа', reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Изменить ✍️':
        await state.set_state(AddNewQuizQuestion.get_1_variant)
        await message.answer('Введите новый вариант', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Пожалуйста выберете ответ кнопкой')
        await state.set_state(AddNewQuizQuestion.get_1_variant)


# _______________2
@router.message(AddNewQuizQuestion.get_2_variant)
async def get_2_variant(message: Message, state: FSMContext):
    await state.update_data(variant_2=message.text)
    await message.answer(f'Второй вариант\n\n{message.text}\n\nВерно?',
                         reply_markup=true_or_edit_keyboard.keyboard())
    await state.set_state(AddNewQuizQuestion.edit_get_2_variant)


@router.message(AddNewQuizQuestion.edit_get_2_variant)
async def edit_get_2_variant(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        await state.set_state(AddNewQuizQuestion.get_3_variant)
        await message.answer('Введите третий вариант ответа', reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Изменить ✍️':
        await state.set_state(AddNewQuizQuestion.get_2_variant)
        await message.answer('Введите новый вариант', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Пожалуйста выберете ответ кнопкой')
        await state.set_state(AddNewQuizQuestion.edit_get_2_variant)


# _______________3
@router.message(AddNewQuizQuestion.get_3_variant)
async def get_3_variant(message: Message, state: FSMContext):
    await state.update_data(variant_3=message.text)
    await message.answer(f'Третий вариант\n\n{message.text}\n\nВерно?',
                         reply_markup=true_or_edit_keyboard.keyboard())
    await state.set_state(AddNewQuizQuestion.edit_get_3_variant)


@router.message(AddNewQuizQuestion.edit_get_3_variant)
async def edit_get_3_variant(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        await state.set_state(AddNewQuizQuestion.get_4_variant)
        await message.answer('Введите чертвертый вариант ответа', reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Изменить ✍️':
        await state.set_state(AddNewQuizQuestion.get_3_variant)
        await message.answer('Введите новый вариант', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Пожалуйста выберете ответ кнопкой')
        await state.set_state(AddNewQuizQuestion.edit_get_3_variant)


# _______________4
@router.message(AddNewQuizQuestion.get_4_variant)
async def get_4_variant(message: Message, state: FSMContext):
    await state.update_data(variant_4=message.text)
    await message.answer(f'Четвертый вариант\n\n{message.text}\n\nВерно?',
                         reply_markup=true_or_edit_keyboard.keyboard())
    await state.set_state(AddNewQuizQuestion.edit_get_4_variant)


@router.message(AddNewQuizQuestion.edit_get_4_variant)
async def edit_get_4_variant(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        await state.set_state(AddNewQuizQuestion.get_right_variant)
        variables = await state.get_data()
        await message.answer('Отправьте верный вариант',
                             reply_markup=variable_keyboard.keyboard(
                                 var1=variables['variant_1'],
                                 var2=variables['variant_2'],
                                 var3=variables['variant_3'],
                                 var4=variables['variant_4']
                             ))
    elif message.text == 'Изменить ✍️':
        await state.set_state(AddNewQuizQuestion.get_4_variant)
        await message.answer('Введите новый вариант', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Пожалуйста выберете ответ кнопкой')
        await state.set_state(AddNewQuizQuestion.edit_get_4_variant)


@router.message(AddNewQuizQuestion.get_right_variant)
async def get_right_variant(message: Message, state: FSMContext):
    variables = await state.get_data()

    if message.text == variables['variant_1']:
        await state.update_data(right_variant=message.text)
        await state.set_state(AddNewQuizQuestion.get_about)
        await message.answer('Введите описание вопроса, которое будет отображено'
                             ' обычным текстом после ответа пользователя',
                             reply_markup=ReplyKeyboardRemove())
    elif message.text == variables['variant_2']:
        await state.update_data(right_variant=message.text)
        await state.set_state(AddNewQuizQuestion.get_about)
        await message.answer('Введите описание вопроса, которое будет отображено'
                             ' обычным текстом после ответа пользователя',
                             reply_markup=ReplyKeyboardRemove())
    elif message.text == variables['variant_3']:
        await state.update_data(right_variant=message.text)
        await state.set_state(AddNewQuizQuestion.get_about)
        await message.answer('Введите описание вопроса, которое будет отображено'
                             ' обычным текстом после ответа пользователя',
                             reply_markup=ReplyKeyboardRemove())
    elif message.text == variables['variant_4']:
        await state.update_data(right_variant=message.text)
        await state.set_state(AddNewQuizQuestion.get_about)
        await message.answer('Введите описание вопроса, которое будет отображено'
                             ' обычным текстом после ответа пользователя',
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Пожалуйста выбирете ответ кнопкой',
                             reply_markup=variable_keyboard.keyboard(
                                 var1=variables['variant_1'],
                                 var2=variables['variant_2'],
                                 var3=variables['variant_3'],
                                 var4=variables['variant_4']
                             ))
        await state.set_state(AddNewQuizQuestion.get_right_variant)


@router.message(AddNewQuizQuestion.get_about)
async def get_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer(f"Описание будет таким\n\n{message.text}\n\nВерноо?",
                         reply_markup=true_or_edit_keyboard.keyboard())
    await state.set_state(AddNewQuizQuestion.edit_get_about)


@router.message(AddNewQuizQuestion.edit_get_about)
async def edit_get_about(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        await message.answer('Отлично, теперь отправьте фото, которое будет прикреплено к вопросу',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddNewQuizQuestion.get_photo)
    elif message.text == 'Изменить ✍️':
        await message.answer('Введи описание, которое будет отобраажено текстом',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddNewQuizQuestion.edit_get_about)
    else:
        await message.answer('Пожалуйста используйте кнопки для ответа')
        await state.set_state(AddNewQuizQuestion.edit_get_about)


@router.message(AddNewQuizQuestion.get_photo)
async def get_photo(message: Message, state: FSMContext):
    from bot import bot

    try:
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)

        from datetime import datetime
        file_name = str(datetime.now()).replace('-', '_').replace(':', '_').replace('.', '_'). replace(' ', '_') + '_photo.jpg'

        await bot.download_file(file.file_path, f'data/question_photo/{file_name}')
        await message.answer('Отлично, изрбражение сохранено', reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddNewQuizQuestion.edit_get_photo)
        await state.update_data(photo_path=f'data/question_photo/{file_name}')

        await asyncio.sleep(3)
        photo = FSInputFile(f'data/question_photo/{file_name}')
        await message.reply_photo(caption='Фото вопроса будет выглядеть так, вас устраивает?',
                                  photo=photo,
                                  reply_markup=true_or_edit_keyboard.keyboard())
    except TypeError:
        await message.answer('Пожалуйста отправьте изображение',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddNewQuizQuestion.get_photo)


@router.message(AddNewQuizQuestion.edit_get_photo)
async def edit_get_photo(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        data = await state.get_data()
        await message.answer('Отлично, новый вопрос создан!',
                             reply_markup=quiz_kb.edit_quiz())

        from bot import db

        await db.add_new_question(
            question=str(data['question']),
            variant_1=str(data['variant_1']),
            variant_2=str(data['variant_2']),
            variant_3=str(data['variant_3']),
            variant_4=str(data['variant_4']),
            right_variant=str(data['right_variant']),
            photo_path=str(data['photo_path']),
            about=str(data['about'])
        )

        await state.clear()
    elif message.text == 'Изменить ✍️':
        await message.answer('Пожалуйста отправьте новое изображение',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddNewQuizQuestion.get_photo)
    else:
        await message.answer('Пожалуйста используйте клавиатуру')
        await state.set_state(AddNewQuizQuestion.edit_get_photo)
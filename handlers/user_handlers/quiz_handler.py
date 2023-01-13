from aiogram import Router
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMedia, InputFile, InputMediaPhoto, ReplyKeyboardRemove

from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State

from keyboards import main_working

from keyboards.inlines import variable

import asyncio

router = Router()

user_question = {}
user_keyboard = {}


class Quiz_State(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()
    question_10 = State()


@router.message(text='🧠 Квиз')
async def start_quiz_handler(message: Message, state: FSMContext):
    from bot import db
    from bot import bot

    user_info = await db.get_one_user_info(message.from_user.id)
    quiz_status = user_info[0][17]

    if quiz_status == None:
        all_questions = await db.get_all_questions()

        #  Создание переменной с количеством вопросов в данный момент
        count_all_questions = len(all_questions)

        # Создание информаци на основе кол-ва сохраненнных вопросов
        if count_all_questions == 0:
            await message.answer('Извините, в данный момент не вопросов для провередения Квиза.')

        if count_all_questions > 0:
            await message.answer('Квиз начинается!', reply_markup=ReplyKeyboardRemove())
            await state.update_data(question_1=all_questions[0])

        if count_all_questions > 1:
            await state.update_data(question_2=all_questions[1])

        if count_all_questions > 2:
            await state.update_data(question_3=all_questions[2])

        if count_all_questions > 3:
            await state.update_data(question_4=all_questions[3])

        if count_all_questions > 4:
            await state.update_data(question_5=all_questions[4])

        if count_all_questions > 5:
            await state.update_data(question_6=all_questions[5])

        if count_all_questions > 6:
            await state.update_data(question_7=all_questions[6])

        if count_all_questions > 7:
            await state.update_data(question_8=all_questions[7])

        if count_all_questions > 8:
            await state.update_data(question_9=all_questions[8])

        if count_all_questions > 9:
            await state.update_data(question_10=all_questions[9])

        data = await state.get_data()

        if data['question_1']:
            info = data['question_1']

            question = str(info[0])

            answer_1 = str(info[1])
            answer_2 = str(info[2])
            answer_3 = str(info[3])
            answer_4 = str(info[4])

            right_answer = str(info[5])
            photo_path = str(info[6])
            question_num = 1
            photo = FSInputFile(photo_path)

            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=question,
                reply_markup=variable.keyboard(
                    var1=answer_1,
                    var2=answer_2,
                    var3=answer_3,
                    var4=answer_4,
                    question_num=question_num
                )
            )

    else:
        await message.answer('Вы уже прошли квиз, двигайтесь дальше!')
        await state.clear()

@router.callback_query(Text(text_startswith="question_"))
async def question_1(callback: CallbackQuery, state: FSMContext):
    ans = str(callback.data.split('_')[2]).replace('var', '')


    call_data = callback.data
    question_answer_num = call_data.split('_')[1]
    next_question = int(question_answer_num) + 1

    data = await state.get_data()
    right_answer_num = data[f'question_{question_answer_num}'][8]
    right_answer_text = data[f'question_{question_answer_num}'][5]


    if right_answer_num == ans:
        # await callback.message.answer('Правильно')
        last_msg = await callback.message.edit_caption('Правильно!')
        from bot import db
        await db.add_point_for_true_answer_queiz(callback.message.chat.id)
    elif right_answer_num == 0:
        last_msg = await callback.message.edit_caption('Правильно!')
        from bot import db
        await db.add_point_for_true_answer_queiz(callback.message.chat.id)
    else:
        # await callback.message.answer('Не правильно')
        last_msg = await callback.message.edit_caption(f'Неправильно!\n\nПравильный ответ: {right_answer_text}')
    print(right_answer_num)
    print(ans)
    await asyncio.sleep(3)
    try:
        if data[f'question_{next_question}']:
            from bot import bot
            info = data[f'question_{next_question}']

            question = str(info[0])

            answer_1 = str(info[1])
            answer_2 = str(info[2])
            answer_3 = str(info[3])
            answer_4 = str(info[4])

            photo_path = str(info[6])
            question_num = next_question
            photo = FSInputFile(photo_path)

            photo = InputMediaPhoto(
                media=photo,
                caption=question
            )

            await bot.edit_message_media(
                media=photo,
                chat_id=callback.from_user.id,
                message_id=last_msg.message_id,
                reply_markup=variable.keyboard(
                    var1=answer_1,
                    var2=answer_2,
                    var3=answer_3,
                    var4=answer_4,
                    question_num=question_num
                )
            )
    except KeyError:
        from bot import bot
        from bot import db

        await db.quiz_status_update(callback.from_user.id)
        data = await db.get_one_user_info(callback.from_user.id)
        quiz_result = data[0][8]

        photo = FSInputFile('data/cover.jpg')

        end_msg = InputMediaPhoto(
            caption=f'Поздравляем, ты прошел квиз!\n\n'
                    f'Количество правильных ответов: {quiz_result}/10',
            media=photo
        )

        await bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=last_msg.message_id,
            media=end_msg
        )

        await callback.message.answer(text='Пора двигаться дальше!',
                                      reply_markup=main_working.keyboard())
        # Отображение сообщения о прохождении квиза

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

        if in_test_it1 == 1 and friends_count1 >= 2 and user_lvl1 == 0:
            await db.lvl_up_user(callback.from_user.id)
            await callback.answer('Поздравляем с получением нового уровня!')

        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 4 and user_lvl1 == 1:
            await db.lvl_up_user(callback.from_user.id)
            await callback.answer('Поздравляем с получением нового уровня!')

        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 6 and user_lvl1 == 2 and quiz_status1 == 1 and post_path1 and email1:
            await db.lvl_up_user(callback.from_user.id)
            await callback.answer('Поздравляем с получением нового уровня!')

        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 8 and user_lvl1 == 3 and quiz_status1 == 1 and post_path1 and review1:
            await db.lvl_up_user(callback.from_user.id)
            await callback.answer('Поздравляем с получением нового уровня!')


@router.callback_query(Text(text_startswith="cancel_quiz"))
async def get_uot_quiz(callback: CallbackQuery, state: FSMContext):
    from bot import db

    await db.null_quiz(callback.from_user.id)

    await state.clear()
    await callback.message.answer('Приходи еще, если захочешь испытать свои силы!',
                                  reply_markup=main_working.keyboard())

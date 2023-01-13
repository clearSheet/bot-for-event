import asyncio

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove, UserProfilePhotos
from aiogram.types import FSInputFile
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State


from keyboards import true_or_edit_keyboard, share_phone_number, main_working

from bot import db

from data import msg
from functions import generate_card

router = Router()


class RegisterNewUser(StatesGroup):
    start = State()
    # Работа с именем пользователя
    get_user_name = State()
    edit_user_name = State()
    # Работа с логином пользователя
    get_user_login = State()
    edit_user_login = State()
    # Работа с должностью и компанией пользователя
    get_user_position_and_company = State()
    confirm_user_position_and_company = State()
    edit_user_position_and_company = State()
    # Работа со статусом пользователя
    get_user_status = State()
    confirm_user_status = State()
    # Работас с фото пользователя
    get_user_photo = State()
    confirm_user_photo = State()
    # Работа с номером телефона пользователя
    get_user_phone = State()


# __ Работа с QR кодом
from aiogram.dispatcher.filters import CommandObject


@router.message(commands=['start'])
async def test(message: Message, command: CommandObject, state: FSMContext):
    # qr_code = command.args
    await state.clear()

    # Пользователь использовал qr
    if command.args:
        qr_code = str(command.args)
        # Пользователь использует валидный QR
        if await db.chek_qr_id_db(qr_code=qr_code):
            # Пользователь использует qr и зарегестрирован
            if await db.user_in_the_database(message.from_user.id):
                # Пользователь использует валидный qr, который привязан к пользователю
                if await db.user_tied_qr(qr_code):
                    # or await db.user_tied_qr(qr_code)
                    user = await db.get_user_by_qr(qr_code)
                    user = str(user[0]).replace('(', '').replace(')','').replace(',','').replace("'", "")

                    user_1 = message.chat.id

                    # Пользователь уже в друзьях
                    if await db.check_friends(user_id_1=user_1, user_id_2=user):
                        await message.answer('Ты уже добавил этого пользователя в друзья')
                    # Пользователи не в друзьях
                    # Добавление в ДРУЗЬЯ
                    else:
                        await db.add_friends(user_id_1=user_1, user_id_2=user)
                        from bot import bot

                        photo1 = FSInputFile(f'data/user_profiles/{user}_profile.jpg')
                        photo2 = FSInputFile(f'data/user_profiles/{message.chat.id}_profile.jpg')

                        data1 = await db.get_one_user_info(str(user))
                        data2 = await db.get_one_user_info(str(message.chat.id))

                        login1 = str(data1[0][2])
                        login2 = str(data2[0][2])

                        await message.reply_photo(caption=f'Новое знакомство! \n\n @{login1}',
                                                  photo=photo1)

                        await bot.send_photo(
                            chat_id=user,
                            photo=photo2,
                            caption=f'Новое знакомство! \n\n @{login2}'
                        )

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

                        user_info2 = await db.get_one_user_info(user)
                        user_info2 = user_info2[0]
                        review2 = user_info2[7]
                        user_lvl2 = user_info2[9]
                        email2 = user_info2[10]
                        post_path2 = user_info2[12]
                        friends_count2 = user_info2[14]
                        in_test_it2 = user_info2[15]
                        in_teamstorm2 = user_info2[16]
                        quiz_status2 = user_info2[17]

                        if in_test_it1 == 1 and friends_count1 >= 2 and user_lvl1 == 0:
                            await db.lvl_up_user(message.from_user.id)
                            await message.answer('Поздравляем с получением нового уровня!')

                        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 4 and user_lvl1 == 1:
                            await db.lvl_up_user(message.from_user.id)
                            await message.answer('Поздравляем с получением нового уровня!')

                        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 6 and user_lvl1 == 2 and quiz_status1 == 1 and post_path1 and email1:
                            await db.lvl_up_user(message.from_user.id)
                            await message.answer('Поздравляем с получением нового уровня!')

                        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 8 and user_lvl1 == 3   and quiz_status1 == 1 and post_path1 and review1:
                            await db.lvl_up_user(message.from_user.id)
                            await message.answer('Поздравляем с получением нового уровня!')



                        if in_test_it2 == 1 and friends_count2 >= 2 and user_lvl2 == 0:
                            await db.lvl_up_user(message.from_user.id)
                            await bot.send_message(chat_id=user, text='Поздравляем с получением нового уровня!')

                        if in_test_it2 == 1 and in_teamstorm2 == 1 and friends_count2 >= 4 and user_lvl2 == 1:
                            await db.lvl_up_user(message.from_user.id)
                            await bot.send_message(chat_id=user, text='Поздравляем с получением нового уровня!')

                        if in_test_it2 == 1 and in_teamstorm2 == 1 and friends_count2 >= 6 and user_lvl2 == 2 and quiz_status2 == 1 and post_path2 and email2:
                            await db.lvl_up_user(message.from_user.id)
                            await bot.send_message(chat_id=user, text='Поздравляем с получением нового уровня!')

                        if in_test_it1 == 1 and in_teamstorm2 == 1 and friends_count2 >= 8 and user_lvl2 == 3   and quiz_status2 == 1 and post_path2 and review2:
                            await db.lvl_up_user(message.from_user.id)
                            await bot.send_message(chat_id=user, text='Поздравляем с получением нового уровня!')





                # Пользователь использует qr, который не привязан к пользователю
                else:
                    # Пользователь использует валиный QR
                    if await db.chek_qr_id_db(qr_code):
                        await message.answer('Пользователь с таким QR еще не зарегестрирован\n'
                                             'Помоги ему пройти регистрацию в боте!')
                    # Пользователь использует не валидный qr
                    else:
                        await message.answer('Такого QR-кода не существует')
            # Пользователь использует qr и не зарегестрирован
            # Процесс РЕГИСТРАЦИИ
            else:
                # QR код валидный
                if await db.chek_qr_id_db(qr_code):
                    await state.update_data(qr_code=qr_code)

                    # await message.answer(msg.hi_message_one, parse_mode="MarkdownV2")
                    photo = FSInputFile(f'data/cover.jpg')

                    await message.answer_photo(
                        photo=photo,
                        caption=msg.hi_message_one,
                        parse_mode="MarkdownV2"
                    )

                    await message.answer(msg.hi_message_second, parse_mode="MarkdownV2")

                    if message.from_user.first_name and message.from_user.last_name:
                        await message.answer(f'Давайте знакомиться!\n'
                                             f'Твое имя {message.from_user.first_name + message.from_user.last_name}, верно? 👇',
                                             reply_markup=true_or_edit_keyboard.keyboard())
                        await state.set_state(RegisterNewUser.get_user_name)
                    elif message.from_user.first_name:

                        await message.answer(f'Давайте знакомиться!\n'
                                             f'Твое имя {message.from_user.first_name}, верно? 👇',
                                             reply_markup=true_or_edit_keyboard.keyboard())
                        await state.set_state(RegisterNewUser.get_user_name)
                    else:
                        await message.answer('Давайте знакомиться!'
                                             'Как тебя зовут?👇')
                        await state.set_state(RegisterNewUser.edit_user_name)
                # QR код не валидный
                else:
                    await message.answer('Ты используешь не настоящий QR-код!')
        #  Пользователь использует не валидный QR
        else:
            await message.answer('Если ты дошел до этого шага, ты - настоящий хакер\n'
                                 'Но не надо пробовать меня взламывать, я умный!')
    # Пользователь не использует QR
    else:
            # Пользователь не использует qr и зарегестрирован
            if await db.user_in_the_database(message.from_user.id):
                await message.answer('Начало работы', reply_markup=main_working.keyboard())
            # Пользователь не использует qr и не зарегестрирован
            else:
                await message.answer('Для работы с ботом вам необходимо использовать'
                                     'индивидуальный QR-код, который ты можешь найти '
                                     'на стенде!')


@router.message(RegisterNewUser.get_user_name)
async def get_user_name(message: Message, state: FSMContext):
    await state.update_data(user_login=message.from_user.username)

    if message.text == 'Верно ✅':
        try:
            name = await state.get_data()
            name = name['user_name']
            await state.update_data(user_name=name)
            await state.set_state(RegisterNewUser.get_user_position_and_company)
            await message.answer('Отлично! Мы сохранили твое имя ✅\n\n'
                                 'Теперь расскажи о себе подробнее. Как называется твоя должность и компания?\n\n'
                                 'Например: Team Lead, Test IT', reply_markup=ReplyKeyboardRemove())
        except KeyError:
            if message.from_user.first_name and message.from_user.last_name:
                await state.update_data(user_name=message.from_user.first_name + " " + message.from_user.last_name)
                # await message.answer(f'Отлично! Мы сохранили твое имя ✅\n\n',
                                     # f'Твой телеграм-аккаунт @{message.from_user.username}, верно?',
                                     # reply_markup=true_or_edit_keyboard.keyboard())
                # await state.set_state(RegisterNewUser.get_user_login)
                await state.set_state(RegisterNewUser.get_user_position_and_company)
                await message.answer('Отлично! Данные сохранены 🔥\n'
                                     'Теперь расскажи о себе подробнее. Как называется твоя должность и компания?\n\n'
                                     'Например: Team Lead, Test IT\n\n', reply_markup=ReplyKeyboardRemove())

            else:
                await state.update_data(user_name=message.from_user.first_name)
                # await message.answer(f'Отлично! Мы сохранили твое имя ✅\n\n',
                                     # f'Твой телеграм-аккаунт @{message.from_user.username}, верно?',
                                     # reply_markup=true_or_edit_keyboard.keyboard())
                # await state.set_state(RegisterNewUser.get_user_login)
                await state.set_state(RegisterNewUser.get_user_position_and_company)
                await message.answer('Отлично! Данные сохранены 🔥\n'
                                     'Теперь расскажи о себе подробнее. Как называется твоя должность и компания?\n\n'
                                     'Например: Team Lead, Test IT\n\n', reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Изменить ✍️':
        await message.answer('Введи свое имя')
        await state.set_state(RegisterNewUser.edit_user_name)
    else:
        await message.answer('Пожалуйста выбери ответ кнопкой',
                             reply_markup=true_or_edit_keyboard.keyboard())
        await state.set_state(RegisterNewUser.get_user_name)


@router.message(RegisterNewUser.edit_user_name)
async def edit_user_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer(f'Ты указал {message.text} в качестве имени, верно?',
                         reply_markup=true_or_edit_keyboard.keyboard())
    await state.set_state(RegisterNewUser.get_user_name)


@router.message(RegisterNewUser.get_user_login)
async def get_user_login(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        await state.update_data(user_login=message.from_user.username)
        await message.answer('Отлично! Данные сохранены 🔥\n'
                             'Теперь расскажи о себе подробнее. Как называется твоя должность и компания?\n\n'
                             'Например: Team Lead, Test IT\n\n', reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterNewUser.get_user_position_and_company)
    elif message.text == 'Изменить ✍️':
        await message.answer('Введи имя своего аккаунта, начиная с @ 👇')
        await state.set_state(RegisterNewUser.edit_user_login)
    else:
        await message.answer('Пожалуйста выбери ответ кнопкой')
        await state.set_state(RegisterNewUser.edit_user_name)


@router.message(RegisterNewUser.edit_user_login)
async def edit_user_login(message: Message, state: FSMContext):
    await state.update_data(user_login=message.text)
    await message.answer(f'Твой телеграм-аккаунт {message.text}, верно?')
    await state.set_state(RegisterNewUser.get_user_login)


@router.message(RegisterNewUser.get_user_position_and_company)
async def get_user_position_and_company(message: Message, state: FSMContext):
    await message.answer(f'Ты указал о себе такую информацию:\n\n{message.text}\n\nВерно?',
                         reply_markup=true_or_edit_keyboard.keyboard())
    await state.set_state(RegisterNewUser.confirm_user_position_and_company)
    await state.update_data(user_position_and_company=message.text)


@router.message(RegisterNewUser.confirm_user_position_and_company)
async def confirm_user_position_and_company(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        await message.answer('Супер! Все данные сохранены.\n\n'
                             'Следующий шаг - поставь статус(не более 38 символов) для своего профиля.\n'
                             'Например: «В 14:00 выступаю с докладом. Буду рад пообщаться!» или «Ищу SDET в команду»',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterNewUser.get_user_status)
    elif message.text == 'Изменить ✍️':
        await message.answer('Введи свою должность и название компании через запятую 👇',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterNewUser.get_user_position_and_company)
    else:
        await message.answer('Пожалуйста используй кнопки для ответа')
        await state.set_state(RegisterNewUser.confirm_user_position_and_company)


@router.message(RegisterNewUser.get_user_status)
async def get_user_status(message: Message, state: FSMContext):
    await state.update_data(user_status=message.text)
    if len(message.text) > 38:
        await message.answer('Введи статус, который менее 38 символов')
        await state.set_state(RegisterNewUser.get_user_status)
    else:
        await message.answer(f'Твой статус:\n\n'
                             f'{message.text}\n\n'
                             f'Верно?', reply_markup=true_or_edit_keyboard.keyboard())
        await state.set_state(RegisterNewUser.confirm_user_status)


@router.message(RegisterNewUser.confirm_user_status)
async def confirm_user_status(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        await message.answer('Твой профиль почти готов!',
                             reply_markup=ReplyKeyboardRemove())

        #  Твое фото будет выглядеть вот так, согласен?

        from bot import bot
        try:
            user_profile_photo: UserProfilePhotos = await bot.get_user_profile_photos(message.from_user.id)
            file = await bot.get_file(user_profile_photo.photos[0][-1].file_id)
            await bot.download_file(file.file_path, f'data/user_photos/{message.from_user.id}_photo.jpg')

            await state.update_data(photo_path=f'data/user_photos/{message.from_user.id}_photo.jpg')

            await asyncio.sleep(3)

            photo = FSInputFile(f'data/user_photos/{message.from_user.id}_photo.jpg')
            await message.reply_photo(caption='Мы выбрали твое фото из профиля, но ты можешь его изменить.',
                                      photo=photo,
                                      reply_markup=true_or_edit_keyboard.keyboard())

            await state.set_state(RegisterNewUser.confirm_user_photo)
        except IndexError:
            await message.answer('Отправь вертикальное фото или сделай селфи 📷')
            await state.set_state(RegisterNewUser.get_user_photo)


    elif message.text == 'Изменить ✍️':
        await message.answer('Поставь статус для своего профиля.\n\n'
                             'Например: «В 14:00 выступаю с докладом. Буду рад пообщаться!» или «Ищу SDET в команду»',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterNewUser.get_user_status)
    else:
        await message.answer('Пожалуйста выбири ответ кнопкой')
        await state.set_state(RegisterNewUser.confirm_user_status)


@router.message(RegisterNewUser.get_user_photo)
async def get_user_photo(message: Message, state: FSMContext):

    try:
        from bot import bot

        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)

        await bot.download_file(file.file_path, f'data/user_photos/{message.from_user.id}_photo.jpg')
        await state.set_state(RegisterNewUser.confirm_user_photo)
        await state.update_data(photo_path=f'data/user_photos/{message.from_user.id}_photo.jpg')

        await asyncio.sleep(3)
        photo = FSInputFile(f'data/user_photos/{message.from_user.id}_photo.jpg')
        await message.reply_photo(caption='Твой профиль будет выглядеть так, верно?',
                                  photo=photo,
                                  reply_markup=true_or_edit_keyboard.keyboard())

        # from bot import bot
        #
        # user_profile_photo: UserProfilePhotos = await bot.get_user_profile_photos(message.from_user.id)
        # file = await bot.get_file(user_profile_photo.photos[0][-1].file_id)
        # await bot.download_file(file.file_path, f'data/user_photos/{message.from_user.id}_photo.jpg')
    except TypeError:
        await message.answer('Отправь вертикальное фото или сделай селфи 📷')
        await state.set_state(RegisterNewUser.get_user_photo)


@router.message(RegisterNewUser.confirm_user_photo)
async def confirm_user_photo(message: Message, state: FSMContext):
    if message.text == 'Верно ✅':
        await message.answer('Последний шаг - осталось отправить номер телефона',
                             reply_markup=share_phone_number.keyboard())
        await state.set_state(RegisterNewUser.get_user_phone)

        data = await state.get_data()
        await generate_card.generate(
            user_id=str(message.from_user.id),
            user_name=data['user_name'],
            position_and_company_user=data['user_position_and_company'],
            user_login=data['user_login'],
            user_status=data['user_status']
        )

    elif message.text == 'Изменить ✍️':
        await message.answer('Твой профиль почти готов!\n'
                             'Отправь вертикальное фото или сделай селфи 📷', reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterNewUser.get_user_photo)
    else:
        await message.answer('Пожалуйста используй клавиатуру для ответов')
        await state.set_state(RegisterNewUser.confirm_user_photo)


@router.message(RegisterNewUser.get_user_phone)
async def get_user_phone(message: Message, state: FSMContext):
    if message.contact != None:
        await state.update_data(user_phone=str(message.contact.phone_number))

        data = await state.get_data()

        await db.add_new_user(user_id=int(message.from_user.id),
                              user_name=str(data['user_name']),
                              user_login=str(data['user_login']),
                              position_and_company_user=str(data['user_position_and_company']),
                              photo_path=str(data['photo_path']),
                              user_status=str(data['user_status']),
                              user_phone=str(data['user_phone']))
        await db.bind_user_to_qr(
            qr_code=str(data['qr_code']),
            user_id=message.chat.id
        )
        await state.clear()

        # await message.answer("Поздравляем! Твой игровой профиль создан!"
        #                      "Теперь можно прокачивать своего игрока до секретного четвертого уровня и собирать "
        #                      "фирменный мерч, участвовать в квизе и попробовать выиграть Apple Watch, сканировать "
        #                      "QR-коды и расширять свой круг знакомств!\n"
        #                      "[Карточка профиля]"
        #                      , reply_markup=main_working.keyboard())

        card_profile = FSInputFile(f'data/user_profiles/{message.from_user.id}_profile.jpg')

        await message.reply_photo(
            photo=card_profile,
            caption="Поздравляем! Твой игровой профиль создан!\n\n"
                    "Теперь можно прокачивать своего игрока до секретного четвертого уровня и собирать "
                    "фирменный мерч, участвовать в квизе и попробовать выиграть Apple Watch, сканировать "
                    "QR-коды и расширять свой круг знакомств!\n",
            reply_markup=main_working.keyboard()
        )

        await message.answer("Твоя цель – дойти до секретного уровня 💪\n"
                             "Чтобы узнать подробности, нажми кнопку «Отобразить правила»\n\n"
                             "Начни с первого уровня 🕹\n"
                             "Чтобы получить первый уровень:\n"
                             "1. Вступи в Telegram-канал Test IT и оставайся в нем (кнопка в меню «Вступить в группы»)\n"
                             "2. Познакомься и отсканируй QR-код не менее 10 других игроков")
    elif message.text == 'Не делиться ❌':
        await state.update_data(user_phone=str('Не поделился'))

        data = await state.get_data()

        await db.add_new_user(user_id=int(message.from_user.id),
                              user_name=str(data['user_name']),
                              user_login=str(data['user_login']),
                              position_and_company_user=str(data['user_position_and_company']),
                              photo_path=str(data['photo_path']),
                              user_status=str(data['user_status']),
                              user_phone=str(data['user_phone']))
        await db.bind_user_to_qr(
            qr_code=str(data['qr_code']),
            user_id=message.chat.id
        )
        await state.clear()

        card_profile = FSInputFile(f'data/user_profiles/{message.from_user.id}_profile.jpg')

        await message.reply_photo(
            photo=card_profile,
            caption="Поздравляем! Твой игровой профиль создан!"
                    "Теперь можно прокачивать своего игрока до секретного четвертого уровня и собирать "
                    "фирменный мерч, участвовать в квизе и попробовать выиграть Apple Watch, сканировать "
                    "QR-коды и расширять свой круг знакомств!\n",
            reply_markup=main_working.keyboard()
        )

        await message.answer("Твоя цель – дойти до секретного уровня 💪\n"
                             "Чтобы узнать подробности, нажми кнопку «Отобразить правила»\n\n"
                             "Начни с первого уровня 🕹\n"
                             "Чтобы получить первый уровень:\n"
                             "Вступи в Telegram-канал Test IT и оставайся в нем (кнопка в меню «Вступить в группы»)\n"
                             "Познакомься и отсканируй QR-код не менее 10 других игроков")
    else:
        await message.answer('Пожалуйста отправьте номер телефона кнопкой или выбирите вариант без отправки номера')
        await state.set_state(RegisterNewUser.get_user_phone)


@router.message(commands=['menu'])
async def go_menu(message: Message, state: FSMContext):
    await state.set_state()
    await message.answer('Главное меню', reply_markup=main_working.keyboard())

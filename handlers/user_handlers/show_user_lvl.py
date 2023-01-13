import asyncio
from aiogram import Router
from aiogram.types import Message

from aiogram.types import FSInputFile


router = Router()


@router.message(text='🕹 Мой уровень')
async def show_rules_of_event(message: Message):
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

    data = await db.get_one_user_info(message.from_user.id)
    lvl = data[0][9]


    if user_lvl1 == 0:
        text_answer = 'Для прокачки до первого уровня выполни следующие условия:\n\n' \
                      '1. Вступи в Telegram-канал Test IT и оставайся в нем (кнопка в меню «Вступить в ' \
                      'группы»)\n' \
                      '2. Познакомься и отсканируй QR-код не менее 10 других игроков'
    elif user_lvl1 == 1:
        text_answer = 'Для перехода на второй уровень выполни следующие условия:\n\n' \
                      '1. Вступи в Telegram-канал TeamStorm и оставайся в нем (кнопка в меню «Вступить ' \
                      'в группы»)\n' \
                      '2. Познакомься и отсканируй QR-код не менее 20 других игроков'
    elif user_lvl1 == 2:
        text_answer = 'Для перехода на третий уровень выполни следующие условия:\n\n' \
                        '1. Вступи в Telegram-канал Test IT и TeamStorm и оставайся в них (кнопка в меню ' \
                        '«Вступить в группы»)\n' \
                        '2. Познакомься и отсканируй QR-код не менее 40 других игроков\n' \
                        '3. Пройди наш квиз (кнопка в меню «Квиз»)\n' \
                        '4. Опубликуй пост с нашего стенда в любой соц.сети с хештегом #testittms\n'\
                        '5.Отметь новости о каких продуктах тебе интересны (кнопка в меню «Новости о '\
                        'продуктах»)'

    elif user_lvl1 == 3:
        text_answer = 'Для перехода на секретный четвертый уровень выполни следующие условия:\n\n' \
                  '1.Вступи в Telegram-каналы Test IT и TeamStorm и оставайся в них (кнопка в меню ' \
                  '«Вступить в группы»)\n' \
                  '2.Познакомься и отсканируй QR-код не менее 60 других игроков\n' \
                  '3.Пройди наш квиз (кнопка в меню «Квиз»)\n' \
                  '4.Опубликуй пост с нашего стенда в любой соц.сети с хештегом #testittms\n' \
                  '5.Оставь отзыв о работе нашей команды (кнопка в меню «Оставить отзыв»)\n' \
                  '6.Отметь новости о каких продуктах тебе интересны (кнопка в меню «Новости о ' \
                  'продуктах»)'
    else:
        text_answer = 'Ты достиг самого большого уровня!'

    if lvl == 0:
        await message.answer('Ты находишься на нулевом уровне, следуй правилам и ты повысишь свой уровень!')
        await message.answer(text_answer)
    else:
        if in_test_it1 == 1 and friends_count1 >= 2 and user_lvl1 == 0:
            await db.lvl_up_user(message.from_user.id)
            await message.answer('Поздравляем с получением нового уровня!')
            await message.answer(text_answer)

        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 4 and user_lvl1 == 1:
            await db.lvl_up_user(message.from_user.id)
            await message.answer('Поздравляем с получением нового уровня!')
            await message.answer(text_answer)

        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 6 and user_lvl1 == 2 and quiz_status1 == 1 and post_path1 and email1:
            await db.lvl_up_user(message.from_user.id)
            await message.answer('Поздравляем с получением нового уровня!')
            await message.answer(text_answer)

        if in_test_it1 == 1 and in_teamstorm1 == 1 and friends_count1 >= 8 and user_lvl1 == 3 and quiz_status1 == 1 and post_path1 and review1:
            await db.lvl_up_user(message.from_user.id)
            await message.answer('Поздравляем с получением нового уровня!')
            await message.answer(text_answer)

        photo = FSInputFile(f'data/users_lvl_presets/{lvl}_level.jpg')

        await message.answer_photo(photo=photo, caption=text_answer)

        if user_lvl1 == 3:
            await message.answer(
                text='Всех, кто прокачивал уровни своего профиля, ждем на стенде Test IT'
                     ' в 17:00 для розыгрыша призов!\n'
                     'Победители активностей будут выбраны случайный образом. Чтобы не'
                     ' упустить свой шанс и получить приз —  физическое присутствие обязательно!\n\n'
                     'Сбор в 16:55 ⏰'
            )

        # ____----____----____----____----____----____----____----____----____----

        # ____----____----____----____----____----____----____----____----____----

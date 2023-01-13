from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, FSInputFile

from openpyxl import Workbook

from config import check_admin

router = Router()


@router.message(text='Инф. о пользователях')
async def get_all_user_info(message: Message):
    if await check_admin(message.from_user.id):
        from bot import db
        from bot import bot
        all_info_users = await db.get_info_all_users()

        new_book = Workbook()
        new_book_sheet = new_book.active

        new_book_sheet.append(
            [
                'ID',
                'Name',
                'Login',
                'Company',
                'Status',
                'Phone Number',
                'Email',
                'Review',
                'Quiz points',
                'LVL',
                'Category maling',
                'Friends count',
                'Quiz status'
            ]
        )

        for all_info_users in all_info_users:
            user_id = all_info_users[0]
            user_name = all_info_users[1]
            user_login = all_info_users[2]
            company_and_position = all_info_users[3]
            user_status = all_info_users[5]
            user_phone = all_info_users[6]
            user_email = all_info_users[10]
            user_review = all_info_users[7]
            user_quiz_points = all_info_users[8]
            user_lvl = all_info_users[9]
            user_emailing_category = all_info_users[11]
            user_frinds_count = all_info_users[14]
            quiz_status = all_info_users[17]

            new_book_sheet.append(
                [
                    user_id,
                    user_name,
                    user_login,
                    company_and_position,
                    user_status,
                    user_phone,
                    user_email,
                    user_review,
                    user_quiz_points,
                    user_lvl,
                    user_emailing_category,
                    user_frinds_count,
                    quiz_status
                ]
            )

        new_book.save(filename='data/all_user_info.xlsx')

        document = FSInputFile('data/all_user_info.xlsx')

        await bot.send_document(
            chat_id=message.from_user.id,
            document=document
        )
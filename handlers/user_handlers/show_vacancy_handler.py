from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(text='🏢 Посмотреть вакансии')
async def show_rules_of_event(message: Message):
    await message.answer("Посмотреть вакансии можно по ссылке:\n\n"
                         "[Посмотреть вакансии](https://testit.software/vacancies?utm_source=tlg-bot&utm_medium=social)",
                         parse_mode="MarkdownV2")


import asyncio

from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(text='🤝 Знакомства')
async def show_rules_of_event(message: Message):
    from bot import db
    data = await db.get_one_user_info(user_id=message.from_user.id) # 14
    friends_count = data[0][14]
    await message.answer('Количество друзей в твоем списке: ' + str(friends_count))
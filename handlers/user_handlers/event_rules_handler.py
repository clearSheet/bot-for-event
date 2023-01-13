import asyncio

from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(text='📃 Отобразить правила')
async def show_rules_of_event(message: Message):
    await message.answer('Перед началом прочитай инструкцию по прокачке своего профиля 👇\n\n'
                         '[Ссылка на правила](https://telegra.ph/Vsem-igrokam-prigotovitsya-11-15)',
                         parse_mode="MarkdownV2")
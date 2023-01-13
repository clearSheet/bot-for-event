from aiogram import types
from aiogram.dispatcher.filters import BaseFilter

class IsSubscriber(BaseFilter):
    async def check(self, message: types.Message):
        from bot import bot
        sub = await bot.get_chat_member( )
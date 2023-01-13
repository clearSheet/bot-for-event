import asyncio

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State

from keyboards.admin_keyboards import main_admin_kb
from keyboards import variable_keyboard
# from keyboards import


from config import check_admin

router = Router()


@router.message(commands=["admin"])
async def main_admin_handler(message: Message):
    if await check_admin(message.from_user.id):
        await message.answer('Выбирите пункт меню', reply_markup=main_admin_kb.keyboard())

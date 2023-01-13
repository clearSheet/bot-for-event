import asyncio

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State

from config import check_admin
from keyboards import true_or_edit_keyboard
from keyboards import variable_keyboard

from keyboards.admin_keyboards import quiz_kb
# from keyboards import

from bot import db

router = Router()


@router.message(text='Инф. о пользователях')
async def show_info(message: Message):
    if await check_admin(message.from_user.id):

        from openpyxl import Workbook

        new_book = Workbook()
        new_book_sheet = new_book.active

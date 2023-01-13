import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from database.sqlite import DataBase

from handlers.user_handlers import start_and_register_user_handler

from handlers.user_handlers import event_rules_handler
from handlers.user_handlers import show_user_lvl
from handlers.user_handlers import join_groups_handler
from handlers.user_handlers import quiz_handler
from handlers.user_handlers import show_vacancy_handler
from handlers.user_handlers import social_media_post_handler
from handlers.user_handlers import review_handler
from handlers.user_handlers import news_of_products_handler
from handlers.user_handlers import send_resume_handler
from handlers.user_handlers import friends_handler

# Удалить
from handlers.user_handlers import test_start_handler

from handlers.admin import add_quiz
from handlers.admin import main_admin_handler
from handlers.admin import show_or_edit_quiz
from handlers.admin import info_of_users

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()
# База данных
db = DataBase('tg.db')


# Запуск процесса поллинга новых апдейтов
async def main():
    # Основной хендлер работы старта и регистрации
    dp.include_router(start_and_register_user_handler.router)

    # Хендлеры работы меню
    dp.include_router(test_start_handler.router)

    dp.include_router(event_rules_handler.router)  # Отображение правил мероприятия
    dp.include_router(show_user_lvl.router)
    dp.include_router(join_groups_handler.router)
    dp.include_router(quiz_handler.router)
    dp.include_router(show_vacancy_handler.router)
    dp.include_router(social_media_post_handler.router)
    dp.include_router(review_handler.router)
    dp.include_router(news_of_products_handler.router)
    dp.include_router(send_resume_handler.router)
    dp.include_router(friends_handler.router)

    dp.include_router(add_quiz.router)
    dp.include_router(main_admin_handler.router)
    dp.include_router(show_or_edit_quiz.router)
    dp.include_router(info_of_users.router)

    # тестовый хендлер, нужно удалить
    # from handlers.admin import test
    # dp.include_router(test.router)

    # Пропускаем все наконпленные сообзения
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск работы бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

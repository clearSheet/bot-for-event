from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="📃 Отобразить правила"), KeyboardButton(text="🕹 Мой уровень")],
        [KeyboardButton(text="👥 Вступить в группы"), KeyboardButton(text="🤝 Знакомства")],
        [KeyboardButton(text="🧠 Квиз"), KeyboardButton(text="#️⃣ Пост в соц. сетях")],
        [KeyboardButton(text="📲 Новости по продуктам"), KeyboardButton(text="✍️ Написать отзыв")],
        [KeyboardButton(text="🏢 Посмотреть вакансии"), KeyboardButton(text="💼 Отправить резюме")]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True)

    return keyboard
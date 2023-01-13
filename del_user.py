import asyncio

import sqlite3


class DataBase:
    def __init__(self, db_path: str):
        """
        Подключиться к базе данных и создать таблицы
        :param db_path: нужен для подключения к базе данных
        """
        self.base = sqlite3.connect(db_path)
        self.cur = self.base.cursor()
        if self.base:
            print('Database connected OK!')

        """
        :param user_id: id пользователя, берем из телеграма
        :param user_name: указанное имя в телеграмме или выбранное пользователем в боте
        :param user_login: Логин пользователя в телеграме
        :param position_and_company_user: Указанные данные о должности и компании пользотваля
        :param photo_path: путь к изображению, которое отправил пользователь
        :param user_status: Статус указанный пользователем при регистрации 
        :param user_phone: Отправленный пользователем номер телефона
        """
        self.base.execute('CREATE TABLE IF NOT EXISTS users('
                          'user_id INTEGER PRIMARY KEY,'
                          'user_name TEXT,'
                          'user_login TEXT,'
                          'position_and_company_user TEXT,'
                          'photo_path TEXT,'
                          'user_status TEXT, '
                          'user_phone TEXT,'
                          'review TEXT,'
                          'quiz_result INTEGER,'
                          'user_lvl INTEGER,'
                          'email TEXT,'
                          'category TEXT,'
                          'post_photo_path TEXT,'
                          'resume_path TEXT,'
                          'user_friends_count INT,'
                          'in_test_it_group INT,'
                          'in_teamstorm_group INT,'
                          'quiz_status INT)')

        self.base.execute('CREATE TABLE IF NOT EXISTS quiz('
                          'question TEXT,'
                          'variant_1 TEXT,'
                          'variant_2 TEXT,'
                          'variant_3 TEXT,'
                          'variant_4 TEXT,'
                          'right_variant TEXT,'
                          'photo_path TEXT,'
                          'about TEXT,'
                          'var_num TEXT)')

        self.base.execute('CREATE TABLE IF NOT EXISTS qr_user('
                          'qr_code TEXT,'
                          'user_id TEXT)')

        self.base.execute('CREATE TABLE IF NOT EXISTS users_friends('
                          'user_id_1 TEXT,'
                          'user_id_2 TEXT)')

        # self.base.commit()
        # self.cur.close()

    async def add_new_user(self, user_id: int, user_name: str, user_login: str, position_and_company_user: str,
                           photo_path: str, user_status: str, user_phone: str):

        self.cur.execute('INSERT OR IGNORE INTO users(user_id, user_name, user_login, position_and_company_user, '
                         'photo_path, user_status, user_phone, user_lvl, user_friends_count, in_test_it_group,'
                         'in_teamstorm_group, quiz_result) '
                         'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                         (user_id, user_name, user_login, position_and_company_user, photo_path, user_status,
                          user_phone, 0, 0, 0, 0, 0))
        self.base.commit()

    async def user_in_the_database(self, id_user: int):
        result = self.cur.execute('SELECT * FROM users WHERE user_id=?', (id_user,)).fetchone()

        if result is None:
            return False
        else:
            return True

    # Добавление нового вопроса в Квиз
    async def add_new_question(self, question: str, variant_1: str, variant_2: str, variant_3: str,
                               variant_4: str, right_variant: str, photo_path: str, about: str):

        var_arr = [variant_1, variant_2, variant_3, variant_4]
        count_var = 1
        var_num = 0

        for var in var_arr:
            if right_variant == var:
                var_num = count_var
            else:
                count_var += 1

        self.cur.execute('INSERT OR IGNORE INTO quiz(question, variant_1, variant_2, variant_3, '
                         'variant_4, right_variant, photo_path, about, var_num) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                         (question, variant_1, variant_2, variant_3, variant_4, right_variant, photo_path, about, var_num))
        print(f'{question} add to database Quiz, {var_num} = {right_variant}')
        self.base.commit()

    # Просмоотреть вопросы квиза
    async def show_quiz_questions(self):
        self.cur.execute('SELECT question, right_variant FROM quiz')
        return self.cur.fetchall()

    # Получить все вопросы, ответы, изображения
    async def get_all_questions(self):
        self.cur.execute('SELECT * FROM quiz')
        return self.cur.fetchall()

    # Удалить вопросы квиза
    async def delete_all_questin(self):
        self.cur.execute('DELETE FROM quiz')
        return self.cur.fetchall()

    # Отправить отзыв
    async def add_review(self, review: str, user_id: str):
        self.cur.execute(f'UPDATE users SET review=? WHERE user_id=?', (review, user_id, ))
        self.base.commit()

    # Сохранить  Email адреса и выбранной категории
    # async def add_email_and_category(self, user_id: str, email: str, mailing_categories: str):
    #     self.cur.execute(f'UPDATE users SET email={email}'
    #                      f'WHERE user_id={user_id}')
    #
    #     self.cur.execute(f'UPDATE users SET mailing_categories={mailing_categories}'
    #                      f'WHERE user_id={user_id}')

    # Добавление нового qr кода
    async def add_new_qr_code_to_db(self, qr_code: str):
        self.cur.execute('INSERT OR IGNORE INTO qr_user(qr_code) VALUES(?)', (qr_code, ))
        self.base.commit()

    # Привязать пользователя к QR
    async def bind_user_to_qr(self, qr_code: str, user_id):
        self.cur.execute(f'UPDATE qr_user SET user_id={user_id} WHERE qr_code={qr_code}')
        self.base.commit()

    # Привязан ли пользователь к QR
    async def user_tied_qr(self, qr_code: str):
        result = self.cur.execute('SELECT * FROM qr_user WHERE qr_code=?', (qr_code, )).fetchone()
        if result is None:
            return False
        else:
            return True

    # Получить пользователя по QR-коду
    async def get_user_by_qr(self, qr_code: str):
        self.cur.execute('SELECT user_id FROM qr_user WHERE qr_code=?', (qr_code, ))
        return self.cur.fetchall()

    # Проверить наличие QR кода в БАЗЕ данных
    async def chek_qr_id_db(self, qr_code: str):
        result = self.cur.execute('SELECT * FROM qr_user WHERE qr_code=?', (qr_code,)).fetchone()

        if result is None:
            return False
        else:
            return True

    # Добавить пользователей в друзья друг другу
    async def add_friends(self, user_id_1: str, user_id_2: str):
        self.cur.execute('INSERT OR IGNORE INTO users_friends(user_id_1, user_id_2) VALUES(?, ?)',
                         (user_id_1, user_id_2, ))
        self.cur.execute('INSERT OR IGNORE INTO users_friends(user_id_1, user_id_2) VALUES(?, ?)',
                         (user_id_2, user_id_1,))

        self.cur.execute(f'UPDATE users SET user_friends_count=user_friends_count+1 WHERE user_id=?', (user_id_1,))
        self.cur.execute(f'UPDATE users SET user_friends_count=user_friends_count+1 WHERE user_id=?', (user_id_2,))
        self.base.commit()

    # Проверить есть ли пользователи в друзьях друг у друга
    async def check_friends(self, user_id_1: str, user_id_2: str):
        result = self.cur.execute('SELECT * FROM users_friends WHERE user_id_1=? and user_id_2=? ',
                                  (user_id_1, user_id_2, )).fetchone()

        if result is None:
            return False
        else:
            return True

    # Получить инфор о пользователе
    async def get_one_user_info(self, user_id):
        self.cur.execute('SELECT * FROM users WHERE user_id=?', (user_id, ))
        return self.cur.fetchall()

    # Добавить запись о email адресе и выбранной категории
    async def add_email_and_category(self, user_id: str, email: str, category: str):
        self.cur.execute(f'UPDATE users SET email=?, category=? WHERE user_id=?', (email, category, user_id, ))
        self.base.commit()

    # Получаить данные о всех пользотвателях
    async def get_info_all_users(self):
        self.cur.execute('SELECT * FROM users')
        return self.cur.fetchall()

    # Добавить данные о пути к изображению скриншота о посте
    async def add_post_photo_path(self, user_id: str, post_photo_path: str):
        self.cur.execute(f'UPDATE users SET post_photo_path=? WHERE user_id=?', (post_photo_path, user_id,))
        self.base.commit()

    # Добавить данные о пути к резюме пользователя
    async def add_user_resume(self, user_id: str, resume_path: str):
        self.cur.execute(f'UPDATE users SET resume_path=? WHERE user_id=?', (resume_path, user_id,))
        self.base.commit()

    #  Поднять уровень пользователю
    async def lvl_up_user(self, user_id: str):
        self.cur.execute(f'UPDATE users SET user_lvl=user_lvl+1 WHERE user_id=?', (user_id,))
        self.base.commit()

    # Получить данные о уровне пользователя
    async def get_user_lvl(self, user_id):
        self.cur.execute('SELECT user_lvl FROM users WHERE user_id=?', (user_id, ))
        return self.cur.fetchall()

    # Получить данные о количестве друзеей пользователя
    async def get_user_friends_count(self, user_id):
        self.cur.execute('SELECT user_friends_count FROM users WHERE user_id=?', (user_id,))
        return self.cur.fetchall()

    # Изменить значение вступления в группу test_it
    async def edit_status_group_test_it(self, user_id: str, status: int):
        # in_test_it_group
        self.cur.execute(f'UPDATE users SET in_test_it_group=? WHERE user_id=?', (status, user_id,))
        self.base.commit()

    # Изменить значение вступления в группу teamstorm
    async def edit_status_group_teamstorm(self, user_id: str, status: int):
        # in_teamstorm_group
        self.cur.execute(f'UPDATE users SET in_teamstorm_group=? WHERE user_id=?', (status, user_id,))
        self.base.commit()

    # Изменить статус прохождени квиза
    async def quiz_status_update(self, user_id: str):
        self.cur.execute(f'UPDATE users SET quiz_status=1 WHERE user_id=?', (user_id,))
        self.base.commit()

    # Добавить бал за правильный ответ
    async def add_point_for_true_answer_queiz(self, user_id: str):
        self.cur.execute(f'UPDATE users SET quiz_result=quiz_result+1 WHERE user_id=?', (user_id,))
        self.base.commit()

    # тестовый метод добавления уровня друзей
    async def set_count_friends(self, user_id: str, count_friend: int):
        self.cur.execute(f'UPDATE users SET user_friends_count=? WHERE user_id=?', (count_friend, user_id,))
        self.base.commit()

    # Обнулить ответы квиза
    async def null_quiz(self, user_id: str):
        self.cur.execute(f'UPDATE users SET quiz_result=0 WHERE user_id=?', (user_id,))
        self.base.commit()

    # Удлаить пользователя из БД
    async def delete_user_1(self, user_id: str):
        self.cur.execute("DELETE FROM users WHERE user_id=?", (user_id, ))
        self.cur.execute("DELETE FROM users_friends WHERE user_id_1=?", (user_id, ))
        self.cur.execute("DELETE FROM users_friends WHERE user_id_2=?", (user_id, ))


        return self.cur.fetchall()

    async def delete_user_2(self, user_id: str):
        self.cur.execute(f'UPDATE qr_user SET user_id=(null) WHERE user_id=?', (user_id,))
        self.base.commit()


db = DataBase('tg.db')

async def test():
    # user_id = '960110943'
    user_id = '0'

    await db.delete_user_1(user_id=user_id)
    await db.delete_user_2(user_id=user_id)

    print('deleted')


asyncio.run(test())


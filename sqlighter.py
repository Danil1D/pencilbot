import sqlite3


class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def day(self, chat_id, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `day_id` FROM `subscriptions` WHERE  `chat_id` = ? and `user_id` = ? ",
                                       (chat_id, user_id,)).fetchall()

    def update_day(self, chat_id, user_id, day_id):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `day_id` =  ? WHERE  `chat_id` = ? and `user_id` = ?",
                (day_id, chat_id, user_id))

    def new_day(self, day_id=1):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `day_id` =  ? ", (day_id,)).fetchall

    def get_subscriptions(self, chat_id, status=True, ):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT `status` FROM `subscriptions` WHERE `user_id` = ? and `chat_id` = ? ",
                                       (chat_id, status,)).fetchall()

    def subscriber_exists(self, user_id, chat_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ? and `chat_id` = ? ',
                                         (user_id, chat_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, first_name, status, chat_id):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `subscriptions` (`user_id`,`first_name`, `status`, `chat_id`) VALUES(?,?,?,?)",
                (user_id, first_name, status, chat_id,))

    def update_subscription(self, user_id, chat_id, status=True):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `status` =  ? WHERE  `chat_id` = ? and `user_id` = ?",
                (status, chat_id, user_id))

    def get_all(self, chat_id):
        with self.connection:
            records = []
            self.cursor.execute(
                'SELECT `first_name`, `status` FROM `subscriptions` WHERE `chat_id` = ? ORDER BY `status` DESC',
                (chat_id,))
            rows = self.cursor.fetchall()
            for row in rows:
                records.append(row)
            return records

    def get_top(self, chat_id):
        with self.connection:
            top = []
            self.cursor.execute(
                'SELECT `first_name`, `status` FROM `subscriptions` WHERE `chat_id` = ? ORDER BY `status` DESC',
                (chat_id,))
            rows1 = self.cursor.fetchall()
            for row1 in (rows1):
                top.append(row1)
            return top

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

import datetime
import os
import sqlite3


class ChatHistory:

    @classmethod
    def insert_variable_into_table(cls, data, result):

        user_id = data["user_id"]
        country = data['country']
        city = data['city']
        min_price = data['min_price']
        max_price = data['max_price']
        date = datetime.datetime.now()

        if result:
            result = ([str(y) for x in result for y in x.split('\n')])
            hotels = ''.join(result)  # результат поиска
        else:
            hotels = 'No result'

        try:
            sqlite_connection = sqlite3.connect(os.path.join('database', 'chat_history.db'))
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            sqlite_insert_with_param = """INSERT INTO Request
                                                    (user,  date, country, city, min_price, max_price, result)
                                                    VALUES(?,?,?,?,?,?,?)
                                                    """
            data_tuple = (user_id, date, country, city, min_price, max_price, hotels)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_connection.commit()
            print("Переменные Python успешно вставлены в таблицу")

            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
            with open('errors.log', 'a') as errors:  # записываем ошибки в лог
                errors.write(f'{datetime.datetime.now()}, Data base error: {error}\n')

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    @classmethod
    def create_message(cls, user_id):

        try:
            connection = sqlite3.connect(os.path.join('database', 'chat_history.db'))
            try:
                messages = [message for message in
                            connection.execute(
                                "SELECT user, date,  country, city, min_price, max_price, result FROM Request")
                            if user_id in message]

                if messages:

                    for message in messages:
                        message_form = {"User id": message[0],
                                        "date": message[1][:19],
                                        "country": message[2],
                                        "city": message[3],
                                        "min price": message[4],
                                        "max price": message[5],
                                        "Results": message[6]}

                        message_to_user = ', '.join(string + ": " + str(data) for string, data in message_form.items())
                        yield message_to_user
                else:
                    yield False

            except sqlite3.Error as error:
                with open('errors.log', 'a') as errors:  # записываем ошибки в лог
                    errors.write(f'{datetime.datetime.now()}, Data base error: {error}\n')

        except ConnectionError as error:
            with open('errors.log', 'a') as errors:  # записываем ошибки в лог
                errors.write(f'{datetime.datetime.now()}, Data base error: {error}\n')


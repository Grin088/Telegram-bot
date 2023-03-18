import datetime
from pathlib import Path
from typing import Generator
import os


class History:

    __path = os.path.abspath(os.path.join('database'))

    @classmethod
    def save_search_history(cls, user_id, data, result) -> None:

        """Метод для сохранения истории поиска"""

        country, city, min_price, max_price = data['country'], data['city'], data['min price'], data['max price']
        with open(os.path.abspath(os.path.join(cls.__path, 'chat_history.txt')), 'a', encoding='utf-8') as chat_history:
            result = ([str(y) for x in result for y in x.split('\n')])
            hotels = ' '.join(result)  # результат поиска
            # записываем данные в историю поиска
            chat_history.write(
                f'{datetime.datetime.now()}, user_id: {user_id}'
                f' request: {country}, {city}'
                f' price: min {min_price}, max {max_price}, result: {hotels}\n')

    @classmethod
    def get_history(cls, user_id) -> Generator:
        """Метод для поиска и вывода
         информации о поиске пользователя"""

        file = Path(os.path.join(cls.__path, 'chat_history.txt'))  # проверка существования файла
        file.touch(exist_ok=True)

        result = False
        # флаг для проверки существования результата в истории поиска
        with open(os.path.join(cls.__path, 'chat_history.txt'), 'r') as history:

            for line in history:
                if str(user_id) in line.split():  # проверка ID пользователя в истории поиска
                    result = True
                    yield line

            if not result:
                yield False

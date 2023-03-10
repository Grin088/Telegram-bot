
import datetime
from step_control import StepControl
from pathlib import Path
from typing import Generator


class DataGather(StepControl):

    """Класс сбора информации
    вводимой пользователем в чате и
    сохранения и вывода информации о поиске
    """

    def __init__(self) -> None:
        super().__init__()
        self._user_id = None
        self._high_price = None
        self._low_price = None
        self._best_deal = None

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def high_price(self):
        return self._high_price

    @high_price.setter
    def high_price(self, status):
        self._high_price = status

    @property
    def low_price(self):
        return self._low_price

    @low_price.setter
    def low_price(self, status):
        self._low_price = status

    @property
    def best_deal(self):
        return self._best_deal

    @best_deal.setter
    def best_deal(self, status):
        self._best_deal = status

    def save_search_history(self, result) -> None:

        """Метод для сохранения истории поиска"""

        with open('chat_history.txt', 'a', encoding='utf-8') as chat_history:
            hotels = ' '.join(result)  # результат поиска
            # записываем данные в историю поиска
            chat_history.write(
                f'{datetime.datetime.now()}, user_id: {self._user_id}'
                f' request: {self._country}, {self._city}'
                f' price: min {self._min_price}, max {self._max_price}, result: {hotels}\n')

    def get_history(self) -> Generator:

        """Метод для поиска и вывода
         информации о поиске пользователя"""

        file = Path('chat_history.txt')  # проверка существования файла
        file.touch(exist_ok=True)

        result = False  # флаг для проверки существования результата в истории поиска
        with open('chat_history.txt', 'r') as history:

            for line in history:
                if str(self._user_id) in line.split():  # проверка ID пользователя в истории поиска
                    result = True
                    yield line

            if not result:
                yield False




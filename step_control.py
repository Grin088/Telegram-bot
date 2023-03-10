import re


class StepControl:

    """Класс контроля шагов в чате бота"""

    def __init__(self) -> None:

        self._method = None
        self._start = None
        self._counter = None
        self._country = None
        self._city = None
        self._hotel_quantity = None
        self._check_in_date = None
        self._check_out_date = None
        self._distance = None
        self._min_price = None
        self._max_price = None
        self._photos = None
        self._photos_quantity = None
        self._finish = None

    @property
    def method(self) -> bool:
        return self._method

    @method.setter
    def method(self, status: bool) -> None:
        self._method = status

    @property
    def start(self) -> bool:
        return self._start

    @start.setter
    def start(self, status: bool):
        self._start = status

    @property
    def counter(self) -> int:
        return self._counter

    @counter.setter
    def counter(self, counter: int):
        self._counter = counter

    @property
    def city(self) -> None:
        return self._city

    @city.setter
    def city(self, status: bool) -> None:
        self._city = status

    @property
    def country(self) -> bool:
        return self._country

    @country.setter
    def country(self, status: bool) -> None:
        self._country = status

    @property
    def hotel_quantity(self) -> bool:
        return self._hotel_quantity

    @hotel_quantity.setter
    def hotel_quantity(self, status: bool) -> None:
        self._hotel_quantity = status

    @property
    def check_in_date(self) -> bool:
        return self._check_in_date

    @check_in_date.setter
    def check_in_date(self, status: bool) -> None:
        self._check_in_date = status

    @property
    def check_out_date(self) -> bool:
        return self._check_out_date

    @check_out_date.setter
    def check_out_date(self, status: bool) -> None:
        self._check_out_date = status

    @property
    def distance(self) -> bool:
        return self._distance

    @distance.setter
    def distance(self, status: bool) -> None:
        self._distance = status

    @property
    def max_price(self) -> bool:
        return self._max_price

    @max_price.setter
    def max_price(self, status: bool) -> None:
        self._max_price = status

    @property
    def min_price(self) -> bool:
        return self._min_price

    @min_price.setter
    def min_price(self, status: bool) -> None:
        self._min_price = status

    @property
    def photos(self) -> bool:
        return self._photos

    @photos.setter
    def photos(self, status: bool) -> None:
        self._photos = status

    @property
    def photos_quantity(self) -> bool | str:
        return self._photos_quantity

    @photos_quantity.setter
    def photos_quantity(self, value: bool) -> None:
        self._photos_quantity = value

    @property
    def finish(self) -> bool:
        return self._finish

    @finish.setter
    def finish(self, status: bool) -> None:
        self._finish = status

    def reset_param(self) -> None:
        """Метод для сброса
         параметров класса"""
        [setattr(self, x, None) for x in dir(self) if re.match('^[a-z_]+[a-z]$', x)
         and x not in ['reset_param', 'save_search_history', 'get_history']]

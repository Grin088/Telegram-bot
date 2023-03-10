import json
import requests
import datetime
import numpy as np
from typing import Type, Any, Callable, Optional, Generator
from requests import Response


def retry_on_connection_error(max_attempts: int = 10) -> Callable[[Type[Any]], Callable[..., Any]]:
    """
    Декоратор, повторяет декорированный метод класса при ошибках соединения.

    Args:
        max_attempts (int): Максимальное число попыток (default=10).
    Returns:
        Callable: Decorated function.
    """
    def decorator(cls: Type[Any]) -> Callable[..., Any]:

        def wrapper(*args: Any, **kwargs: Any) -> Optional[Any]:

            attempt_counter = 0  # считает количество попыток подключений
            while attempt_counter < max_attempts:
                try:
                    result = cls(*args, **kwargs)
                    if result.status_code != 200:  # если ответ с сервера отрицательный возникает ошибка
                        raise ReferenceError(result.reason)
                    return result  # в случае положительного ответа возвращаем True
                except (requests.ConnectionError, ReferenceError) as error:
                    with open('errors.log', 'a') as errors:  # записываем ошибки в лог
                        errors.write(f'{datetime.datetime.now()}, {error}\n')
                    attempt_counter += 1
            return False
        return wrapper
    return decorator


class HotelRequest:

    """
    Класс для запроса данных с сервера через API
     и сортировки полученного результат в зависимости от запроса пользователя
     """

    _headers = {
        "X-RapidAPI-Key": "2edaeb5594msh135f465ed72fa5bp15829cjsn868db2218774",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    def __init__(self):

        self.country = None
        self._city = None
        self._city_id = None
        self._cost = None
        self.photo = None
        self.check_in = None
        self.check_out = None
        self.distance = None
        self._hotels_information = {}
        self.result = None

    def get_city_id(self):
        return self._city_id

    def recursion_searcher(self, name: dict, key: str) -> Generator:
        """
        Рекурсивный поиск для получения значения ключа

        :parameter:
            name (dict): Словарь для поиска
            key (str): Ключ для поиска
.
        """
        if key in name:
            yield name.get(key)

        for i_elem in name.values():

            if isinstance(i_elem, list):
                for i_value in i_elem:
                    if isinstance(i_value, dict):
                        yield from self.recursion_searcher(i_value, key)

            elif isinstance(i_elem, dict):
                yield from self.recursion_searcher(i_elem, key)

    @retry_on_connection_error()
    def country_id_request(self, name: str) -> Optional[Any]:

        """
         Метод для получения city ID
         :param name: Name of the city

         :return: None если нет соединения с сервером или ответ сервера отрицательный
         если ответ положительный возвращает HTTP response

         """

        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": f"{name}"}

        response = requests.request("GET", url, headers=self._headers, params=querystring)
        if response:

            data = json.loads(response.text)
            with open('place_id.json', 'w') as file:
                json.dump(data, file, indent=4)

            with open('place_id.json', 'r') as get_place_id:
                data = json.load(get_place_id)

                city_id = [
                    elem.get('gaiaId') for elem in data.get('sr', [])
                    if elem.get('type') == 'CITY'
                    and elem.get('hierarchyInfo')['country']['name'] == self.country
                ]
                if city_id:
                    self._city_id = city_id[0]
                else:
                    return 'No result'

        return response

    @retry_on_connection_error()
    def find_hotels(
            self, max_price: str, min_price: str,
            high_price: bool, quantity: str) -> Response:

        """
        Метод запроса информации об отеле и сортировки данных

        :arg:
            max_price (str): Максимальная цена комнаты.
            min_price (str): Минимальная цена комнаты.
            low_price (bool): If True, сортируем по низкой цене.
            high_price (bool): If True, сортируем по высокой цене.
            best_deal (bool): If True, сортируем по расстоянию от центра .
            quantity (str): Количество отелей для поиска.

        :return:
            Optional[Any]: Response: если запрос сервера успешный, None: если запрос отрицательный
        """

        check_in_date = self.check_in.split()  # создаем список для запроса дат
        check_out_date = self.check_out.split()  # создаем список для запроса дат

        sort_method = "PRICE_LOW_TO_HIGH"

        if high_price:
            sort_method = 'PRICE_HIGH_TO_LOW'

        url = "https://hotels4.p.rapidapi.com/properties/v2/list"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "destination": {"regionId": f"{self._city_id}"},
            "checkInDate": {
                "day": int(check_in_date[0]),
                "month": int(check_in_date[1]),
                "year": int(check_in_date[2])
            },
            "checkOutDate": {
                "day": int(check_out_date[0]),
                "month": int(check_out_date[1]),
                "year": int(check_out_date[2])
            },
            "rooms": [
                {
                    "adults": 2,
                    "children": []
                }
            ],

            "resultsStartingIndex": 0,
            "resultsSize": int(quantity),
            "sort": sort_method,
            "filters": {"price": {
                "max": int(max_price),
                "min": int(min_price)
            }}
        }

        response = requests.request("POST", url, json=payload, headers=self._headers)

        if response.status_code == 200:

            data = json.loads(response.text)

            with open('hotels_id.json', 'w') as hotels_info:
                json.dump(data, hotels_info, indent=4)

        return response

    def get_hotel_information(self, low_price: bool, high_price: bool, best_deal: bool):

        with open('hotels_id.json', 'r') as my_search:

            data = json.load(my_search)
            # ищем значение для получения списка отелей
            try:
                hotels = next(self.recursion_searcher(data, 'properties'))
            except StopIteration:
                return False

            for i_num, i_key in enumerate(hotels):
                searching_data = {
                    # находи id отеля, дистанцию от центра, цену за ночь и полную стоимость за период.
                    "id": i_key.get("id"), "property": i_key.get('name'),
                    "distance": i_key.get("destinationInfo")['distanceFromDestination']['value'],
                    "cost": next((self.recursion_searcher(i_key, "formattedDisplayPrice"))),
                    'full_cost': [
                                  x[0].get('value') for x in
                                  self.recursion_searcher(i_key, 'lineItems')
                                  if isinstance(x, list) and x[0].get('value')
                                ]
                }

                self._hotels_information[i_num + 1] = searching_data  # создаем словарь с найденными значениями
            #  сортируем значения по минимальной цене (в запросе с сайта значения приходят без сортировки)
            if low_price:
                self._hotels_information = (
                    dict(sorted(self._hotels_information.items(),
                                key=lambda value: value[1]['cost'])))
            # сортируем значения по максимальной цене
            elif high_price:
                self._hotels_information = (
                    dict(sorted(self._hotels_information.items(),
                                key=lambda value: value[1]['cost'], reverse=True)))
            # сортируем отели по расстоянию от центра
            elif best_deal:
                # создаем список значений float для сравнения с дынными пользователя
                desire_distance = np.arange(int(self.distance[0]), int(self.distance[1]), 0.01)
                unfitted_hotels = []  # список для значений не подходящих под условие

                for i_kye, i_value in self._hotels_information.items():
                    # получаем значения расстояний полученных при поиске отелей в km.
                    distance = round(float(i_value.get('distance')) * 1.69, 2)
                    # добавляем неподходящие значения в список
                    if distance not in desire_distance:
                        unfitted_hotels.append(i_kye)
                # исключаем из списка неподходящие по расстоянию отели
                if len(unfitted_hotels) > 0:
                    for i in unfitted_hotels:
                        self._hotels_information.pop(i)
                # сортируем оставшиеся отели по дистанции от центра, если список пустой, возвращаем No result
                if len(self._hotels_information) > 0:

                    self._hotels_information = (
                        dict(sorted(self._hotels_information.items(),
                                    key=lambda value: value[1]['distance'])))
                else:
                    return False
        return True

    @retry_on_connection_error()
    def hotels_info(self, hotel_id: str) -> Response:

        """
           Получение информации об отеле с сервера через  API

           :arg:
               hotel_id (str):  id отеля.

           :return:
               Response: Возвращает объект API

           """

        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": f"{hotel_id}"
        }

        response = requests.request("POST", url, json=payload, headers=self._headers)
        hotel_photo = json.loads(response.text)

        with open('hotels_info.json', 'w') as photos:
            json.dump(hotel_photo, photos, indent=4)

        return response

    def hotel_information_message(self) -> Generator[str, None, None]:
        """Функция для формирования
        сообщения для вывода в чате"""

        result = []  # переменная для сохранения данных в историю поиска

        for i_value in self._hotels_information.values():
            message = f"hotel: {i_value['property']}" \
                      f"\ndistance from centre {round(i_value['distance'] * 1.69, 2)} km." \
                      f"\nprice: {i_value['cost']} per night\n" \
                      f"price for all period {i_value['full_cost'][0]}"

            result.append(message)
            yield message
            # отправляем фото если пользователь ввел соответсвующую информацию
            if self.photo:
                for i_photo in i_value['photos']:
                    message = i_photo
                    yield message

        self.result = result

    def get_hotel_photo(self, photo_quantity: str) -> None:

        """Метод для получения ссылок
        на фотографии из информации об отеле

        :param photo_quantity: Количество фотографий для вывода сообщения
        """

        hotels_id = [x.get('id') for x in self._hotels_information.values()]

        for i_num, i_value in enumerate(hotels_id):

            self.hotels_info(i_value)

            with open('hotels_info.json', 'r') as get_photo:
                # добавляем фото в информацию об отелях
                hotel_data = json.load(get_photo)
                photo_of_hotel = next(self.recursion_searcher(hotel_data, 'images'))
                photos = [i_elem.get('image')['url'] for i_elem in photo_of_hotel[:int(photo_quantity)]]
                self._hotels_information[i_num + 1]['photos'] = photos

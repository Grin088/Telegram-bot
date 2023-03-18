import json
import requests
import datetime
from math import ceil
from typing import Type, Any, Callable, Optional, Generator
from requests import Response
import functools
from config_data.config import RAPID_API_KEY
import os


def retry_on_connection_error(max_attempts: int = 10) -> Callable[[Type[Any]], Callable[..., Any]]:
    """
    Декоратор, повторяет декорированный метод класса при ошибках соединения.
    """
    def decorator(cls: Type[Any]) -> Callable[..., Any]:

        @functools.wraps(cls)
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

    __hotels_information = None
    __headers = {"X-RapidAPI-Key": RAPID_API_KEY}
    __path = os.path.abspath(os.path.join('database'))
    __city_id = None

    @classmethod
    def recursion_searcher(cls, name: dict, key: str) -> Generator:
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
                        yield from cls.recursion_searcher(i_value, key)

            elif isinstance(i_elem, dict):
                yield from cls.recursion_searcher(i_elem, key)

    @classmethod
    @retry_on_connection_error()
    def place_id_request(cls, name: str) -> Response:

        """
         Метод для получения city ID
         :param name: Name of the city

         :return: None если нет соединения с сервером или ответ сервера отрицательный
         если ответ положительный возвращает HTTP response

         """

        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": f"{name}"}

        response = requests.request("GET", url, headers=cls.__headers, params=querystring)

        if response:

            data = json.loads(response.text)

            with open(os.path.join(cls.__path, 'place_id.json'), 'w') as file:
                json.dump(data, file, indent=4)

        return response

    @classmethod
    def get_place_id(cls, country) -> bool:

        with open(os.path.join(cls.__path, 'place_id.json'), 'r') as get_city_id:
            data = json.load(get_city_id)
            city_id = [
                elem.get('gaiaId') for elem in data.get('sr', [])
                if elem.get('type') == 'CITY'
                and elem.get('hierarchyInfo')['country']['name'] == country]
            if city_id:
                cls.__city_id = city_id[0]
            else:
                return False
        return True

    @classmethod
    @retry_on_connection_error()
    def hotels_request(cls, user_data: dict) -> Response:

        """
        Метод запроса информации об отеле

        """

        check_in_date = user_data['check in'].split('.')  # создаем список для запроса дат
        check_out_date = user_data['check out'].split('.')  # создаем список для запроса дат
        find_method = user_data['find method']

        sort_method = "PRICE_LOW_TO_HIGH"

        if find_method == 'highprice':

            sort_method = 'PRICE_HIGH_TO_LOW'

        url = "https://hotels4.p.rapidapi.com/properties/v2/list"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "destination": {"regionId": f"{cls.__city_id}"},
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
            "resultsSize": int(user_data['hotel quantity']),
            "sort": sort_method,
            "filters": {"price": {
                "max": int(user_data['max price']),
                "min": int(user_data['min price'])
            }}
        }

        response = requests.request("POST", url, json=payload, headers=cls.__headers)

        if response.status_code == 200:

            data = json.loads(response.text)

            with open(os.path.join(cls.__path, 'hotels_id.json'), 'w') as hotels_info:
                json.dump(data, hotels_info, indent=4)

        return response

    @classmethod
    def get_hotel_information(cls, user_data: dict) -> bool:

        hotels_information = {}
        find_method = user_data['find method']

        with open(os.path.join(cls.__path, 'hotels_id.json'), 'r') as my_search:

            data = json.load(my_search)
            # ищем значение для получения списка отелей
            try:
                hotels = next(cls.recursion_searcher(data, 'properties'))

            except StopIteration:
                return False

            for i_num, i_key in enumerate(hotels):
                searching_data = {
                    # находи id отеля, дистанцию от центра, цену за ночь и полную стоимость за период.
                    "id": i_key.get("id"), "property": i_key.get('name'),
                    "distance": i_key.get("destinationInfo")['distanceFromDestination']['value'],
                    "cost": next((cls.recursion_searcher(i_key, "formattedDisplayPrice"))),
                    'full_cost': [
                                  x[0]['value'] for x in
                                  cls.recursion_searcher(i_key, 'lineItems')
                                  if isinstance(x, list) and x[0].get('value')
                                ][0]
                }

                hotels_information[i_num + 1] = searching_data  # создаем словарь с найденными значениями
            #  сортируем значения по минимальной цене (в запросе с сайта значения приходят без сортировки)
            if find_method == 'lowprice':
                hotels_information = sorted(hotels_information.items(), key=lambda x: x[1]['cost'])
            # сортируем значения по максимальной цене
            elif find_method == 'highprice':
                hotels_information = sorted(hotels_information.items(), key=lambda x: x[1]['cost'], reverse=True)
            # сортируем отели по расстоянию от центра
            elif find_method == 'bestdeal':

                desire_distance = list(range(int(user_data['distance'][0]), int(user_data['distance'][1]) + 1))
                # список для значений не подходящих под условие
                unfitted_hotels = [
                                   i_kye for i_kye, i_value in hotels_information.items()
                                   if ceil((i_value.get('distance')) * 1.69) not in desire_distance
                ]

                # исключаем из списка неподходящие по расстоянию отели
                for i in unfitted_hotels:
                    del hotels_information[i]
                # сортируем оставшиеся отели по дистанции от центра, если список пустой, возвращаем False
                if hotels_information:
                    hotels_information = (sorted(hotels_information.items(), key=lambda value: value[1]['distance']))
                else:
                    return False

            cls.__hotels_information = dict(hotels_information)

        return True

    @classmethod
    @retry_on_connection_error()
    def hotels_info(cls, hotel_id: str) -> Response:

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

        response = requests.request("POST", url, json=payload, headers=cls.__headers)
        hotel_photo = json.loads(response.text)

        with open(os.path.abspath(os.path.join(cls.__path, 'hotels_info.json')), 'w') as photos:
            json.dump(hotel_photo, photos, indent=4)

        return response

    @classmethod
    def get_hotel_photo(cls, photo_quantity: int) -> None:

        """
        Метод для получения ссылок
        на фотографии из информации об отеле

        :param
        photo_quantity: Количество фотографий для вывода сообщения
        """

        hotels_id = {i_key: i_values.get('id') for i_key, i_values in cls.__hotels_information.items()}

        if hotels_id:

            for i_num, i_id in hotels_id.items():

                cls.hotels_info(hotel_id=i_id)

                with open(os.path.join(cls.__path, 'hotels_info.json'), 'r') as get_photo:
                    # добавляем фото в информацию об отелях
                    hotel_data = json.load(get_photo)
                    photo_of_hotel = next(cls.recursion_searcher(hotel_data, 'images'))
                    photos = [i_elem.get('image')['url'] for i_elem in photo_of_hotel[:int(photo_quantity)]]
                    cls.__hotels_information[i_num]['photos'] = photos

    @classmethod
    def hotel_information_message(cls, photo) -> Generator[str, None, None]:

        """Метод формирования
        сообщения для вывода в чате"""

        for values in cls.__hotels_information.values():
            message = f"Hotel: {values['property']}" \
                      f"\ndistance from centre: {round(values['distance'] * 1.69, 2)} km." \
                      f"\nprice: {values['cost']} per night\n" \
                      f"price for all period {values['full_cost']}"

            yield message
            # отправляем фото если пользователь ввел соответсвующую информацию
            if photo:
                if values.get('photos'):
                    for photo_url in values['photos']:
                        message = photo_url
                        yield message

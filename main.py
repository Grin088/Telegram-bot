# импортируем необходимые библиотеки
import json
import time
import telebot
from telebot import types
import re
import datetime


# импортируем собственные классы
from step_control import StepControl  # класс для контроля чата
from user_data import DataGather  # класс для сбора информации от пользователя
from hotel_API import HotelRequest  # клас для получения информации о поиске


step_control = StepControl()  # присваиваем переменной класс для контроля чата
user_data = DataGather()  # класс для сбора данных, вводимых пользователем
hotel_data = HotelRequest()  # класс для запроса API с сервера

# Создаем инстанс Телеграмм бота используя API токен
bot = telebot.TeleBot('6104491116:AAGUUOG1pVKtmOU-7djFeEFZp6XfL7839EI')


@bot.message_handler(commands=['start', 'main', '🔙MainMenu'])
def start_message(message: json) -> None:

    """ Функция для отображения главного меню чата"""

    step_control.reset_param()  # метод класса, сбрасывает параметры
    user_data.reset_param()  # метод класса, сбрасывает параметры

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем кнопки для главного меню
    btn_find = types.KeyboardButton(text='🔎Find Hotel')  # переход в меню поиска
    btn_question = types.KeyboardButton(text='/❓Help')  # переход в меню списка команд
    btn_history = types.KeyboardButton(text='/History')  # переход в меню истории поиска
    markup.add(btn_find, btn_question, btn_history)
    answer = 'You are in Main menu'
    # приветствие бота
    if message.text == '/start':
        answer = f"👋 Hello {message.from_user.first_name}" \
                 f" I'm test bot.\nI can help you to find a Hotel of your desire!" \
                 "\nPush [🔎Find Hotel] or type /find to start searching.\n You can see all commands" \
                 " to get pushing button ❓Help or enter /help "

    bot.send_message(message.chat.id, text=answer, reply_markup=markup)
    user_data.user_id = message.from_user.id  # присваиваем переменной значение ID пользователя


@bot.message_handler(commands=['❓Help', 'help'])
def help_info(message: json) -> None:

    """Функция для вывода информации
     о командах бота на экран пользователя"""

    # текст вывода основных команд
    answer = 'Waiting answer from bot after entering information!\n'\
             'Operation code:\n' \
             '/find: start to searching hotel' \
             '/lowprice: Show result for lower price hotels.\n' \
             '/highprice: Show result for high price hotels.\n' \
             '/bestdeal: Show result for hotels with good price and good location.\n' \
             '/history: show your searching history \n' \
             '/main: return to main menu\n' \


    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['history', 'History'])
def show_history(message: json) -> None:

    """Функция для вывода на экран истории поиска"""

    user_data.user_id = message.from_user.id  # получаем ID пользователя

    # проверка и вывод информации о поиске, если ID есть в истории
    for i_elem in user_data.get_history():
        # делим строку для поиска ID пользователя и выводим результат
        if str(message.from_user.id) in i_elem.split():
            bot.send_message(message.from_user.id, text=i_elem)
        # если результата нет, выводим сообщение об отсутствии
        elif not i_elem:
            bot.send_message(message.from_user.id, text='No result')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_return = types.KeyboardButton(text='/🔙Main menu')  # клавиша для возврата в главное меню
    markup.add(btn_return)


# основной код чата
@bot.message_handler(content_types=['text'])
def menu(message: json) -> None:

    """Функция основного чата, собирает данные введенные пользователем,
     отправляет пользователю полученный результат
      и сохраняет историю поиска """

    # шаг выбора метода поиска
    if message.text in ['🔎Find Hotel', '/find']:

        # создаем кнопки для выбора метода поиска
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_low_price = types.KeyboardButton(text='🏨Low Price')
        btn_high_price = types.KeyboardButton(text='🏯High Price')
        btn_best_deal = types.KeyboardButton(text='🏩Best Deal')
        btn_return = types.KeyboardButton(text='/🔙MainMenu')
        markup.add(btn_low_price, btn_best_deal, btn_high_price, btn_return)
        bot.send_message(message.from_user.id, 'Choose method to find', reply_markup=markup)
        # переходим к шагу выбора буквы с которой начинается название страны.
        step_control.method = True
        step_control.counter = 0  # счетчик для работы с клавишами алфавита при выборе страны для поиска

    elif message.text in ['🏯High Price', '🏨Low Price', '🏩Best Deal',
                          '/lowprice', '/bestdeal', '/highprice'] and step_control.method:

        if message.text in ['🏩Best Deal', '/bestdeal']:
            user_data.best_deal = True  # присваиваем переменной значение если выбран данный метод поиска

        elif message.text in ['🏨Low Price', '/lowprice']:
            user_data.low_price = True  # присваиваем переменной значение если выбран данный метод поиска

        elif message.text in ['🏯High Price' or '/highprice']:
            user_data.high_price = True  # присваиваем переменной значение если выбран данный метод поиска

        # переходим в меню с алфавитом, для удобного ввода буквы с которой начинается название страны
        alphabet(message)  # функция отображения алфавита, для выбора первой буквы из названия страны

        # переход к шагу проверки ввода первой буквы названия страны и выбора названия страны
        step_control.method = False
        step_control.start = True

    # шаг проверки ввода буквы и выбора страны для поиска
    elif step_control.start and message.text not in ['Next', 'Back']:

        if re.match(r'^[A-Z]$', message.text):  # проверка ответа пользователя
            with open('all_countries.json', 'r') as country_list:
                data = json.load(country_list)  # загрузка файла со списком
                # создаем список с названиями стран
                result = [country for country in data.keys() if re.match(f'^{message.text}.*', country)]
                markup = types.ReplyKeyboardMarkup()
                # создаем кнопки с именами стран
                buttons = [types.KeyboardButton(text=country) for country in result]
                buttons.append(types.KeyboardButton(text='/🔙MainMenu'))
                markup.add(*buttons)
                bot.send_message(message.from_user.id, text='Choose a country', reply_markup=markup)
                # переход к проверке ввода страны и выбора города для поиска
                step_control.start = False
                step_control.country = True
        else:
            # если введена не буква, продолжаем ввод
            bot.send_message(message.from_user.id, text='Enter first letter, e.g "I"')

    # шаг проверки ввода старны и выбора города
    elif step_control.country:

        # проверяем что бы ввод сообщения с именем страны содержало только буквы и пробелы
        if re.match(r'^[a-zA-Z\s]+$', message.text):

            hotel_data.country = message.text   # переменная для проверки при поиске ID города
            # создаем кнопки с названием городов
            with open('all_countries.json', 'r') as country_list:

                data = json.load(country_list)
                # если в списке стран есть страна введенная пользователем, создаем кнопки с названиями городов
                if data.get(message.text):
                    # создаем сортированный список городов
                    result = [city for city in sorted(data.get(message.text))]
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    # создаем кнопки с названиями городов
                    buttons = [types.KeyboardButton(text=city) for city in result]
                    buttons.append(types.KeyboardButton(text='/🔙MainMenu'))
                    markup.add(*buttons)
                    bot.send_message(message.from_user.id, 'Choose a city', reply_markup=markup)
                    user_data.country = message.text
                    # переходим к шагу получения ID города и выбора количества отелей для поиска
                    step_control.country = False
                    step_control.city = True

                else:
                    # если страна не найдена предлагаем выбрать другую
                    answer = 'This country not found, choose other country'
                    bot.send_message(message.from_user.id, answer)
        else:
            answer = 'Enter name of country without digits or symbols, for e.g "Republic of Kosovo"'
            bot.send_message(message.from_user.id, answer)

    # шаг получения ID города и ввода количества от отелей
    elif step_control.city:
        # отправляем запрос на получение ID города
        result = hotel_data.country_id_request(message.text)
        print(hotel_data.get_city_id())

        if result:
            # если результат получен проверяем наличие ID города
            if result != 'Not result':
                # если ID получен выбираем количество отелей для поиска
                user_data.city = message.text
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_return = types.KeyboardButton(text='/🔙MainMenu')
                markup.add(btn_return)
                # отправляем запрос на ввод количества отелей для поиска
                answer = 'Enter quantity of hotels,  not more than 5'
                bot.send_message(message.from_user.id, text=answer, reply_markup=markup)
                # переходим к шагу проверки ввода количества отелей
                step_control.hotel_quantity = True
                step_control.city = False

            else:
                # если город не был найден отправляем сообщение пользователю
                answer = 'Sorry! We have no any result for this city, try to change parameters for search'
                bot.send_message(message.from_user.id, text=answer)

        else:

            bot.send_message(message.from_user.id, 'No internet connection, try again')

    # шаг проверки ввода количества отелей и выбора даты заезда в отель
    elif step_control.hotel_quantity:

        if re.match(r"^\d+$", message.text):
            # проверка количество отелей, введено не больше 5 отелей
            if int(message.text) <= 5:
                user_data.hotel_quantity = message.text  # переменная для поиска отелей
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_return = types.KeyboardButton(text='/🔙MainMenu')
                markup.add(btn_return)
                # отправляем запрос на ввод даты
                answer = 'Enter data for check_in in format DD MM YYYY'
                bot.send_message(message.chat.id, text=answer, reply_markup=markup)
                # переходим к шагу проверки даты и ввода даты Check out
                step_control.hotel_quantity = False
                step_control.check_in_date = True
            else:
                answer = 'Enter quantity not more than 5'
                bot.send_message(message.chat.id, text=answer)
        else:
            bot.send_message(message.from_user.id, 'Enter only digits!')
    # шаг проверки даты Check in и ввода даты Check out
    elif step_control.check_in_date:
        # проверка введенной даты Checkin
        if is_valid_date(message.text):
            # проверка: введенная Check in дата > дата сегодня
            date_now = time.strptime(str(datetime.date.today()), '%Y-%m-%d')
            check_in_date = time.strptime(message.text, '%d %m %Y')

            if date_now < check_in_date:
                user_data.check_in_date = message.text
                hotel_data.check_in = message.text
                answer = 'Enter data for check_out in format DD MM YYYY'
                bot.send_message(message.from_user.id, text=answer)
                # переходим к шагу проверки Check out даты и переходу к шагу ввода дистанции либо показа фотографий
                step_control.check_in_date = False
                step_control.check_out_date = True
            else:
                answer = f'Date for check in not be early then date now {datetime.date.today()}'
                bot.send_message(message.chat.id, text=answer)

        else:
            bot.send_message(message.chat.id, text='Enter correct format of data DD MM YYYY')
    # шаг проверки Check out даты и ввода информации о дистанции или ввода минимальной цены
    elif step_control.check_out_date:
        # проверка корректности введенной даты
        if is_valid_date(message.text):

            hotel_data.check_out = message.text
            check_in = time.strptime(hotel_data.check_in, '%d %m %Y')
            check_out = time.strptime(message.text, '%d %m %Y')
            # проверка Check in < Check out
            if check_in < check_out:

                user_data.check_out_date = message.text
                step_control.check_out_date = False
                # переходим к шагу проверки ввода дистанции и ввода минимальной цены
                if user_data.best_deal:
                    print(user_data.best_deal)
                    answer = 'Enter desire distance from centre in format: e.g 0-1, in km'
                    bot.send_message(message.chat.id, text=answer)
                    step_control.distance = True
                #  переходим к проверке ввода минимальной цены и ввода максимальной цены
                else:
                    answer = 'Enter min price in $'
                    bot.send_message(message.chat.id, text=answer)
                    step_control.min_price = True
            else:
                bot.send_message(message.chat.id, text='Check out date must be later than check in date')
        else:
            bot.send_message(message.chat.id, text='Enter correct format of data e.g 20 12 2023')
    # шаг проверки ввода дистанции и ввода минимальной цены
    elif step_control.distance:
        # проверка ввода дистанции
        if re.match(r"^\d+-\d+$", message.text):

            check_value = message.text.split('-')
            # проверка первого и второго значения при выборе дистанции
            if int(check_value[0]) < int(check_value[1]):
                answer = 'Enter min price in $'
                hotel_data.distance = message.text.split('-')
                bot.send_message(message.chat.id, text=answer)
                # переход к шагу проверки ввода минимальной цены и ввода максимальной цены
                step_control.distance = False
                step_control.min_price = True
            else:
                answer = "First number must be less then second "
                bot.send_message(message.chat.id, text=answer)

        else:
            answer = "Enter correct distance, e.g '0 1'"
            bot.send_message(message.chat.id, text=answer)

    # шаг проверки ввода минимальной цены и ввод максимальной цены
    elif step_control.min_price:
        # проверка, что введены только цифры
        if re.match(r"^\d+$", message.text):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_return = types.KeyboardButton(text='/🔙MainMenu')
            markup.add(btn_return)
            bot.send_message(message.from_user.id, 'Enter max price in $', reply_markup=markup)
            # переход к шагу проверки максимальной цены и ввода решения о получении фотографий отеля
            step_control.min_price = False
            step_control.max_price = True
            user_data.min_price = message.text  # присваиваем переменной значение минимальной цены для запроса

        else:
            bot.send_message(message.from_user.id, 'Enter only digits!')

    # шаг проверки ввода максимальной цены и ввод информации о получении фото отеля
    elif step_control.max_price:
        # проверка ввода
        if re.match(r"^\d+$", message.text):
            # проверка: минимальная цена < чем максимальная
            if int(message.text) > int(user_data.min_price):
                # создаем кнопки для выбора ответа о получении фото
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                bth_1 = types.KeyboardButton(text='Yes')
                bth_2 = types.KeyboardButton(text='No')
                btn_return = types.KeyboardButton(text='/🔙MainMenu')
                markup.add(bth_1, bth_2, btn_return)
                answer = 'Do you want to get photo of your hotel?. Enter "Yes" or "No"'
                bot.send_message(message.from_user.id, text=answer, reply_markup=markup)
                # переходим к шагу проверки ввода информации, ввода количества фотографий либо вывода результата
                step_control.max_price = False
                step_control.photos = True
                user_data.max_price = message.text  # присваиваем переменной значение максимальной цены для запроса

            else:

                answer = f'Enter number more than {user_data.min_price}'
                bot.send_message(message.from_user.id, text=answer)

        else:
            bot.send_message(message.from_user.id, 'Enter only digits!')

    # шаг проверки ввода информации о получении фото
    elif step_control.photos:

        if message.text in ['Yes', 'No']:

            if message.text == 'Yes':
                hotel_data.photo = True  # переменная для вывода результата
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_return = types.KeyboardButton(text='/🔙MainMenu')
                markup.add(btn_return)
                answer = 'Enter quantity of photos, not more than 5'
                bot.send_message(message.from_user.id, text=answer, reply_markup=markup)
                user_data.photos = True  # переменная для вывода результата
                # переходим к шагу проверки ввода количества фотографий и вывода результата
                step_control.photos = False
                step_control.photos_quantity = True

            elif message.text == 'No':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                result = types.KeyboardButton(text='Show result')
                btn_return = types.KeyboardButton(text='/🔙MainMenu')
                markup.add(result, btn_return)
                answer = "To get result. Send message: 'show result' or push button"
                bot.send_message(message.from_user.id, text=answer, reply_markup=markup)
                # переход к шагу вывода информации
                user_data.photos = False
                step_control.photos = False
                step_control.finish = True

            else:
                bot.send_message(message.chat.id, text='enter correct answer')
    # шаг проверки ввода количества фотографий и вывода результата
    elif step_control.photos_quantity:
        # проверка ввода цифр
        if re.match(r"^\d+$", message.text):
            # проверка ввода информации о количестве фото
            if int(message.text) <= 5:
                user_data.photos_quantity = message.text  # переменная для запроса количества фотографий
                # создаем кнопку для вывода результата
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                result = types.KeyboardButton(text='Show result')
                btn_return = types.KeyboardButton(text='/🔙MainMenu')
                markup.add(result, btn_return)
                answer = 'To get result , send: show result or push button'
                bot.send_message(message.from_user.id, text=answer, reply_markup=markup)
                # переходим к шагу вывода результата
                step_control.photos_quantity = False
                step_control.finish = True
            else:
                bot.send_message(message.from_user.id, text='Enter number less or equal 5')

        else:

            bot.send_message(message.from_user.id, text='Enter only digits')

    elif step_control.finish:

        if message.text == 'Show result':
            # отправляем запрос на сервер HOTELS используя API
            hotels_request = hotel_data.find_hotels(min_price=user_data.min_price, max_price=user_data.max_price,
                                                    high_price=user_data.best_deal, quantity=user_data.hotel_quantity)
            # проверка ответа от сервера
            if hotels_request:
                # проверка результата по запросу
                hotel_data.get_hotel_information(low_price=user_data.low_price, high_price=user_data.low_price,
                                                 best_deal=user_data.best_deal)
                if hotel_data:
                    # Запрашиваем фото отеля, если выбран пункт "show photo"
                    if user_data.photos:
                        hotel_data.get_hotel_photo(user_data.photos_quantity)

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn_return = types.KeyboardButton(text='/🔙MainMenu')
                    markup.add(btn_return)
                    # выводим полученную информацию
                    for i_message in hotel_data.hotel_information_message():
                        bot.send_message(message.chat.id, text=i_message)
                    # сохраняем результат поиска
                    user_data.save_search_history([str(y) for x in hotel_data.result for y in x.split('\n')])
                    bot.send_message(message.chat.id, text='/start')
                    step_control.finish = False
                else:
                    # сохраняем результат поиска
                    user_data.save_search_history(result='No result')
                    answer = 'No result for your request, try to change searching parameters'
                    bot.send_message(message.chat.id, text=answer)
            else:

                bot.send_message(message.chat.id, text='Sorry, No internet connection!')
        else:
            bot.send_message(message.chat.id, text='Enter "Show result or push button')
    # шаг для управления алфавитом
    elif message.text == 'Next' and step_control.start:

        step_control.counter += 1
        alphabet(message)
    # шаг для управления алфавитом
    elif message.text == 'Back' and step_control.start:

        step_control.counter -= 1
        alphabet(message)


def alphabet(message: json) -> None:

    """
    Функция для отображения алфавита с 3 мя
    вариантами клавиатуры

    """

    alphabet_list = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
    letters = alphabet_list[:9] if step_control.counter == 0 \
        else(alphabet_list[9:18] if step_control.counter == 1 else alphabet_list[18:26])

    print(step_control.counter)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text=letter) for letter in letters]
    buttons.append(types.KeyboardButton(text='/🔙MainMenu'))

    if step_control.counter == 0:

        buttons.append(types.KeyboardButton(text='Next'))

    elif step_control.counter == 1:

        buttons.append(types.KeyboardButton(text='Back'))
        buttons.append(types.KeyboardButton(text='Next'))

    elif step_control.counter == 2:

        buttons.append(types.KeyboardButton(text='Back'))

    markup.add(*buttons)
    bot.send_message(message.from_user.id, 'Choose a start letter of country name', reply_markup=markup)


def is_valid_date(date_text: str) -> bool:

    """Функция проверки корректности
    введенной даты
    """

    try:
        datetime.datetime.strptime(date_text, '%d %m %Y')
        return True

    except ValueError:
        return False


bot.polling(none_stop=True)

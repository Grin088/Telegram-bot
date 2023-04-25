from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.start import start_keyboard
from keyboards.reply.alphabet import AlphaBet



@bot.message_handler(commands=["main", '🔙MainMenu'])
def main_menu(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.main, message.chat.id)
    answer = 'You are in main menu'
    bot.send_message(message.from_user.id, text=answer, reply_markup=start_keyboard())


@bot.message_handler(commands=['🏯HighPrice', '🏨LowPrice', '🏩BestDeal',
                               'lowprice', 'bestdeal', 'highprice'])
def survey(message: Message) -> None:

    bot.set_state(message.from_user.id, UserRequestState.start, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_id'] = message.from_user.id
        data['find method'] = message.text.strip('/🏩🏯🏩').lower()

    answer = "Chose or enter first letter of country name, e.g 'E'"
    bot.send_message(message.from_user.id, text=answer, reply_markup=next(AlphaBet.alphabet(message)))


# @bot.message_handler(state=UserRequestState.start)
# def alphabet_step(message: Message) -> None:
#
#     match_obj = match(r'^[A-Z]$', message.text)
#
#     if match_obj:
#
#         bot.set_state(message.from_user.id, UserRequestState.country, message.chat.id)
#         answer = 'Enter or chose name of country'
#         bot.send_message(message.from_user.id, text=answer, reply_markup=all_country_keyboard(message.text.title()))
#
#     elif message.text in ['Next', 'Back']:
#         bot.send_message(message.from_user.id, text=message.text, reply_markup=next(AlphaBet.alphabet(message)))
#
#     else:
#         bot.send_message(message.from_user.id, text='Enter first letter of country name')


# @bot.message_handler(state=UserRequestState.country)
# def country_step(message: Message) -> None:
#
#     match_obj = match(r'^[a-zA-Z\s]+$', message.text)
#
#     if match_obj:
#
#         if cities_keyboard(message.text):
#
#             bot.set_state(message.from_user.id, UserRequestState.city, message.chat.id)
#             with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#                 data['country'] = message.text
#
#             answer = 'Enter or chose name of city'
#             bot.send_message(message.from_user.id, text=answer, reply_markup=cities_keyboard(message.text))
#
#         else:
#             answer = 'This country not found, enter other name of country'
#             bot.send_message(message.from_user.id, text=answer)


# @bot.message_handler(state=UserRequestState.city)
# def city_step(message: Message) -> None:
#
#     match_obj = match(r'^[a-zA-Z\s-]+$', message.text)
#
#     if match_obj:
#         if HotelRequest.place_id_request(message.text):
#
#             with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#                 if HotelRequest.get_place_id(data['country']):
#                     data['city'] = message.text
#                     bot.set_state(message.from_user.id, UserRequestState.hotel_quantity, message.chat.id)
#                     answer = 'Enter quantity of hotels. Not more than 5'
#                     bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())
#
#                 else:
#                     answer = 'This city is not founded, enter other name or return to main menu'
#                     bot.send_message(message.from_user.id, text=answer)
#         else:
#             answer = 'Sorry. No response from server, try again'
#             bot.send_message(message.from_user.id, text=answer)
#     else:
#         answer = 'Enter name of country without digits or symbols, for e.g "Republic of Kosovo"'
#         bot.send_message(message.from_user.id, answer)


# @bot.message_handler(state=UserRequestState.hotel_quantity)
# def hotel_quantity_step(message: Message) -> None:
#
#     if message.text.isdigit():
#         # проверка количество отелей, введено не больше 5 отелей
#         if int(message.text) <= 5:
#
#             with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#                 data['hotel quantity'] = message.text
#
#             bot.set_state(message.from_user.id, UserRequestState.check_in_date, message.chat.id)
#             # отправляем запрос на ввод даты
#             answer = 'Enter check_in date in format DD.MM.YYYY for e.g 01.03.2023'
#             bot.send_message(message.chat.id, text=answer, reply_markup=return_keyboard())
#             # переходим к шагу проверки даты и ввода даты Check out
#
#         else:
#             answer = 'Enter quantity not more than 5'
#             bot.send_message(message.chat.id, text=answer)
#     else:
#         bot.send_message(message.from_user.id, 'Enter only digits!')


# @bot.message_handler(state=UserRequestState.check_in_date)
# def check_in_step(message: Message) -> None:
#
#     if CheckDate.is_valid_date(message.text):
#         # проверка: введенная Check in дата > дата сегодня
#         if CheckDate.later_date(message.text):
#
#             with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#                 data['check in'] = message.text
#             answer = 'Enter check_out date in format DD.MM.YYYY for e.g 10.03.2023'
#             bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())
#             bot.set_state(message.from_user.id, UserRequestState.check_out_date, message.chat.id)
#
#         else:
#             answer = f'Date for check in must be later then date now'
#             bot.send_message(message.chat.id, text=answer)
#
#     else:
#         bot.send_message(message.chat.id, text='Enter correct format of data DD.MM.YYYY')


# @bot.message_handler(state=UserRequestState.check_out_date)
# def check_out_step(message: Message) -> None:
#
#     if CheckDate.is_valid_date(message.text):
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#
#             if CheckDate.compare_date(data['check in'], message.text):
#
#                 data['check out'] = message.text
#
#                 if data['find method'] == 'bestdeal':
#
#                     bot.set_state(message.from_user.id, UserRequestState.distance, message.chat.id)
#                     answer = 'Enter desire distance from centre in format: e.g 0-1, in km'
#                     bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())
#
#                 else:
#
#                     bot.set_state(message.from_user.id, UserRequestState.min_price, message.chat.id)
#                     answer = 'Enter minimum price per night in $. For e.g "100"'
#                     bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())
#
#             else:
#                 bot.send_message(message.chat.id, text='Check out date must be later than check in date')
#     else:
#         bot.send_message(message.chat.id, text='Enter correct format of data e.g "10.03.2023"')


# @bot.message_handler(state=UserRequestState.distance)
# def distance_step(message: Message) -> None:
#
#     match_obj = match(r"^\d+-\d+$", message.text)
#     if match_obj:
#
#         check_value = message.text.split('-')
#         # проверка первого и второго значения при выборе дистанции
#         if int(check_value[0]) < int(check_value[1]):
#
#             with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#                 data['distance'] = message.text.split('-')
#
#             bot.set_state(message.from_user.id, UserRequestState.min_price, message.chat.id)
#             answer = 'Enter minimum price per night in $. For e.g "100"'
#             bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())
#
#         else:
#             answer = "First number must be less then second number"
#             bot.send_message(message.chat.id, text=answer)
#
#     else:
#         answer = 'Enter correct distance, e.g "0-1"'
#         bot.send_message(message.chat.id, text=answer)


# @bot.message_handler(state=UserRequestState.min_price)
# def min_price_step(message: Message) -> None:
#     # проверка, что введены только цифры
#     if message.text.isdigit():
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['min price'] = message.text
#
#         bot.set_state(message.from_user.id, UserRequestState.max_price, message.chat.id)
#         answer = 'Enter maximum price per night in $. For e.g "200"'
#         bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())
#
#     else:
#         bot.send_message(message.from_user.id, text='Enter only digits!')


# @bot.message_handler(state=UserRequestState.max_price)
# def max_price_step(message: Message) -> None:
#
#     if message.text.isdigit():
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             if int(data['min price']) < int(message.text):
#                 data['max price'] = message.text
#
#                 bot.set_state(message.from_user.id, UserRequestState.photos, message.chat.id)
#                 answer = 'Do you want to get photo of hotels?'
#                 bot.send_message(message.from_user.id, text=answer, reply_markup=yes_no_keyboard())
#
#             else:
#                 answer = f'Max price mus be more than {data["min price"]}'
#                 bot.send_message(message.from_user.id, text=answer)
#     else:
#         bot.send_message(message.from_user.id, text='Enter only digits!')


# @bot.message_handler(state=UserRequestState.photos)
# def get_photo_step(message: Message) -> None:
#
#     if message.text in ['yes', 'Yes']:
#         answer = 'Enter quantity of photos, not more than 5'
#         bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())
#         bot.set_state(message.from_user.id, UserRequestState.photos_quantity, message.chat.id)
#
#     elif message.text in ['no', 'No']:
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['photo quantity'] = None
#         answer = 'To get result enter "show" or push the button "show result"'
#         bot.send_message(message.from_user.id, text=answer, reply_markup=show_result_button())
#         bot.set_state(message.from_user.id, UserRequestState.finish, message.chat.id)
#
#     else:
#         bot.send_message(message.from_user.id, text='Enter "yes" or "no"')


# @bot.message_handler(state=UserRequestState.photos_quantity)
# def photo_quantity_step(message: Message) -> None:
#
#     if match(r"^\d+$", message.text):
#
#         if int(message.text) <= 5:
#
#             with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#                 data['photo quantity'] = message.text
#             answer = 'To get result enter "show" or push the button "show result"'
#             bot.send_message(message.from_user.id, text=answer, reply_markup=show_result_button())
#             bot.set_state(message.from_user.id, UserRequestState.finish, message.chat.id)
#
#         else:
#             bot.send_message(message.from_user.id, text='Enter number less or equal 5')
#     else:
#         bot.send_message(message.from_user.id, text='Enter only digits')


# @bot.message_handler(state=UserRequestState.finish)
# def finish_step(message: Message) -> None:
#
#     if message.text == 'Show result':
#
#         photo = False
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#
#             if HotelRequest.hotels_request(data):
#
#                 if HotelRequest.get_hotel_information(data):
#
#                     bot.send_message(message.chat.id, text='Waiting for result', reply_markup=return_keyboard())
#
#                     if data.get('photo quantity'):
#                         photo = True
#                         HotelRequest.get_hotel_photo(data['photo quantity'])
#
#                     result = []
#
#                     for i_elem in HotelRequest.hotel_information_message(photo):
#
#                         if not isinstance(i_elem, list):
#                             bot.send_message(message.from_user.id, text=i_elem)
#                             result.append(i_elem)
#
#                         elif isinstance(i_elem, list) and photo:
#                             photos = [InputMediaPhoto(link) for link in i_elem]
#                             bot.send_media_group(message.from_user.id, media=photos)
#
#                     History.save_search_history(user_id=message.from_user.id, data=data, result=result)
#
#                 else:
#
#                     History.save_search_history(user_id=message.from_user.id, data=data, result='No result')
#                     answer = 'No result for your request, try to change searching parameters'
#                     bot.send_message(message.chat.id, text=answer, reply_markup=return_keyboard())
#
#             else:
#
#                 bot.send_message(message.chat.id, text='Sorry, No internet connection!')
#     else:
#         bot.send_message(message.chat.id, text='Enter "Show result or push button')

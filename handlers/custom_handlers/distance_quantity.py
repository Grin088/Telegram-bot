from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.return_keyboard import return_keyboard
from re import match


@bot.message_handler(state=UserRequestState.hotel_quantity)
def hotel_quantity_step(message: Message) -> None:

    if message.text.isdigit():
        # проверка количество отелей, введено не больше 5 отелей
        if int(message.text) <= 5:

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['hotel quantity'] = message.text

            bot.set_state(message.from_user.id, UserRequestState.check_in_date, message.chat.id)
            # отправляем запрос на ввод даты
            answer = 'Enter check_in date in format DD.MM.YYYY for e.g 01.03.2023'
            bot.send_message(message.chat.id, text=answer, reply_markup=return_keyboard())
            # переходим к шагу проверки даты и ввода даты Check out

        else:
            answer = 'Enter quantity not more than 5'
            bot.send_message(message.chat.id, text=answer)
    else:
        bot.send_message(message.from_user.id, 'Enter only digits!')


@bot.message_handler(state=UserRequestState.distance)
def distance_step(message: Message) -> None:

    match_obj = match(r"^\d+-\d+$", message.text)
    if match_obj:

        check_value = message.text.split('-')
        # проверка первого и второго значения при выборе дистанции
        if int(check_value[0]) < int(check_value[1]):

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['distance'] = message.text.split('-')

            bot.set_state(message.from_user.id, UserRequestState.min_price, message.chat.id)
            answer = 'Enter minimum price per night in $. For e.g "100"'
            bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())

        else:
            answer = "First number must be less then second number"
            bot.send_message(message.chat.id, text=answer)

    else:
        answer = 'Enter correct distance, e.g "0-1"'
        bot.send_message(message.chat.id, text=answer)

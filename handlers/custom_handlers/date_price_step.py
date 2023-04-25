from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.return_keyboard import return_keyboard
from utils.misc.check_date_time import CheckDate
from keyboards.reply.yes_no import yes_no_keyboard


@bot.message_handler(state=UserRequestState.check_in_date)
def check_in_step(message: Message) -> None:

    if CheckDate.is_valid_date(message.text):
        # проверка: введенная Check in дата > дата сегодня
        if CheckDate.later_date(message.text):

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['check in'] = message.text
            answer = 'Enter check_out date in format DD.MM.YYYY for e.g 10.03.2023'
            bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())
            bot.set_state(message.from_user.id, UserRequestState.check_out_date, message.chat.id)

        else:
            answer = f'Date for check in must be later then date now'
            bot.send_message(message.chat.id, text=answer)

    else:
        bot.send_message(message.chat.id, text='Enter correct format of data DD.MM.YYYY')


@bot.message_handler(state=UserRequestState.check_out_date)
def check_out_step(message: Message) -> None:

    if CheckDate.is_valid_date(message.text):

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

            if CheckDate.compare_date(data['check in'], message.text):

                data['check out'] = message.text

                if data['find method'] == 'bestdeal':

                    bot.set_state(message.from_user.id, UserRequestState.distance, message.chat.id)
                    answer = 'Enter desire distance from centre in format: e.g 0-1, in km'
                    bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())

                else:

                    bot.set_state(message.from_user.id, UserRequestState.min_price, message.chat.id)
                    answer = 'Enter minimum price per night in $. For e.g "100"'
                    bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())

            else:
                bot.send_message(message.chat.id, text='Check out date must be later than check in date')
    else:
        bot.send_message(message.chat.id, text='Enter correct format of data e.g "10.03.2023"')


@bot.message_handler(state=UserRequestState.min_price)
def min_price_step(message: Message) -> None:
    # проверка, что введены только цифры
    if message.text.isdigit():

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price'] = message.text

        bot.set_state(message.from_user.id, UserRequestState.max_price, message.chat.id)
        answer = 'Enter maximum price per night in $. For e.g "200"'
        bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())

    else:
        bot.send_message(message.from_user.id, text='Enter only digits!')


@bot.message_handler(state=UserRequestState.max_price)
def max_price_step(message: Message) -> None:
    if message.text.isdigit():

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if int(data['min_price']) < int(message.text):
                data['max_price'] = message.text

                bot.set_state(message.from_user.id, UserRequestState.photos, message.chat.id)
                answer = 'Do you want to get photo of hotels?'
                bot.send_message(message.from_user.id, text=answer, reply_markup=yes_no_keyboard())

            else:
                answer = f'Max price mus be more than {data["min_price"]}'
                bot.send_message(message.from_user.id, text=answer)
    else:
        bot.send_message(message.from_user.id, text='Enter only digits!')

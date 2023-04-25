from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.return_keyboard import return_keyboard
from utils.misc.check_date_time import CheckDate


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

from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.return_keyboard import return_keyboard
from re import match


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
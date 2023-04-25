from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.cities import cities_keyboard
from re import match


@bot.message_handler(state=UserRequestState.country)
def country_step(message: Message) -> None:

    match_obj = match(r'^[a-zA-Z\s]+$', message.text)

    if match_obj:

        if cities_keyboard(message.text):

            bot.set_state(message.from_user.id, UserRequestState.city, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['country'] = message.text

            answer = 'Enter or chose name of city'
            bot.send_message(message.from_user.id, text=answer, reply_markup=cities_keyboard(message.text))

        else:
            answer = 'This country not found, enter other name of country'
            bot.send_message(message.from_user.id, text=answer)
from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.return_keyboard import return_keyboard
from re import match
from utils.misc.hotel_API_request import HotelRequest


@bot.message_handler(state=UserRequestState.city)
def city_step(message: Message) -> None:

    match_obj = match(r'^[a-zA-Z\s-]+$', message.text)

    if match_obj:
        if HotelRequest.place_id_request(message.text):

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                if HotelRequest.get_place_id(data['country']):
                    data['city'] = message.text
                    bot.set_state(message.from_user.id, UserRequestState.hotel_quantity, message.chat.id)
                    answer = 'Enter quantity of hotels. Not more than 5'
                    bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())

                else:
                    answer = 'This city is not founded, enter other name or return to main menu'
                    bot.send_message(message.from_user.id, text=answer)
        else:
            answer = 'Sorry. No response from server, try again'
            bot.send_message(message.from_user.id, text=answer)
    else:
        answer = 'Enter name of country without digits or symbols, for e.g "Republic of Kosovo"'
        bot.send_message(message.from_user.id, answer)
from loader import bot
from telebot.types import Message, InputMediaPhoto
from states.user_states import UserRequestState
from keyboards.reply.return_keyboard import return_keyboard
from utils.misc.hotel_API_request import HotelRequest
from utils.misc.get_save_history import ChatHistory


@bot.message_handler(state=UserRequestState.finish)
def finish_step(message: Message) -> None:

    if message.text == 'Show result':

        photo = False

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

            if HotelRequest.hotels_request(data):

                if HotelRequest.get_hotel_information(data):

                    bot.send_message(message.chat.id, text='Waiting for result', reply_markup=return_keyboard())

                    if data.get('photo quantity'):
                        photo = True
                        HotelRequest.get_hotel_photo(data['photo quantity'])

                    result = []

                    for i_elem in HotelRequest.hotel_information_message(photo):

                        if not isinstance(i_elem, list):
                            bot.send_message(message.from_user.id, text=i_elem)
                            result.append(i_elem)

                        elif isinstance(i_elem, list) and photo:
                            photos = [InputMediaPhoto(link) for link in i_elem]
                            bot.send_media_group(message.from_user.id, media=photos)

                    ChatHistory.insert_variable_into_table(data=data, result=result)

                else:

                    ChatHistory.insert_variable_into_table(data=data, result=False)
                    answer = 'No result for your request, try to change searching parameters'
                    bot.send_message(message.chat.id, text=answer, reply_markup=return_keyboard())

            else:

                bot.send_message(message.chat.id, text='Sorry, No internet connection!')
    else:
        bot.send_message(message.chat.id, text='Enter "Show result or push button')

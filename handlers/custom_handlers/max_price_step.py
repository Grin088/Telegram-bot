from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.yes_no import yes_no_keyboard


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

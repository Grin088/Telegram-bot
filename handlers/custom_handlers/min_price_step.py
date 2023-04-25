from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.return_keyboard import return_keyboard


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
from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.show_result import show_result_button
from re import match


@bot.message_handler(state=UserRequestState.photos_quantity)
def photo_quantity_step(message: Message) -> None:

    if match(r"^\d+$", message.text):

        if int(message.text) <= 5:

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['photo quantity'] = message.text
            answer = 'To get result enter "show" or push the button "show result"'
            bot.send_message(message.from_user.id, text=answer, reply_markup=show_result_button())
            bot.set_state(message.from_user.id, UserRequestState.finish, message.chat.id)

        else:
            bot.send_message(message.from_user.id, text='Enter number less or equal 5')
    else:
        bot.send_message(message.from_user.id, text='Enter only digits')
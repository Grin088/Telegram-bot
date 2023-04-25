from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.return_keyboard import return_keyboard
from keyboards.reply.show_result import show_result_button


@bot.message_handler(state=UserRequestState.photos)
def get_photo_step(message: Message) -> None:

    if message.text in ['yes', 'Yes']:
        answer = 'Enter quantity of photos, not more than 5'
        bot.send_message(message.from_user.id, text=answer, reply_markup=return_keyboard())
        bot.set_state(message.from_user.id, UserRequestState.photos_quantity, message.chat.id)

    elif message.text in ['no', 'No']:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo quantity'] = None
        answer = 'To get result enter "show" or push the button "show result"'
        bot.send_message(message.from_user.id, text=answer, reply_markup=show_result_button())
        bot.set_state(message.from_user.id, UserRequestState.finish, message.chat.id)

    else:
        bot.send_message(message.from_user.id, text='Enter "yes" or "no"')

from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.return_keyboard import return_keyboard
from utils.misc.check_date_time import CheckDate


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
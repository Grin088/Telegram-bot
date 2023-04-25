from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.alphabet import AlphaBet
from keyboards.reply.all_countries import all_country_keyboard
from re import match


@bot.message_handler(state=UserRequestState.start)
def alphabet_step(message: Message) -> None:

    match_obj = match(r'^[A-Z]$', message.text)

    if match_obj:

        bot.set_state(message.from_user.id, UserRequestState.country, message.chat.id)
        answer = 'Enter or chose name of country'
        bot.send_message(message.from_user.id, text=answer, reply_markup=all_country_keyboard(message.text.title()))

    elif message.text in ['Next', 'Back']:
        bot.send_message(message.from_user.id, text=message.text, reply_markup=next(AlphaBet.alphabet(message)))

    else:
        bot.send_message(message.from_user.id, text='Enter first letter of country name')
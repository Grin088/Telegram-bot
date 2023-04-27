from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.start import start_keyboard
from keyboards.reply.alphabet import AlphaBet


@bot.message_handler(commands=["main", '🔙MainMenu'])
def main_menu(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.main, message.chat.id)
    answer = 'You are in main menu'
    bot.send_message(message.from_user.id, text=answer, reply_markup=start_keyboard())


@bot.message_handler(commands=['🏯HighPrice', '🏨LowPrice', '🏩BestDeal',
                               'lowprice', 'bestdeal', 'highprice'])
def survey(message: Message) -> None:

    bot.set_state(message.from_user.id, UserRequestState.start, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_id'] = message.from_user.id
        data['find method'] = message.text.strip('/🏩🏯🏩').lower()

    answer = "Chose or enter first letter of country name, e.g 'E'"
    bot.send_message(message.from_user.id, text=answer, reply_markup=next(AlphaBet.alphabet(message)))

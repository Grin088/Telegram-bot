from loader import bot
from telebot.types import Message
from states.user_states import UserRequestState
from keyboards.reply.return_keyboard import return_keyboard


@bot.message_handler(state=UserRequestState.hotel_quantity)
def hotel_quantity_step(message: Message) -> None:

    if message.text.isdigit():
        # проверка количество отелей, введено не больше 5 отелей
        if int(message.text) <= 5:

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['hotel quantity'] = message.text

            bot.set_state(message.from_user.id, UserRequestState.check_in_date, message.chat.id)
            # отправляем запрос на ввод даты
            answer = 'Enter check_in date in format DD.MM.YYYY for e.g 01.03.2023'
            bot.send_message(message.chat.id, text=answer, reply_markup=return_keyboard())
            # переходим к шагу проверки даты и ввода даты Check out

        else:
            answer = 'Enter quantity not more than 5'
            bot.send_message(message.chat.id, text=answer)
    else:
        bot.send_message(message.from_user.id, 'Enter only digits!')
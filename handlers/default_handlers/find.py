from telebot.types import Message
from keyboards.reply.hotel_find_method import chose_method
from loader import bot


@bot.message_handler(commands=["find", "🔎FindHotel"])
def statr_searching(message: Message):
    answer = 'Chose method to find hotel'
    bot.send_message(message.from_user.id, answer, reply_markup=chose_method())

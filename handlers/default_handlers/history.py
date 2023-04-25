from telebot.types import Message
from loader import bot
from keyboards.reply.start import start_keyboard
from utils.misc.get_save_history import ChatHistory


@bot.message_handler(commands=["History", "history"])
def show_history(message: Message) -> None:

    """Функция для вывода на экран истории поиска"""

    # проверка и вывод информации о поиске, если ID есть в истории
    if next(ChatHistory.create_message(message.from_user.id)):
        for text in ChatHistory.create_message(message.from_user.id):
            bot.send_message(message.from_user.id, text=text, reply_markup=start_keyboard())
    else:
        bot.send_message(message.from_user.id, text='No history', reply_markup=start_keyboard())



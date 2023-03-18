from telebot.types import Message
from utils.misc.history import History
from loader import bot
from keyboards.reply.start import start_keyboard



@bot.message_handler(commands=["History", "history"])
def show_history(message: Message) -> None:

    """Функция для вывода на экран истории поиска"""

    # проверка и вывод информации о поиске, если ID есть в истории
    for i_elem in History.get_history(message.from_user.id):
        # делим строку для поиска ID пользователя и выводим результат
        if str(message.from_user.id) in i_elem.split():
            bot.send_message(message.from_user.id, text=i_elem, reply_markup=start_keyboard())
        # если результата нет, выводим сообщение об его отсутствии
        elif not i_elem:
            bot.send_message(message.from_user.id, text='No result', reply_markup=start_keyboard())

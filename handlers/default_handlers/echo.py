from telebot.types import Message
from loader import bot


@bot.message_handler(commands=None)
def unfitted_commands(message: Message) -> None:
    answer = 'I dont know this command. Use /help to show all commands'
    bot.send_message(message.from_user.id, text=answer)


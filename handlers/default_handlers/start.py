from telebot.types import Message
from keyboards.reply.start import start_keyboard
from loader import bot


@bot.message_handler(commands=["start", "main", '🔙MainMenu'])
def start_menu(message: Message) -> None:

    if message.text == '/start':
        answer = f"👋 Hello {message.from_user.first_name}" \
                 f" I'm test bot.\nI can help you to find a Hotel of your desire!" \
                 "\nPush \n[🔎Find Hotel]\n or enter /find to start searching.\n To see all commands" \
                 " push the button\n[❓Help]\nor enter /help "
    else:
        answer = 'You are in main menu'
    bot.send_message(message.from_user.id, text=answer, reply_markup=start_keyboard())

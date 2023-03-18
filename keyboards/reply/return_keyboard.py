
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def return_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text='/🔙MainMenu'))
    return markup

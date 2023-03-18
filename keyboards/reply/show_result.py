from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def show_result_button() -> ReplyKeyboardMarkup:

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text='Show result'))
    return markup


from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def yes_no_keyboard() -> ReplyKeyboardMarkup:

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    bth_1 = KeyboardButton(text='Yes')
    bth_2 = KeyboardButton(text='No')
    btn_return = KeyboardButton(text='/🔙MainMenu')
    markup.add(bth_1, bth_2, btn_return)

    return markup


from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def chose_method() -> ReplyKeyboardMarkup:

    markup = ReplyKeyboardMarkup(True, True)
    btn_low_price = KeyboardButton(text='/🏨LowPrice')
    btn_high_price = KeyboardButton(text='/🏯HighPrice')
    btn_best_deal = KeyboardButton(text='/🏩BestDeal')
    btn_return = KeyboardButton(text='/🔙MainMenu')
    markup.add(btn_low_price, btn_best_deal, btn_high_price, btn_return)
    return markup

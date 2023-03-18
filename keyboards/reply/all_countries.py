
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
import json
from re import match


def all_country_keyboard(message):

    path = os.path.abspath(os.path.join('database', 'all_countries.json'))

    with open(path, 'r') as country_list:
        data = json.load(country_list)
    # создаем список с названиями стран
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # создаем кнопки с именами стран
    buttons = [KeyboardButton(text=country) for country in data.keys() if match(f'^{message}.*', country)]
    buttons.append(KeyboardButton(text='/🔙MainMenu'))
    markup.add(*buttons)
    return markup

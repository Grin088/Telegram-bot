
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import os
import json


def cities_keyboard(message: str) -> ReplyKeyboardMarkup | bool:

    path = os.path.abspath(os.path.join('database', 'all_countries.json'))
    with open(path, 'r') as country_list:
        data = json.load(country_list)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    result = data.get(message)

    if result:
        buttons = [KeyboardButton(text=city) for city in sorted(result)]
        buttons.append(KeyboardButton(text='/🔙MainMenu'))
        markup.add(*buttons)
        return markup
    else:
        return False



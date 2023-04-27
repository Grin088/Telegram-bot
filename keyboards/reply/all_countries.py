from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from database.all_countries import AllCountries
from re import match


def all_country_keyboard(message):

    data = AllCountries.get_country_dict()
    # создаем список с названиями стран
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # создаем кнопки с именами стран
    buttons = [KeyboardButton(text=country) for country in data.keys() if match(f'^{message}.*', country)]
    buttons.append(KeyboardButton(text='/🔙MainMenu'))
    markup.add(*buttons)
    return markup

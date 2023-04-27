from database.all_countries import AllCountries
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def cities_keyboard(message: str) -> ReplyKeyboardMarkup | bool:

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    result = AllCountries.get_cities(message)
    if result:
        buttons = [KeyboardButton(text=city) for city in sorted(result)]
        buttons.append(KeyboardButton(text='/🔙MainMenu'))
        markup.add(*buttons)
        return markup
    else:
        return False



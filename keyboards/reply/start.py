from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def start_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(True, True)  # создаем кнопки для главного меню

    btn_find = KeyboardButton(text='/🔎FindHotel')  # переход в меню поиска
    btn_question = KeyboardButton(text='/❓Help')  # переход в меню списка команд
    btn_history = KeyboardButton(text='/History')  # переход в меню истории поиска
    markup.add(btn_find, btn_question, btn_history)
    return markup

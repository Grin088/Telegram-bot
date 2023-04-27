
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
from typing import Generator


class AlphaBet:

    __step_counter = 0

    @classmethod
    def alphabet(cls, message: Message) -> Generator:

        """
        Метод для отображения алфавита с 3 мя
        вариантами клавиатуры

        """
        if message.text == 'Next':
            cls.__step_counter += 1

        elif message.text == 'Back':
            cls.__step_counter -= 1

        alphabet_list = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
        letters = alphabet_list[:9] if cls.__step_counter == 0 \
            else(alphabet_list[9:18] if cls.__step_counter == 1 else alphabet_list[18:26])

        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = [KeyboardButton(text=letter) for letter in letters]
        buttons.append(KeyboardButton(text='/🔙MainMenu'))

        if cls.__step_counter == 0:

            buttons.append(KeyboardButton(text='Next'))

        elif cls.__step_counter == 1:

            buttons.append(KeyboardButton(text='Back'))
            buttons.append(KeyboardButton(text='Next'))

        elif cls.__step_counter == 2:

            buttons.append(KeyboardButton(text='Back'))

        markup.add(*buttons)
        yield markup



from datetime import datetime, date
import time

class CheckDate:

    @classmethod
    def is_valid_date(cls,date_text: str) -> bool:

        """Функция проверки корректности
        введенной даты
        """

        try:
            datetime.strptime(date_text, '%d.%m.%Y')
            return True

        except ValueError:
            return False

    @classmethod
    def later_date(cls, date_text: str) -> bool:

        """Функция для проверки текущей даты
        и даты заселения в отель"""

        date_now = time.strptime(str(date.today()), '%Y-%m-%d')
        check_in_date = time.strptime(date_text, '%d.%m.%Y')

        if date_now < check_in_date:
            return True

        return False

    @classmethod
    def compare_date(cls, date_check_in: str, date_check_out) -> bool:

        """Функция для проверки даты въезда и выезда из отеля"""

        check_in = time.strptime(date_check_in, '%d.%m.%Y')
        check_out = time.strptime(date_check_out, '%d.%m.%Y')

        if check_in < check_out:
            return True

        return False

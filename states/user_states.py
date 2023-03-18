from telebot.handler_backends import State, StatesGroup


class UserRequestState(StatesGroup):

    main = State()
    start = State()
    find_method = State()
    alphabet = State()
    country = State()
    city = State()
    hotel_quantity = State()
    check_in_date = State()
    check_out_date = State()
    distance = State()
    min_price = State()
    max_price = State()
    photos = State()
    photos_quantity = State()
    finish = State()

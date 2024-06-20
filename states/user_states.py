from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    user_in_cart = State()
    user_in_product = State()
    user_show_products = State()
    user_sub_category = State()
    user_up_category = State()
    change_language = State()
    change_phone = State()
    change_name = State()
    settings = State()
    user_menu = State()
    phone_number = State()
    first_name = State()
    choice_language = State()
    select_sum = State()

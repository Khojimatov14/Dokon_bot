from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    add_product_photos = State()
    add_product_description_uzbek = State()
    add_product_description_russia = State()
    add_product_description_usa = State()
    add_product_price = State()
    add_product_name = State()
    add_debit_card_number = State()
    add_product_sub_category = State()
    add_product_up_category = State()
    admin_add_sub_category_text = State()
    admin_add_sub_category = State()
    admin_add_up_category = State()
    admin_delete_category = State()
    admin_delete_data = State()
    admin_add_data = State()
    admin_add_category = State()
    admin = State()
from math import ceil
from data import ADMINS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def brand_keyboards():
    keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="EPA", callback_data="epa"),
            ],
            [
                InlineKeyboardButton(text="POLLWON", callback_data="pollwon"),
            ],
            [
                InlineKeyboardButton(text="back", callback_data="back"),
            ]
        ]
    )
    return keyboards


def cart_keyboards(cart_user, user_id):
    from loader import users_db

    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        back = "⬅️ Назад"
        buy_text = "✅ Оформить заказ"
    else:
        back = "⬅️ Ortga"
        buy_text = "✅ Buyurtmani rasmiylashtirish"

    keyboards = InlineKeyboardMarkup(inline_keyboard=[])

    for i in cart_user:
        keyboards.inline_keyboard.append(
            [
                InlineKeyboardButton(text="➖", callback_data=f"{i[1]}_minus"),
                InlineKeyboardButton(text=f"{i[2].split()[-1]}", callback_data=i[2]),
                InlineKeyboardButton(text="➕", callback_data=f"{i[1]}_plus"),
            ]
        )

    keyboards.inline_keyboard.append(
        [
            InlineKeyboardButton(text=buy_text, callback_data="buy"),
        ]
    )
    keyboards.inline_keyboard.append(
        [
            InlineKeyboardButton(text=back, callback_data="back"),
        ]
    )

    return keyboards


def product_keyboards(user_id, product_id):
    from loader import users_db

    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        back = "⬅️ Назад"
        cart = "🛒 Добавить в корзину"
    else:
        back = "⬅️ Ortga"
        cart = "🛒 Savatga qo`shish"

    keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=cart, callback_data=f"{product_id}"),
            ],
            [
                InlineKeyboardButton(text=back, callback_data="back"),
            ]
        ]
    )
    return keyboards


def product_keyboard_back(user_id, product_id):
    from loader import users_db

    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        cart = "🛒 Корзина"
        back = "⬅️ Назад"
    else:
        cart = "🛒 Savat"
        back = "⬅️ Ortga"

    keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=cart, callback_data=f"{product_id}_cart_product"),
            ],
            [
                InlineKeyboardButton(text=back, callback_data="back"),
            ]
        ]
    )
    return keyboards


def products_keyboard(user_id, page):
    from loader import products_db, users_db

    user_data = users_db.select_user(user_id=user_id)

    if user_data[13] == "bu-kategoriyadagi-barcha-mahsulotlar":
        products = products_db.select_all_products_one_category(up_category=user_data[12])
    else:
        products = products_db.select_products(up_category=user_data[12], sub_category=user_data[13])

    if user_data[9] == "russia":
        back = "⬅️ Назад"
        product_name = 4
    else:
        back = "⬅️ Ortga"
        product_name = 3

    keyboards = InlineKeyboardMarkup(inline_keyboard=[])

    items_per_page = 6
    pages = ceil(len(products) / items_per_page)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    current_page_products = products[start:end]

    for i in current_page_products:
        keyboards.inline_keyboard.append([InlineKeyboardButton(text=i[product_name], callback_data=str(i[0]))])

    if pages > 1:
        pagination_buttons = []
        if page > 1:
            back_data = f"page_{page-1}"
            button_text = "◀️"
        else:
            back_data = "none"
            button_text = "#️⃣"
        pagination_buttons.append(InlineKeyboardButton(text=button_text, callback_data=back_data))
        pagination_buttons.append(InlineKeyboardButton(text=f"{page}/{pages}", callback_data="none"))
        if page < pages:
            next_data = f"page_{page+1}"
            button_text = "▶️"
        else:
            next_data = "none"
            button_text = "#️⃣"
        pagination_buttons.append(InlineKeyboardButton(text=button_text, callback_data=next_data))
        keyboards.inline_keyboard.append(pagination_buttons)

    keyboards.inline_keyboard.append([InlineKeyboardButton(text=back, callback_data="back")])

    return keyboards


def sub_category_keyboard(user_id, page):
    from loader import categories_db, users_db
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        back = "⬅️ Назад"
        button_text = 4
    else:
        back = "⬅️ Ortga"
        button_text = 3

    sub_categories = categories_db.select_sub_categories(up_category=user_data[12])
    keyboards = InlineKeyboardMarkup(inline_keyboard=[])

    items_per_page = 6
    pages = ceil(len(sub_categories) / items_per_page)

    start = (page - 1) * items_per_page
    end = start + items_per_page
    current_page_sub_categories = sub_categories[start:end]

    for i in current_page_sub_categories:
        keyboards.inline_keyboard.append([InlineKeyboardButton(text=i[button_text], callback_data=i[2])])

    if pages > 1:
        pagination_buttons = []
        if page > 1:
            back_data = f"page_{page - 1}"
            button_text = "◀️"
        else:
            back_data = "none"
            button_text = "#️⃣"
        pagination_buttons.append(InlineKeyboardButton(text=button_text, callback_data=back_data))
        pagination_buttons.append(InlineKeyboardButton(text=f"{page}/{pages}", callback_data="none"))
        if page < pages:
            next_data = f"page_{page + 1}"
            button_text = "▶️"
        else:
            next_data = "none"
            button_text = "#️⃣"
        pagination_buttons.append(InlineKeyboardButton(text=button_text, callback_data=next_data))
        keyboards.inline_keyboard.append(pagination_buttons)

    keyboards.inline_keyboard.append([InlineKeyboardButton(text=back, callback_data="back")])

    return keyboards


def up_category_keyboard(user_id):
    from loader import categories_db, users_db
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        back = "⬅️ Назад"
        button_text = 4
    else:
        back = "⬅️ Ortga"
        button_text = 3

    up_categories = categories_db.select_up_categories()
    keyboards = InlineKeyboardMarkup(inline_keyboard=[])

    for i in up_categories:
        keyboards.inline_keyboard.append(
            [
                InlineKeyboardButton(text=i[button_text], callback_data=i[2])
            ]
        )
    keyboards.inline_keyboard.append(
        [
            InlineKeyboardButton(text=back, callback_data="back")
        ]
    )
    return keyboards


def back_keyboard(user_id: int):
    from loader import users_db
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        back = "⬅️ Назад"
    else:
        back = "⬅️ Ortga"

    keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=back, callback_data="back")
            ]
        ]
    )
    return keyboards


def languages_keyboard(user_id: int, back: bool):
    from loader import users_db
    user_data = users_db.select_user(user_id=user_id)

    if back:
        if user_data[9] == "russia":
            back = "⬅️ Назад"
        else:
            back = "⬅️ Ortga"

        keyboards = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uzbek"),
                    InlineKeyboardButton(text="🇷🇺 Русский", callback_data="russia")
                ],
                [
                    InlineKeyboardButton(text=back, callback_data="back"),
                ],
            ]
        )
        return keyboards
    else:
        keyboards = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uzbek"),
                    InlineKeyboardButton(text="🇷🇺 Русский", callback_data="russia"),
                ]
            ]
        )
        return keyboards


def menu_keyboard(user_id: int):
    from loader import users_db
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        shopping = "🛍 Покупка"
        myorders = "📑 Мои покупки"
        settings = "⚙️ Настройки"
        search = "🔍 Поиск"
        wallet = "💰 Кошелек"
        cart = "🛒 Корзина"
    else:
        shopping = "🛍 Xarid qilish"
        myorders = "📑 Buyurtmalarim"
        settings = "⚙️ Sozlamalar"
        search = "🔍 Qidirish"
        wallet = "💰 Hamyon"
        cart = "🛒 Savat"

    keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=shopping, callback_data="shopping")
            ],
            [
                InlineKeyboardButton(text=wallet, callback_data="wallet"),
                InlineKeyboardButton(text=settings, callback_data="settings"),
            ],
            [
                InlineKeyboardButton(text=myorders, callback_data="myorders"),
                InlineKeyboardButton(text=cart, callback_data="cart_menu")
                # InlineKeyboardButton(text=search, callback_data="search"),
            ]
        ]
    )
    if user_id in ADMINS:
        keyboards.inline_keyboard.append(
            [
                InlineKeyboardButton(text="👨‍💻 Admin", callback_data="admin")
            ]
        )
    return keyboards


def settings_keyboard(user_id: int):
    from loader import users_db
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        name = "✏️ Изменить имя"
        phone = "☎️ Изменить номер телефона"
        language = "🌍 Изменить язык"
        back = "⬅️ Назад"
    else:
        name = "✏️ Isimni o`zgartirish"
        phone = "☎️ Telefon raqamni o`zgartirish"
        language = "🌍 Tilni o`zgartirish"
        back = "⬅️ Ortga"

    keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=phone, callback_data="phone")
            ],
            [
                InlineKeyboardButton(text=language, callback_data="language")
            ],
            [
                InlineKeyboardButton(text=name, callback_data="first_name")
            ],
            [
                InlineKeyboardButton(text=back, callback_data="back"),
            ],
        ]
    )
    return keyboards

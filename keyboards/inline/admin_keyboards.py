from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Qo'shish", callback_data="add_data")
        ],
        [
            InlineKeyboardButton(text="O'chirish", callback_data="delete_data")
        ],
        [
            InlineKeyboardButton(text="Tahrirlash", callback_data="edit")
        ],
        [
            InlineKeyboardButton(text="Kunlik savdo", callback_data="day_trading")
        ],
        [
            InlineKeyboardButton(text="Mahsus buyruqlar", callback_data="commands")
        ],
        [
            InlineKeyboardButton(text="⬅️ Chiqish", callback_data="back")
        ]
    ]
)

add_data_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Mahsulot qo'shish", callback_data="add_product")
        ],
        [
            InlineKeyboardButton(text="Bo'lim qo'shish", callback_data="add_category")
        ],
        [
            InlineKeyboardButton(text="Plastik karta qo'shish", callback_data="add_debit_card")
        ],
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="back"),
        ],

    ]
)

add_category_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Yuqori bo'lim qo'shish", callback_data="add_up_category")
        ],
        [
            InlineKeyboardButton(text="Ichki bo'lim qo'shish", callback_data="add_sub_category")
        ],
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="back"),
        ],
    ]
)

delete_data_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Mahsulotni o'chirish", callback_data="delete_product")
        ],
        [
            InlineKeyboardButton(text="Bo'limni o'chirish", callback_data="delete_category")
        ],
        [
            InlineKeyboardButton(text="Plastik kartani o'chirish", callback_data="delete_debit_card")
        ],
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="back"),
        ],

    ]
)

delete_category_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Yuqori bo'limni o'chirish", callback_data="delete_up_category")
        ],
        [
            InlineKeyboardButton(text="Ichki bo'limni o'chirish", callback_data="delete_sub_category")
        ],
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="back"),
        ],

    ]
)

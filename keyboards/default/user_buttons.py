from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


finish_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Rasm va video qo'shishni yakunlash!")
        ]
    ],
    resize_keyboard=True
)

def phone_number_button(back, user_id):
    from loader import users_db
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        send_phone = "☎️ Отправьте номер телефона"
        back_text = "⬅️ Назад"
    elif user_data[9] == "usa":
        send_phone = "☎️ Send phone number"
        back_text = "⬅️ Back"
    else:
        send_phone = "☎️ Telefon raqamni yuborish"
        back_text = "⬅️ Ortga"

    phone_button = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=send_phone, request_contact=True)
            ],
        ],
        resize_keyboard=True
    )
    if back:
        phone_button.keyboard.append(
            [
                KeyboardButton(text=back_text)
            ]
        )
    return phone_button

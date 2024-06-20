from aiogram import F
from data import ADMINS
from aiogram.types import Message
from loader import dp, users_db, bot
from states.user_states import UserStates
from aiogram.fsm.context import FSMContext
from keyboards import phone_number_button, menu_keyboard


@dp.message(UserStates.first_name)
async def add_last_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = users_db.select_user(user_id=user_id)
    if user_data[9] == "russia":
        text = "Подтвердите отправку своего номера телефона, нажав кнопку <b>☎️ Отправить номер телефона</b>!"
    else:
        text = "<b>☎️ Telefon raqamni yuborish</b> tugmasini bosib telefon raqamingizni yuborishni tasdiqlang!"

    msg = await message.answer(text=text, reply_markup=phone_number_button(back=False, user_id=user_id))
    await bot.delete_message(chat_id=message.from_user.id, message_id=user_data[11])
    await state.set_state(UserStates.phone_number)
    await message.delete()
    users_db.update_user_info(user_id=user_id, user_first_name=message.text, user_last_message_id=msg.message_id)


@dp.message(F.contact, UserStates.phone_number)
async def add_phone_number(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = users_db.select_user(user_id=user_id)
    if user_data[9] == "russia":
        text = ("Вы можете приобрести Подарочные карты (Gift Card) для пополнения игровых приставок или игр.\n\n"
                "Нажмите кнопку <b>🛍 Покупка</b> и купите нужный вам товар!")
    else:
        text = ("O'yin konsollari yoki o'yinlar hisobini to'ldirish uchun Sovg'a kartalarini (Gift Card) xarid "
                "qilishingiz mumkun.\n\n<b>🛍 Xarid qilish</b> tugmasini bosing va o'zingizga kerakli mahsulotni "
                "xarid qiling!")

    await message.answer(text=text, reply_markup=menu_keyboard(user_id=user_id))
    await state.set_state(UserStates.user_menu)
    await bot.delete_message(chat_id=message.from_user.id, message_id=user_data[11])
    await message.delete()
    users_db.update_user_info(user_id=user_id,
                              user_phone_number=message.contact.phone_number,
                              user_registration="True")
    await bot.send_message(chat_id=ADMINS[0], text=f"<b>Botga yangi obunachi qo'shildi</b>\n\n"
                                                   f"Username: @{user_data[1]}\n"
                                                   f"Ism: {user_data[3]}\n"
                                                   f"Tel: {message.contact.phone_number}\n"
                                                   f"Tanlagan tili: {user_data[9]}\n"
                                                   f"User Id: <code>{user_data[0]}</code>")

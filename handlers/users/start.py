import pytz
from aiogram import F
from datetime import datetime
from loader import dp, users_db
from sqlite3 import IntegrityError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states import UserStates, AdminStates
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart
from keyboards.inline.admin_keyboards import add_data_keyboard
from keyboards import languages_keyboard, menu_keyboard, admin_keyboard


@dp.message(CommandStart())
async def bot_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = users_db.select_user(user_id=user_id)
    if user_data and (user_data[8] == "True"):
        if user_data[9] == "russia":
            text = ("Вы можете приобрести Подарочные карты (Gift Card) для пополнения игровых приставок или игр.\n\n"
                    "Нажмите кнопку <b>🛍 Покупка</b> и купите нужный вам товар!")
        else:
            text = ("O'yin konsollari yoki o'yinlar hisobini to'ldirish uchun Sovg'a kartalarini (Gift Card) xarid "
                    "qilishingiz mumkun.\n\n<b>🛍 Xarid qilish</b> tugmasini bosing va o'zingizga kerakli mahsulotni "
                    "xarid qiling!")
        await message.answer(text=text, reply_markup=menu_keyboard(user_id=user_id))
        await state.set_state(UserStates.user_menu)
    else:
        await message.answer(text="<b>Tilni tanlang!\n\nВыберите язык!</b>",
                             reply_markup=languages_keyboard(user_id=user_id, back=False))
        await state.set_state(UserStates.choice_language)
    await message.delete()


@dp.callback_query(F.data.in_({"uzbek", "russia", "usa"}), UserStates.choice_language)
async def bot_start1(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if call.data == "russia":
        enter_name = "Введите свое имя, чтобы начать регистрацию!"
    else:
        enter_name = "Ro`yhatdan o'tishni boshlash uchun ismingizni kiriting!"

    current_time = datetime.now(pytz.timezone("Asia/Tashkent")).strftime("%H:%M | %d.%m.%Y")
    msg = await call.message.edit_text(text=enter_name)
    try:
        users_db.add_user(user_id=user_id,
                          user_name=call.from_user.username,
                          user_full_name=call.from_user.full_name,
                          user_first_name="none",
                          user_last_name=call.from_user.last_name,
                          user_phone_number="none",
                          user_registration_date=current_time,
                          user_all_money_spent=0,
                          user_registration="False",
                          user_language=call.data,
                          user_wallet=0,
                          user_last_message_id=msg.message_id,
                          user_up_category="none",
                          user_sub_category="none",
                          user_last_page=0,
                          user_sub_category_last_page=0,
                          user_last_state="none")
    except IntegrityError:
        users_db.update_user_info(user_id=user_id, user_language=call.data)
    await state.set_state(UserStates.first_name)


@dp.callback_query(F.data == "back", StateFilter(AdminStates.admin_add_data, AdminStates.admin_delete_data))
async def settings(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=".<b>      Kerakli buyruqni tanlang!      </b>.", reply_markup=admin_keyboard)
    await state.set_state(AdminStates.admin)


@dp.callback_query(F.data == "back", StateFilter(AdminStates.admin_add_category, AdminStates.add_product_up_category,
                                                 AdminStates.add_debit_card_number))
async def add_category_back(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=".<b>      Kerakli buyruqni tanlang!      </b>.", reply_markup=add_data_keyboard)
    await state.set_state(AdminStates.admin_add_data)


@dp.callback_query(F.data == "back", StateFilter(AdminStates.admin, UserStates.user_up_category, UserStates.settings))
async def settings(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)
    if user_data[9] == "russia":
        text = ("Вы можете приобрести Подарочные карты (Gift Card) для пополнения игровых приставок или игр.\n\n"
                "Нажмите кнопку <b>🛍 Покупка</b> и купите нужный вам товар!")
    else:
        text = ("O'yin konsollari yoki o'yinlar hisobini to'ldirish uchun Sovg'a kartalarini (Gift Card) xarid "
                "qilishingiz mumkun.\n\n<b>🛍 Xarid qilish</b> tugmasini bosing va o'zingizga kerakli mahsulotni "
                "xarid qiling!")
    await call.message.edit_text(text=text, reply_markup=menu_keyboard(user_id=user_id))
    await state.set_state(UserStates.user_menu)


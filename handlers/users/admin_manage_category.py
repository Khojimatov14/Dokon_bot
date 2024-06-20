from aiogram import F
from states import AdminStates
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loader import dp, users_db, bot, categories_db
from keyboards import add_category_keyboard, up_category_keyboard
from keyboards.inline.admin_keyboards import delete_category_keyboard, delete_data_keyboard


@dp.callback_query(F.data == "add_category", AdminStates.admin_add_data)
async def add_category1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=".<b>      Kerakli buyruqni tanlang!      </b>.",
                                 reply_markup=add_category_keyboard)
    await state.set_state(AdminStates.admin_add_category)


@dp.callback_query(F.data == "add_up_category", AdminStates.admin_add_category)
async def add_up_category(call: CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text(text="<b>Bo'lim nomini kiriting!</b>")
    await state.set_state(AdminStates.admin_add_up_category)
    users_db.update_user_info(user_id=call.from_user.id, user_last_message_id=msg.message_id)


@dp.message(AdminStates.admin_add_up_category)
async def add_up_category_text(message: Message, state: FSMContext):
    user_data = users_db.select_user(user_id=message.from_user.id)
    await message.delete()
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=user_data[11],
                                text=".<b>      Yuqori bo'lim qo'shildi!      </b>.",
                                reply_markup=add_category_keyboard)
    await state.set_state(AdminStates.admin_add_category)
    categories_db.add_category(up_category="True", sub_category="none", category_name=message.text)


@dp.callback_query(F.data == "add_sub_category", AdminStates.admin_add_category)
async def add_sub_category(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=".<b>    Yuqori bo'limni tanlang!    </b>.", reply_markup=up_category_keyboard(user_id=call.from_user.id))
    await state.set_state(AdminStates.admin_add_sub_category)


@dp.callback_query(AdminStates.admin_add_sub_category)
async def add_sub_category_text(call: CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text(text="<b>Ichki bo'lim nomini kiriting!</b>")
    await state.set_state(AdminStates.admin_add_sub_category_text)
    users_db.update_user_info(user_id=call.from_user.id, user_up_category=call.data, user_last_message_id=msg.message_id)


@dp.message(AdminStates.admin_add_sub_category_text)
async def add_up_category_text(message: Message, state: FSMContext):
    user_data = users_db.select_user(user_id=message.from_user.id)
    await message.delete()
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=user_data[11],
                                text=".<b>      Ichki bo'lim qo'shildi!      </b>.",
                                reply_markup=add_category_keyboard)
    await state.set_state(AdminStates.admin_add_category)
    categories_db.add_category(up_category=user_data[12], sub_category="none", category_name=message.text)


@dp.callback_query(F.data == "delete_category", AdminStates.admin_delete_data)
async def delete_category1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=".<b>      Kerakli buyruqni tanlang!      </b>.",
                                 reply_markup=delete_category_keyboard)
    await state.set_state(AdminStates.admin_delete_category)


@dp.callback_query(F.data == "back", AdminStates.admin_delete_category)
async def delete_category_back(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=".<b>      Kerakli buyruqni tanlang!      </b>.", reply_markup=delete_data_keyboard)
    await state.set_state(AdminStates.admin_delete_data)

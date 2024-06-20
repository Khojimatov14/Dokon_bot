from aiogram import F
from loader import dp
from aiogram.types import CallbackQuery
from states import AdminStates, UserStates
from aiogram.fsm.context import FSMContext
from keyboards import admin_keyboard
from keyboards.inline.admin_keyboards import add_data_keyboard, delete_data_keyboard


@dp.callback_query(F.data == "admin", UserStates.user_menu)
async def settings(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=".<b>      Kerakli buyruqni tanlang!      </b>.", reply_markup=admin_keyboard)
    await state.set_state(AdminStates.admin)


@dp.callback_query(F.data == "add_data", AdminStates.admin)
async def settings(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=".<b>      Kerakli buyruqni tanlang!      </b>.", reply_markup=add_data_keyboard)
    await state.set_state(AdminStates.admin_add_data)


@dp.callback_query(F.data == "delete_data", AdminStates.admin)
async def settings(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=".<b>      Kerakli buyruqni tanlang!      </b>.", reply_markup=delete_data_keyboard)
    await state.set_state(AdminStates.admin_delete_data)


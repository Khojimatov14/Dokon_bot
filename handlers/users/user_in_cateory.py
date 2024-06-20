import re
from aiogram import F
from states import UserStates
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from loader import dp, users_db, categories_db
from keyboards import up_category_keyboard, sub_category_keyboard, products_keyboard


@dp.callback_query(F.data == "shopping", UserStates.user_menu)
async def up_category(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        text = ".<b>      Выбирайте нужный раздел!      </b>."
    elif user_data[9] == "usa":
        text = ".<b>      Choose the desired section!      </b>."
    else:
        text = ".<b>       Kerakli bo'limni tanlang!       </b>."

    await call.message.edit_text(text=text, reply_markup=up_category_keyboard(user_id=user_id))
    await state.set_state(UserStates.user_up_category)


pattern = re.compile(r'^[a-zA-Z-]+$')


@dp.callback_query(lambda c: bool(pattern.match(c.data)), UserStates.user_up_category)
async def up_category(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        text = f"<b>{categories_db.select_category(sub_category=call.data)[4]}</b>"
    else:
        text = f"<b>{categories_db.select_category(sub_category=call.data)[3]}</b>"

    users_db.update_user_info(user_id=user_id, user_up_category=call.data, user_sub_category_last_page=1)
    await call.message.edit_text(text=text, reply_markup=sub_category_keyboard(user_id=user_id, page=1))
    await state.set_state(UserStates.user_sub_category)


@dp.callback_query(lambda c: c.data.startswith("page_") or c.data == "none", UserStates.user_sub_category)
async def show_products_by_page(call: CallbackQuery):
    if call.data != "none":
        user_id = call.from_user.id
        page = int(call.data.split("_")[1])

        await call.message.edit_reply_markup(reply_markup=sub_category_keyboard(user_id=user_id, page=page))
        users_db.update_user_info(user_id=user_id, user_sub_category_last_page=page)


@dp.callback_query(F.data == "back", UserStates.user_sub_category)
async def up_category_back(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if call.data == "back":
        if user_data[9] == "russia":
            text = ".<b>      Выбирайте нужный раздел!      </b>."
        elif user_data[9] == "usa":
            text = ".<b>      Choose the desired section!      </b>."
        else:
            text = ".<b>       Kerakli bo'limni tanlang!       </b>."

        await call.message.edit_text(text=text, reply_markup=up_category_keyboard(user_id=user_id))
        await state.set_state(UserStates.user_up_category)


@dp.callback_query(lambda c: bool(pattern.match(c.data)), UserStates.user_sub_category)
async def up_subcategory(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        text = f"<b>{categories_db.select_category(sub_category=call.data)[4]}</b>"
    else:
        text = f"<b>{categories_db.select_category(sub_category=call.data)[3]}</b>"

    users_db.update_user_info(user_id=user_id, user_sub_category=call.data, user_last_page=1)
    await call.message.edit_text(text=text, reply_markup=products_keyboard(user_id=user_id, page=1))
    await state.set_state(UserStates.user_show_products)


@dp.callback_query(F.data.startswith("page_"), UserStates.user_show_products)
async def show_products_by_page(call: CallbackQuery):
    user_id = call.from_user.id
    page = int(call.data.split("_")[1])

    await call.message.edit_reply_markup(reply_markup=products_keyboard(user_id=user_id, page=page))
    users_db.update_user_info(user_id=user_id, user_last_page=page)


@dp.callback_query(F.data == "back", UserStates.user_show_products)
async def up_subcategory_back(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        text = f"<b>{categories_db.select_category(sub_category=user_data[12])[4]}</b>"
    else:
        text = f"<b>{categories_db.select_category(sub_category=user_data[12])[3]}</b>"

    await call.message.edit_text(text=text, reply_markup=sub_category_keyboard(user_id=user_id, page=user_data[15]))
    await state.set_state(UserStates.user_sub_category)

from aiogram import F
from states import UserStates
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from loader import dp, products_db, users_db, carts_db, categories_db
from keyboards import products_keyboard, product_keyboards, product_keyboard_back
from utils import create_album_product, create_old_messages, delete_old_messages


@dp.callback_query(lambda c: c.data.isdigit(), UserStates.user_show_products)
async def show_product(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    product_id = call.data
    user_cart = carts_db.select_user_cart(user_id=user_id)

    if any(str(item[1]) == product_id for item in user_cart):
        markup = product_keyboard_back(user_id=user_id, product_id=product_id)
    else:
        markup = product_keyboards(user_id=user_id, product_id=product_id)

    album = create_album_product(user_id=user_id, product=products_db.select_product(product_id=product_id))

    if album["album"]:
        msg = await call.message.answer_media_group(media=album["album"])
        await call.message.answer_photo(photo=album["last_photo"], caption=album["description"],
                                        reply_markup=markup)
    else:
        msg = await call.message.answer_photo(photo=album["last_photo"], caption=album["description"],
                                              reply_markup=markup)

    await create_old_messages(message=msg, user_id=user_id)
    await state.set_state(UserStates.user_in_product)
    await call.message.delete()


@dp.callback_query(F.data == "back", UserStates.user_in_product)
async def back_product(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        text = f"<b>{categories_db.select_category(sub_category=user_data[13])[4]}</b>"
    else:
        text = f"<b>{categories_db.select_category(sub_category=user_data[13])[3]}</b>"

    await call.message.answer(text=text, reply_markup=products_keyboard(user_id=user_id, page=user_data[14]))
    await state.set_state(UserStates.user_show_products)
    await delete_old_messages(user_id=user_id, message_id=call.message.message_id)


@dp.callback_query(lambda c: c.data.isdigit(), UserStates.user_in_product)
async def add_cart_product(call: CallbackQuery):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)
    product_data = products_db.select_product(product_id=call.data)

    if user_data[9] == "russia":
        text = "Товар добавлен в корзину!"
        product_name = 4
    else:
        text = "Mahsulot savatga qo'shildi!"
        product_name = 3

    await call.answer(text=text)
    await call.message.edit_reply_markup(inline_message_id=call.inline_message_id,
                                         reply_markup=product_keyboard_back(user_id=user_id, product_id=call.data))
    carts_db.add_product_cart(user_id=call.from_user.id,
                              product_id=call.data,
                              product_name=product_data[product_name],
                              product_price=product_data[6],
                              count=1)

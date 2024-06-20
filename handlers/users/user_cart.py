import asyncio
from states import UserStates
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from loader import dp, carts_db, users_db, products_db
from keyboards import cart_keyboards, menu_keyboard, product_keyboard_back
from utils import products_text, delete_old_messages, create_album_product, create_old_messages


@dp.callback_query(lambda c: c.data == "cart_menu" or c.data.endswith("_cart_product"), StateFilter(UserStates))
async def cart(call: CallbackQuery, state: FSMContext):
    cart_user = carts_db.select_user_cart(user_id=call.from_user.id)
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        empty_cart = "В корзине нет товаров!"
    else:
        empty_cart = "Savatda hechqanday mahsulot yo`q!"

    if len(cart_user) > 0:
        try:
            await call.message.edit_text(products_text(cart_user=cart_user, language=user_data[9]),
                                         reply_markup=cart_keyboards(cart_user, user_id=user_id))
        except TelegramBadRequest:
            await call.message.answer(products_text(cart_user=cart_user, language=user_data[9]),
                                      reply_markup=cart_keyboards(cart_user, user_id=user_id))

            await delete_old_messages(user_id=user_id, message_id=call.message.message_id)

        await state.set_state(UserStates.user_in_cart)
        users_db.update_user_info(user_id=user_id, user_last_state=call.data)
    else:
        rem = await call.message.answer(text=empty_cart)
        await asyncio.sleep(5)
        await rem.delete()


@dp.callback_query(lambda c: True, UserStates.user_in_cart)
async def plus_cuantity(call: CallbackQuery, state: FSMContext):
    # message_text = texts_db.select_text(text_name="main_text")
    # categories = categories_db.select_all_categories()
    product_id = call.data.split('_')[0]
    user_id = call.from_user.id
    cart_user = carts_db.select_user_cart(user_id=user_id)
    user_data = users_db.select_user(user_id=user_id)

    if call.data == "buy":
        await call.message.edit_text(".      <b>Xarid qilish usulini tanlang</b>      .")#, reply_markup=picup_delivery)
        # await ProductsState.check_picup_delivery.set()
    elif call.data == "back":
        if user_data[16] != "cart_menu":
            product_id = user_data[16].split("_")[0]
            album = create_album_product(user_id=user_id, product=products_db.select_product(product_id=product_id))

            if album["album"]:
                msg = await call.message.answer_media_group(media=album["album"])
                await call.message.answer_photo(photo=album["last_photo"], caption=album["description"],
                                                reply_markup=product_keyboard_back(user_id=user_id, product_id=product_id))
            else:
                msg = await call.message.answer_photo(photo=album["last_photo"], caption=album["description"],
                                                      reply_markup=product_keyboard_back(user_id=user_id, product_id=product_id))

            await create_old_messages(message=msg, user_id=user_id)
            await state.set_state(UserStates.user_in_product)
            await call.message.delete()
        else:
            await call.message.edit_text(text="Menu", reply_markup=menu_keyboard(user_id=user_id))
            await state.set_state(UserStates.user_menu)
    else:
        for i in cart_user:
            if i[1] == product_id and "plus" in call.data:
                carts_db.update_cart_info(user_id=user_id, product_id=i[1], count=i[4] + 1)
                cart_user = carts_db.select_user_cart(user_id=user_id)
                await call.message.edit_text(products_text(cart_user=cart_user, language=user_data[9]), reply_markup=cart_keyboards(cart_user, user_id=user_id))
            elif i[1] == product_id and "minus" in call.data:
                if i[4] - 1 < 1:
                    carts_db.delete_cart_product(user_id=user_id, product_id=i[1])
                    cart_user = carts_db.select_user_cart(user_id=user_id)
                    if cart_user:
                        await call.message.edit_text(products_text(cart_user=cart_user, language=user_data[9]), reply_markup=cart_keyboards(cart_user, user_id=user_id))
                    else:
                        await call.message.edit_text(text="Menu", reply_markup=menu_keyboard(user_id=user_id))
                        await state.set_state(UserStates.user_menu)
                else:
                    carts_db.update_cart_info(user_id=user_id, product_id=i[1], count=i[4] - 1)
                    cart_user = carts_db.select_user_cart(user_id=user_id)
                    await call.message.edit_text(products_text(cart_user=cart_user, language=user_data[9]), reply_markup=cart_keyboards(cart_user, user_id=user_id))

    if "plus" not in call.data and "minus" not in call.data and "back" not in call.data and "buy" not in call.data:
        rem = await call.message.answer(call.data)
        await asyncio.sleep(3)
        await rem.delete()

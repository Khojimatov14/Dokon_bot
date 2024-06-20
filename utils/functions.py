from keyboards import finish_button
from aiogram.enums import ContentType
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo


def products_text(cart_user, language):

    if language == "russia":
        price_text = "Цена:"
        sum_text = "сум"
        pcs = "шт"
        total = "Общий:"
        products = "Товары в корзине!"
    else:
        price_text = "Narxi:"
        sum_text = "so'm"
        pcs = "dona"
        total = "Jami:"
        products = "Savatdagi mahsulotlar!"

    product_text = f".           <b>{products}</b>           .\n\n"
    price = 0

    for i in cart_user:
        product_text += f"<b>{i[4]} {pcs}</b> | {i[2]} | {price_text} <b>{'{:,.0f}'.format(i[3])} {sum_text}</b>\n\n"
        price += i[3] * i[4]
    product_text += f"{total} <b>{'{:,.0f}'.format(price)} {sum_text}</b>"
    return product_text


async def create_old_messages(message, user_id):
    from loader import users_db
    messages = ""
    if type(message) is list:
        messages += str(message[0].message_id)
        for i in message[1:]:
            messages += f",{str(i.message_id)}"
    else:
        messages += str(message.message_id)
    users_db.update_user_info(user_id=user_id, user_last_message_id=messages)


async def delete_old_messages(user_id, message_id=None):
    from loader import users_db, bot
    old_messages = users_db.select_user(user_id=user_id)[11].split(',')
    if message_id is not None:
        old_messages.append(message_id)
    await bot.delete_messages(chat_id=user_id, message_ids=old_messages)


async def add_new_product_media(message: Message):
    from loader import users_db, products_db
    product_id = products_db.select_last_product()[0]
    product_photos = products_db.select_last_product()[4]
    if message.content_type == ContentType.PHOTO:
        if product_photos == "none":
            products_db.update_product_info(product_id=product_id,
                                            product_photos=f"|photo|{message.photo[-1].file_id}")
        else:
            products_db.update_product_info(product_id=product_id,
                                            product_photos=f"{product_photos},|photo|{message.photo[-1].file_id}")
    elif message.content_type == ContentType.VIDEO:
        if product_photos == "none":
            products_db.update_product_info(product_id=product_id,
                                            product_photos=f"|video|{message.video.file_id}")
        else:
            products_db.update_product_info(product_id=product_id,
                                            product_photos=f"{product_photos},|video|{message.video.file_id}")
    msg = await message.answer(text="Yana rasm yoki video yuborishingiz mumkun!", reply_markup=finish_button)
    users_db.update_user_info(user_id=message.from_user.id, user_last_message_id=msg.message_id)


def create_album_product(user_id, product):
    from loader import users_db

    album = []
    product_photos = product[7].split(",")
    if len(product_photos) > 1:
        for photo in product_photos[:-1]:
            album.append(InputMediaPhoto(media=photo))
        last_photo = product_photos[-1]
    else:
        last_photo = product[7]

    user_data = users_db.select_user(user_id=user_id)
    if user_data[9] == "russia":
        caption = product[9]
        price = "Цена"
        sum_text = "сум"
        product_name = product[4]
    elif user_data[9] == "usa":
        caption = product[10]
        price = "Price"
        sum_text = "sum"
        product_name = product[5]
    else:
        caption = product[8]
        price = "Narxi"
        sum_text = "so'm"
        product_name = product[3]

    description = f"<b>{product_name}\n\n💰 {price}: {'{:,.0f}'.format(product[6])} {sum_text}</b>\n\n{caption}"

    return {"album": album, "description": description, "last_photo": last_photo}

import asyncio
from aiogram import F
from data import ADMINS
from states import AdminStates
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from loader import dp, users_db, products_db, bot
from aiogram.types import CallbackQuery, Message
from utils import add_new_product_media, create_album_product
from keyboards import up_category_keyboard, sub_category_keyboard, admin_keyboard


@dp.callback_query(F.data == "add_product", F.from_user.id == ADMINS[0], AdminStates.admin_add_data)
async def add_product_start(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="<b>Mahsulotni qaysi bo'limga qo'shmoqchisiz?</b>", reply_markup=up_category_keyboard(user_id=call.from_user.id))
    await state.set_state(AdminStates.add_product_up_category)


@dp.callback_query(lambda c: c.data.isdigit(), F.from_user.id == ADMINS[0], AdminStates.add_product_up_category)
async def add_product_up_category(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    users_db.update_user_info(user_id=user_id, user_up_category=call.data)
    await call.message.edit_text(text="<b>Ichki bo'limni tanlang!</b>", reply_markup=sub_category_keyboard(user_id=user_id, page=1))
    await state.set_state(AdminStates.add_product_sub_category)
    users_db.update_user_info(user_id=user_id, user_up_category=call.data, user_sub_category_last_page=1)


@dp.callback_query(F.data == "back", F.from_user.id == ADMINS[0], AdminStates.add_product_sub_category)
async def add_product_back(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="<b>Mahsulotni qaysi bo'limga qo'shmoqchisiz?</b>", reply_markup=up_category_keyboard(user_id=call.from_user.id))
    await state.set_state(AdminStates.add_product_up_category)


@dp.callback_query(lambda c: c.data.isdigit(), F.from_user.id == ADMINS[0], AdminStates.add_product_sub_category)
async def add_product_sub_category(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="<b>Mahsulotning nomini kiriting!</b>")
    await state.set_state(AdminStates.add_product_name)
    users_db.update_user_info(user_id=call.from_user.id, user_sub_category=call.data)


@dp.message(F.from_user.id == ADMINS[0], AdminStates.add_product_name)
async def add_product_name(message: Message, state: FSMContext):
    await message.answer(text="<b>Mahsulotning narxini kiriting!</b>")
    await state.set_state(AdminStates.add_product_price)
    user_data = users_db.select_user(user_id=message.from_user.id)
    products_db.add_product(up_category=user_data[12],
                            sub_category=user_data[13],
                            product_name_uz=message.text,
                            product_name_ru="none",
                            product_name_en="none",
                            price=0,
                            product_photos="none",
                            description_uz="none",
                            description_ru="none",
                            description_en="none",
                            brand_name="none")


@dp.message(F.from_user.id == ADMINS[0], AdminStates.add_product_price)
async def add_product_name(message: Message, state: FSMContext):
    try:
        products_db.update_product_info(product_id=products_db.select_last_product()[0], price=int(message.text))
        await message.answer(text="Mahsulot haqida malumotlarni o'zbek tilida kiriting!")
        await state.set_state(AdminStates.add_product_description_uzbek)
    except (ValueError, TypeError):
        await message.delete()
        rem = await message.answer(text="Mahsulot narxini raqamlar bilan kiriting!")
        await asyncio.sleep(5)
        await rem.delete()


@dp.message(F.from_user.id == ADMINS[0], AdminStates.add_product_description_uzbek)
async def add_product_name(message: Message, state: FSMContext):
    await message.answer(text="Mahsulot haqida malumotlarni rus tilida kiriting!")
    await state.set_state(AdminStates.add_product_description_russia)
    products_db.update_product_info(product_id=products_db.select_last_product()[0], description_uzbek=message.text)


@dp.message(F.from_user.id == ADMINS[0], AdminStates.add_product_description_russia)
async def add_product_name(message: Message, state: FSMContext):
    await message.answer(text="Mahsulot haqida malumotlarni ingliz tilida kiriting!")
    await state.set_state(AdminStates.add_product_description_usa)
    products_db.update_product_info(product_id=products_db.select_last_product()[0], description_russia=message.text)


@dp.message(F.from_user.id == ADMINS[0], AdminStates.add_product_description_usa)
async def add_product_name(message: Message, state: FSMContext):
    await message.answer(text="Mahsulotning video va rasmlarini 1 tadan yuboring!")
    await state.set_state(AdminStates.add_product_photos)
    products_db.update_product_info(product_id=products_db.select_last_product()[0], description_usa=message.text)


@dp.message(F.from_user.id == ADMINS[0], AdminStates.add_product_photos)
async def add_product_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = users_db.select_user(user_id=user_id)
    if message.content_type == ContentType.PHOTO or message.content_type == ContentType.VIDEO:
        await add_new_product_media(message=message)
    elif message.text == "✅ Rasm va video qo'shishni yakunlash!":
        product = products_db.select_last_product()
        album = create_album_product(user_id=user_id, product=product)
        await bot.delete_message(chat_id=user_id, message_id=user_data[11])
        await message.answer_media_group(media=album["album"])
        await message.answer_photo(photo=album["last_photo"], caption=album["description"])
        await message.answer(text=".<b>      Mahsulot qo'shildi!      </b>.", reply_markup=admin_keyboard)
        await state.set_state(AdminStates.admin)
    else:
        await message.delete()
        rem = await message.answer("Iltimos bu bo'limda habar yozmang va boshqa fayllarni yubormang! "
                                   "Ko`rsatmalarga amal qiling!")
        await asyncio.sleep(6)
        await rem.delete()


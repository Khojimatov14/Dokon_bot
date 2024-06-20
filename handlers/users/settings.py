import re
import asyncio
from aiogram import F
from aiogram.filters import StateFilter
from loader import dp, users_db, bot
from states.user_states import UserStates
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ContentType, Message
from keyboards import settings_keyboard, back_keyboard, phone_number_button, languages_keyboard


@dp.callback_query(F.data == "settings", UserStates.user_menu)
async def settings(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        text = ".<b>       Выберите нужную команду!       </b>."
    elif user_data[9] == "usa":
        text = ".<b>     Select the desired command!     </b>."
    else:
        text = ".<b>      Kerakli buyruqni tanlang!      </b>."

    await call.message.edit_text(text=text, reply_markup=settings_keyboard(user_id=user_id))
    await state.set_state(UserStates.settings)


@dp.callback_query(F.data.in_({"phone", "language", "first_name"}), UserStates.settings)
async def change_datas(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        old_name_text = "Прежнее имя:"
        new_name_text = "Введите новое имя!"
        language_text = ".<b>            Выберите язык!            </b>."
        phone_text = ("Введите свой номер, как показано в примере, или нажмите кнопку\n"
                      "<b>☎️ Отправьте номер телефона</b> и подтвердите отправку номера телефона!\n\nПример: ")
    elif user_data[9] == "usa":
        old_name_text = "Former name:"
        new_name_text = "Enter a new name!"
        language_text = ".<b>           Choose language!           </b>."
        phone_text = ("Enter your number as shown in the example, or click the button\n"
                      "<b>☎️ Send phone number</b> and confirm sending the phone number!\n\nExample: ")
    else:
        old_name_text = "Avvalgi ism:"
        new_name_text = "Yangi isimni kiriting!"
        language_text = ".<b>            Tilni tanlang!            </b>."
        phone_text = ("Raqamingizni namunadagidek kiriting, yoki pastdagi <b>☎️ Telefon raqamni yuborish</b> "
                      "tugmasini bosib telefon raqamingizni yuborishni tasdiqlang!\n\nNamuna: ")

    if call.data == "first_name":
        msg = await call.message.edit_text(text=f"{old_name_text} <b>{user_data[3]}</b>\n\n{new_name_text}",
                                           reply_markup=back_keyboard(user_id=user_id))
        users_db.update_user_info(user_id=user_id, user_last_message_id=msg.message_id)
        await state.set_state(UserStates.change_name)
    elif call.data == "phone":
        msg = await call.message.answer(text=phone_text + user_data[5],
                                        reply_markup=phone_number_button(back=True, user_id=user_id))
        users_db.update_user_info(user_id=user_id, user_last_message_id=msg.message_id)
        await state.set_state(UserStates.change_phone)
        await call.message.delete()
    elif call.data == "language":
        await call.message.edit_text(text=language_text, reply_markup=languages_keyboard(user_id=user_id, back=True))
        await state.set_state(UserStates.change_language)


@dp.callback_query(F.data == "back", StateFilter(UserStates.change_name, UserStates.change_language))
async def change_first_name_back(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        text = ".<b>       Выберите нужную команду!       </b>."
    elif user_data[9] == "usa":
        text = ".<b>     Select the desired command!     </b>."
    else:
        text = ".<b>      Kerakli buyruqni tanlang!      </b>."

    await call.message.edit_text(text=text, reply_markup=settings_keyboard(user_id=user_id))
    await state.set_state(UserStates.settings)


@dp.callback_query(F.data.in_({"uzbek", "russia", "usa"}), UserStates.change_language)
async def edit_language(call: CallbackQuery, state: FSMContext):
    if call.data == "russia":
        text = ".                  Язык изменен                  .\n\n.<b>     Выберите нужную команду     </b>."
    elif call.data == "usa":
        text = ".     Language has been changed    .\n\n.<b>    Select the desired command    </b>."
    else:
        text = ".               Til o`zgartirildi!                .\n\n.<b>       Kerakli buyruqni tanlang       </b>."

    users_db.update_user_info(user_id=call.from_user.id, user_language=call.data)
    await call.message.edit_text(text=text, reply_markup=settings_keyboard(user_id=call.from_user.id))
    await state.set_state(UserStates.settings)


@dp.message(UserStates.change_name)
async def change_first_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        name_alpha = "Введите свое имя буквами!"
        name_changed = ".                   Имя изменено!               .\n\n.<b>    Выберите нужную команду!    </b>."
    elif user_data[9] == "usa":
        name_alpha = "Enter your name in letters!"
        name_changed = ".       Name has been changed!       .\n\n.<b>   Select the desired command!   </b>."
    else:
        name_alpha = "Ismingizni harflar bilan kiriting!"
        name_changed = ".              Ism o`zgartirildi!             .\n\n.     <b>Kerakli buyruqni tanlang!</b>     ."

    async def not_name():
        await message.delete()
        rem = await message.answer(text=name_alpha)
        await asyncio.sleep(5)
        await rem.delete()

    try:
        if message.text.isalpha():
            await message.delete()
            await bot.edit_message_text(chat_id=user_id,
                                        message_id=user_data[11],
                                        text=name_changed,
                                        reply_markup=settings_keyboard(user_id=user_id))
            await state.set_state(UserStates.settings)
            users_db.update_user_info(user_id=user_id, user_first_name=message.text)
        else:
            await not_name()
    except AttributeError:
        await not_name()


@dp.message(UserStates.change_phone)
async def change_phone(message: Message, state: FSMContext):
    pattern = r'^\+?998[0-9]{9}$'
    user_id = message.from_user.id
    user_data = users_db.select_user(user_id=user_id)

    if user_data[9] == "russia":
        number_example = "Введите свой номер как в примере!"
        number_changed = ".       Номер телефона изменен!      .\n\n"
        select_command = ".<b>     Выберите нужную команду     </b>."
    elif user_data[9] == "usa":
        number_example = "Enter your number as in the example!"
        number_changed = ". Phone number has been changed! .\n\n"
        select_command = ".<b>     Select the desired command     </b>."
    else:
        number_example = "Raqamingizni namunadagidek kiriting!"
        number_changed = ".    Telefon raqam o`zgartirildi!    .\n\n"
        select_command = ".<b>      Kerakli buyruqni tanlang      </b>."

    async def delete_message_func():
        await bot.delete_message(chat_id=user_id, message_id=user_data[11])
        await message.delete()

    async def not_phone():
        await message.delete()
        rem = await message.answer(text=number_example)
        await asyncio.sleep(5)
        await rem.delete()

    async def phone_changed():
        await message.answer(text=number_changed + select_command, reply_markup=settings_keyboard(user_id=user_id))
        await state.set_state(UserStates.settings)

    if message.content_type == ContentType.CONTACT:
        users_db.update_user_info(user_id=user_id, user_phone_number=message.contact.phone_number)

        await phone_changed()
        await delete_message_func()
    elif message.text in ["⬅️ Ortga", "⬅️ Back", "⬅️ Назад"]:
        await message.answer(text=select_command, reply_markup=settings_keyboard(user_id=user_id))
        await state.set_state(UserStates.settings)
        await delete_message_func()
    else:
        try:
            if re.match(pattern, message.text):
                users_db.update_user_info(user_id=user_id, user_phone_number=message.text)
                await phone_changed()
                await delete_message_func()
            else:
                await not_phone()
        except TypeError:
            await not_phone()

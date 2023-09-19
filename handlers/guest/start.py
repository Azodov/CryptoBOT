from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ContentTypes, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

from filters import IsGuest
from keyboards.inline.userKeyboards import menu_user_uz, menu_user_ru, menu_user_en
from loader import dp, db


@dp.message_handler(IsGuest(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if message.get_args():
        await db.update_admin(telegram_id=int(message.from_user.id), otp=int(message.get_args()), action=None)
        await message.answer(f"Salom Admin, {message.from_user.full_name}!")
    else:
        lang_btn = InlineKeyboardMarkup(row_width=1)
        lang_btn.add(InlineKeyboardButton(text="🇺🇿Uzbek", callback_data="uz"))
        lang_btn.add(InlineKeyboardButton(text="🇷🇺Русский", callback_data="ru"))
        lang_btn.add(InlineKeyboardButton(text="🇺🇸English", callback_data="en"))
        await message.answer("🇺🇿Tilni tanlang\n🇷🇺Выберите язык\n🇺🇸Choose language", reply_markup=lang_btn)

    await state.set_state("get_language")


@dp.callback_query_handler(IsGuest(), state="get_language")
async def get_language(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.delete()
    language = call.data
    await state.update_data(language=language)
    phone_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    if language == "uz":
        phone_btn.add(KeyboardButton(text="📱Telefon raqamni yuborish", request_contact=True))
        await call.message.answer("🇺🇿Telefon raqamingizni yuboring", reply_markup=phone_btn)
    elif language == "ru":
        phone_btn.add(KeyboardButton(text="📱Отправить номер телефона", request_contact=True))
        await call.message.answer("🇷🇺Отправьте свой номер телефона", reply_markup=phone_btn)
    elif language == "en":
        phone_btn.add(KeyboardButton(text="📱Send phone number", request_contact=True))
        await call.message.answer("🇺🇸Send your phone number", reply_markup=phone_btn)
    await state.set_state("get_phone_number")


@dp.message_handler(IsGuest(), state="get_phone_number", content_types=ContentTypes.CONTACT)
@dp.message_handler(IsGuest(), state="get_phone_number", content_types=ContentTypes.TEXT)
async def get_phone_number(message: types.Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    await state.update_data(phone_number=phone_number)

    data = await state.get_data()
    language = data.get("language")
    if language == "uz":
        await message.answer("✍️To'liq ismingizni kiriting...", reply_markup=ReplyKeyboardRemove())
    elif language == "ru":
        await message.answer("✍️Введите ваше полное имя...", reply_markup=ReplyKeyboardRemove())
    elif language == "en":
        await message.answer("✍️Enter your full name...", reply_markup=ReplyKeyboardRemove())
    await state.set_state("get_full_name")


@dp.message_handler(IsGuest(), state="get_full_name")
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    data = await state.get_data()
    phone_number = data.get("phone_number")
    language = data.get("language")
    await db.add_user(telegram_id=message.from_user.id, fullname=full_name, phone_number=phone_number, language=language)
    if language == "uz":
        await message.answer(f"✅Siz muvaffaqiyatli ro'yxatdan o'tdingiz!", reply_markup=menu_user_uz)
    elif language == "ru":
        await message.answer(f"✅Вы успешно зарегистрировались!", reply_markup=menu_user_ru)
    elif language == "en":
        await message.answer(f"✅You have successfully registered!", reply_markup=menu_user_en)
    await state.finish()

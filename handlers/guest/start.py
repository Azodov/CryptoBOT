from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ContentTypes, ReplyKeyboardRemove

from filters import IsGuest
from keyboards.inline.userKeyboards import menu_user
from loader import dp, db


@dp.message_handler(IsGuest(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if message.get_args():
        await db.update_admin(telegram_id=int(message.from_user.id), otp=int(message.get_args()), action=None)
        await message.answer(f"Salom Admin, {message.from_user.full_name}!")
    else:
        request_phone_number = KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
        await message.answer(f"👋Assalomu alaykum Botdan foydalanish uchun telefon raqamingizni yuboring..."
                             , reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
                request_phone_number))
        await state.set_state("get_phone_number")


@dp.message_handler(IsGuest(), state="get_phone_number", content_types=ContentTypes.CONTACT)
@dp.message_handler(IsGuest(), state="get_phone_number", content_types=ContentTypes.TEXT)
async def get_phone_number(message: types.Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    await state.update_data(phone_number=phone_number)
    await message.answer("✍️To'liq ismingizni kiriting...", reply_markup=ReplyKeyboardRemove())
    await state.set_state("get_full_name")


@dp.message_handler(IsGuest(), state="get_full_name")
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    data = await state.get_data()
    phone_number = data.get("phone_number")
    await db.add_user(telegram_id=message.from_user.id, fullname=full_name, phone_number=phone_number, language="uz")
    await message.answer(f"✅Siz muvaffaqiyatli ro'yxatdan o'tdingiz!", reply_markup=menu_user)
    await state.finish()

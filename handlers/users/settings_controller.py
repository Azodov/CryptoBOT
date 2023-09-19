from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsUser
from keyboards.inline.userKeyboards import settings_uz, settings_ru, settings_en, langs_uz, langs_ru, langs_en, \
    back_uz, back_ru, back_en
from loader import dp, db


@dp.callback_query_handler(text="user:settings", state="*")
async def settings(call: CallbackQuery):
    await call.answer(cache_time=1)
    user_languege = await db.select_user(telegram_id=call.from_user.id)
    lang = user_languege['language']
    if lang == "uz":
        await call.message.edit_text(text="⚙️ Sozlamalar", reply_markup=settings_uz)
    elif lang == "ru":
        await call.message.edit_text(text="⚙️ Настройки", reply_markup=settings_ru)
    elif lang == "en":
        await call.message.edit_text(text="⚙️ Settings", reply_markup=settings_en)


@dp.callback_query_handler(IsUser(), text="user:change_language", state="*")
async def change_language(call: CallbackQuery):
    await call.answer(cache_time=1)
    user_languege = await db.select_user(telegram_id=call.from_user.id)
    lang = user_languege['language']
    if lang == "uz":
        await call.message.edit_text(text="Tilni tanlang", reply_markup=langs_uz)
    elif lang == "ru":
        await call.message.edit_text(text="Выберите язык", reply_markup=langs_ru)
    elif lang == "en":
        await call.message.edit_text(text="Choose language", reply_markup=langs_en)


@dp.callback_query_handler(IsUser(), text_contains="lang", state="*")
async def change_language(call: CallbackQuery):
    await call.answer(cache_time=1)
    lang = call.data.split(":")[-1].split("_")[-1]
    await db.update_user_language(telegram_id=call.from_user.id, language=lang)
    if lang == "uz":
        await call.message.edit_text(text="🇺🇿 Til o'zgartirildi ✅", reply_markup=back_uz)
    elif lang == "ru":
        await call.message.edit_text(text="🇷🇺 Язык изменен ✅", reply_markup=back_ru)
    elif lang == "en":
        await call.message.edit_text(text="🇬🇧 Language changed ✅", reply_markup=back_en)


@dp.callback_query_handler(IsUser(), text="user:change_name", state="*")
async def help(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    user_languege = await db.select_user(telegram_id=call.from_user.id)
    lang = user_languege['language']
    if lang == "uz":
        await call.message.edit_text(text="✍️ Ismingizni yozing", reply_markup=back_uz)
    elif lang == "ru":
        await call.message.edit_text(text="✍️ Отправьте ваше имя", reply_markup=back_ru)
    elif lang == "en":
        await call.message.edit_text(text="✍️ Send your name", reply_markup=back_en)

    await state.set_state("change_name")


@dp.message_handler(IsUser(), state="change_name")
async def change_name(message: types.Message, state: FSMContext):
    await state.finish()
    await db.update_user_fullname(telegram_id=message.from_user.id, fullname=message.text)
    user_languege = await db.select_user(telegram_id=message.from_user.id)
    lang = user_languege['language']
    if lang == "uz":
        await message.answer(text="✅ Ism o'zgartirildi", reply_markup=back_uz)
    elif lang == "ru":
        await message.answer(text="✅ Имя изменено", reply_markup=back_ru)
    elif lang == "en":
        await message.answer(text="✅ Name changed", reply_markup=back_en)


@dp.callback_query_handler(IsUser(), text="user:change_phone", state="*")
async def change_phone(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    user_languege = await db.select_user(telegram_id=call.from_user.id)
    lang = user_languege['language']
    if lang == "uz":
        await call.message.edit_text(text="📞 Telefon raqamingizni yozing", reply_markup=back_uz)
    elif lang == "ru":
        await call.message.edit_text(text="📞 Отправьте ваш номер телефона", reply_markup=back_ru)
    elif lang == "en":
        await call.message.edit_text(text="📞 Send your phone number", reply_markup=back_en)

    await state.set_state("change_phone")


@dp.message_handler(IsUser(), state="change_phone")
async def change_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    await state.finish()
    await db.update_user_phone_number(telegram_id=message.from_user.id, phone_number=phone_number)
    user_languege = await db.select_user(telegram_id=message.from_user.id)
    lang = user_languege['language']
    if lang == "uz":
        await message.answer(text="✅ Telefon raqam o'zgartirildi", reply_markup=back_uz)
    elif lang == "ru":
        await message.answer(text="✅ Номер телефона изменен", reply_markup=back_ru)
    elif lang == "en":
        await message.answer(text="✅ Phone number changed", reply_markup=back_en)

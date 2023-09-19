from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsUser
from keyboards.inline.userKeyboards import menu_user_uz, menu_user_ru, menu_user_en
from loader import dp, db


@dp.message_handler(IsUser(), CommandStart(), state="*")
async def bot_start(message: types.Message):
    if message.get_args():
        await db.update_admin(telegram_id=int(message.from_user.id), otp=int(message.get_args()), action=None)
        await message.answer(f"Salom Admin, {message.from_user.full_name}!")
    user_language = await db.select_user(telegram_id=message.from_user.id)
    lang = user_language['language']
    if lang == "uz":
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!", reply_markup=menu_user_uz)
    elif lang == "ru":
        await message.answer(f"Здравствуйте, {message.from_user.full_name}!", reply_markup=menu_user_ru)
    elif lang == "en":
        await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=menu_user_en)


@dp.callback_query_handler(IsUser(), text_contains="user:cancel", state="*")
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    user_language = await db.select_user(telegram_id=call.from_user.id)
    lang = user_language['language']
    if lang == "uz":
        await call.message.edit_text("♦️ Bosh Sahifa!", reply_markup=menu_user_uz)
    elif lang == "ru":
        await call.message.edit_text("♦️ Главная страница!", reply_markup=menu_user_ru)
    elif lang == "en":
        await call.message.edit_text("♦️ Main page!", reply_markup=menu_user_en)
    await state.finish()
    await state.reset_data()


@dp.message_handler(IsUser(), text="🏠 Bosh menyuga qaytish", state="*")
async def back_to_menu(message: types.Message, state: FSMContext):
    user_language = await db.select_user(telegram_id=message.from_user.id)
    lang = user_language['language']
    if lang == "uz":
        await message.answer("♦️ Bosh Sahifa!", reply_markup=menu_user_uz)
    elif lang == "ru":
        await message.answer("♦️ Главная страница!", reply_markup=menu_user_ru)
    elif lang == "en":
        await message.answer("♦️ Main page!", reply_markup=menu_user_en)
    await state.finish()
    await state.reset_data()

@dp.message_handler(IsUser(), text="🏠 Вернуться в главное меню", state="*")
async def back_to_menu(message: types.Message, state: FSMContext):
    user_language = await db.select_user(telegram_id=message.from_user.id)
    lang = user_language['language']
    if lang == "uz":
        await message.answer("♦️ Bosh Sahifa!", reply_markup=menu_user_uz)
    elif lang == "ru":
        await message.answer("♦️ Главная страница!", reply_markup=menu_user_ru)
    elif lang == "en":
        await message.answer("♦️ Main page!", reply_markup=menu_user_en)
    await state.finish()
    await state.reset_data()


@dp.message_handler(IsUser(), text="🏠 Back to main menu", state="*")
async def back_to_menu(message: types.Message, state: FSMContext):
    user_language = await db.select_user(telegram_id=message.from_user.id)
    lang = user_language['language']
    if lang == "uz":
        await message.answer("♦️ Bosh Sahifa!", reply_markup=menu_user_uz)
    elif lang == "ru":
        await message.answer("♦️ Главная страница!", reply_markup=menu_user_ru)
    elif lang == "en":
        await message.answer("♦️ Main page!", reply_markup=menu_user_en)
    await state.finish()
    await state.reset_data()
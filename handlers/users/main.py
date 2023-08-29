from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsUser
from keyboards.inline.userKeyboards import menu_user
from loader import dp, db


@dp.message_handler(IsUser(), CommandStart(), state="*")
async def bot_start(message: types.Message):
    if message.get_args():
        await db.update_admin(telegram_id=int(message.from_user.id), otp=int(message.get_args()), action=None)
        await message.answer(f"Salom Admin, {message.from_user.full_name}!")
    await message.answer(f"Salom Foydalanuvchi, {message.from_user.full_name}!", reply_markup=menu_user)


@dp.callback_query_handler(IsUser(), text_contains="user:cancel", state="*")
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text("♦️ Bosh Sahifa!", reply_markup=menu_user)
    await state.finish()
    await state.reset_data()

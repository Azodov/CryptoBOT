from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from filters import IsSuperAdmin
from keyboards.inline.superAdminKeyboards import menu_super_admin
from loader import db, dp


@dp.callback_query_handler(IsSuperAdmin(), text="superadmin:currency", state="*")
async def bot_currency(call: CallbackQuery):
    await call.answer(cache_time=1)
    currencies_list = await db.select_all_currencies()
    btn = []
    for currency in currencies_list:
        btn.append([InlineKeyboardButton(text=currency[1], callback_data=f"superadmin:currency:{currency[0]}")])
    btn.append([InlineKeyboardButton(text="➕ Yangi valyuta qo'shish", callback_data="superadmin:add_currency")])
    btn.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="superadmin:cancel")])
    await call.message.edit_text("Valyutalar ro'yxati:", reply_markup=InlineKeyboardMarkup(inline_keyboard=btn))


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:add_currency", state="*")
async def add_currency(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text("Yangi valyuta nomini kiriting:")
    await state.set_state("add_currency:name")


@dp.message_handler(IsSuperAdmin(), state="add_currency:name")
async def get_currency_name(message: Message, state: FSMContext):
    currency_name = message.text
    await state.update_data(currency_name=currency_name)
    await message.answer("BTC kursini kiriting:")
    await state.set_state("add_currency:btc_rate")


@dp.message_handler(IsSuperAdmin(), state="add_currency:btc_rate")
async def get_btc_rate(message: Message, state: FSMContext):
    btc_rate = message.text
    await state.update_data(btc_rate=btc_rate)
    await message.answer("ETH kursini kiriting:")
    await state.set_state("add_currency:eth_rate")


@dp.message_handler(IsSuperAdmin(), state="add_currency:eth_rate")
async def get_eth_rate(message: Message, state: FSMContext):
    eth_rate = message.text
    await state.update_data(eth_rate=eth_rate)
    await message.answer("USDT kursini kiriting:")
    await state.set_state("add_currency:usdt_rate")


@dp.message_handler(IsSuperAdmin(), state="add_currency:usdt_rate")
async def get_usdt_rate(message: Message, state: FSMContext):
    usdt_rate = message.text
    await state.update_data(usdt_rate=usdt_rate)
    await message.answer("Humo kursini kiriting:")
    await state.set_state("add_currency:humo_rate")


@dp.message_handler(IsSuperAdmin(), state="add_currency:humo_rate")
async def get_humo_rate(message: Message, state: FSMContext):
    humo_rate = message.text
    await state.update_data(humo_rate=humo_rate)
    await message.answer("Uzcard kursini kiriting:")
    await state.set_state("add_currency:uzcard_rate")


@dp.message_handler(IsSuperAdmin(), state="add_currency:uzcard_rate")
async def get_uzcard_rate(message: Message, state: FSMContext):
    uzcard_rate = message.text
    await state.update_data(uzcard_rate=uzcard_rate)
    await message.answer("Visa kursini kiriting:")
    await state.set_state("add_currency:visa_rate")


@dp.message_handler(IsSuperAdmin(), state="add_currency:visa_rate")
async def get_visa_rate(message: Message, state: FSMContext):
    visa_rate = message.text
    await state.update_data(visa_rate=visa_rate)
    data = await state.get_data()
    await db.add_currency(data["currency_name"], data["btc_rate"], data["eth_rate"], data["usdt_rate"],
                          data["humo_rate"], data["uzcard_rate"], data["visa_rate"])
    await message.answer("Valyuta muvaffaqiyatli qo'shildi!", reply_markup=menu_super_admin)
    await state.finish()


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:currency", state="*")
async def get_currency(call: CallbackQuery):
    await call.answer(cache_time=1)
    currency_id = call.data.split(":")[-1]
    currency = await db.select_currency(id=int(currency_id))
    await call.message.edit_text(f"Valyuta nomi: {currency[1]}\n"
                                 f"🪙 BTC kursi: {currency[2]}\n"
                                 f"🪙 ETH kursi: {currency[3]}\n"
                                 f"💵 USDT kursi: {currency[4]}\n"
                                 f"💳 Humo kursi: {currency[5]}\n"
                                 f"💳 Uzcard kursi: {currency[6]}\n"
                                 f"💳 Visa kursi: {currency[7]}\n",
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text="❌ O'chirish",
                                                              callback_data=f"superadmin:delete_currency:{currency[0]}"),
                                         InlineKeyboardButton(text="📈 Kursni o'zgartirish",
                                                              callback_data=f"superadmin:edit_rate:{currency[0]}")
                                     ],
                                     [
                                         InlineKeyboardButton(text="⬅️ Orqaga", callback_data="superadmin:currency")
                                     ]
                                 ]))


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:edit_rate", state="*")
async def edit_rate(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    currency_id = call.data.split(":")[-1]
    await state.update_data(currency_id=currency_id)
    await call.message.edit_text("BTC kursini kiriting:")
    await state.set_state(f"edit_rate:btc_rate")


@dp.message_handler(IsSuperAdmin(), state="edit_rate:btc_rate")
async def get_btc_rate(message: Message, state: FSMContext):
    btc_rate = message.text
    await state.update_data(btc_rate=btc_rate)
    await message.answer("ETH kursini kiriting:")
    await state.set_state("edit_rate:eth_rate")


@dp.message_handler(IsSuperAdmin(), state="edit_rate:eth_rate")
async def get_eth_rate(message: Message, state: FSMContext):
    eth_rate = message.text
    await state.update_data(eth_rate=eth_rate)
    await message.answer("USDT kursini kiriting:")
    await state.set_state("edit_rate:usdt_rate")


@dp.message_handler(IsSuperAdmin(), state="edit_rate:usdt_rate")
async def get_usdt_rate(message: Message, state: FSMContext):
    usdt_rate = message.text
    await state.update_data(usdt_rate=usdt_rate)
    await message.answer("Humo kursini kiriting:")
    await state.set_state("edit_rate:humo_rate")


@dp.message_handler(IsSuperAdmin(), state="edit_rate:humo_rate")
async def get_humo_rate(message: Message, state: FSMContext):
    humo_rate = message.text
    await state.update_data(humo_rate=humo_rate)
    await message.answer("Uzcard kursini kiriting:")
    await state.set_state("edit_rate:uzcard_rate")


@dp.message_handler(IsSuperAdmin(), state="edit_rate:uzcard_rate")
async def get_uzcard_rate(message: Message, state: FSMContext):
    uzcard_rate = message.text
    await state.update_data(uzcard_rate=uzcard_rate)
    await message.answer("Visa kursini kiriting:")
    await state.set_state("edit_rate:visa_rate")


@dp.message_handler(IsSuperAdmin(), state="edit_rate:visa_rate")
async def get_visa_rate(message: Message, state: FSMContext):
    visa_rate = message.text
    await state.update_data(visa_rate=visa_rate)
    data = await state.get_data()
    await db.update_currency(id=int(data["currency_id"]), btc_rate=data["btc_rate"], eth_rate=data["eth_rate"],
                             usdt_rate=data["usdt_rate"], humo_rate=data["humo_rate"], uzcard_rate=data["uzcard_rate"],
                             visa_rate=data["visa_rate"])
    await message.answer("Valyuta muvaffaqiyatli o'zgartirildi!", reply_markup=menu_super_admin)
    await state.finish()


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:delete_currency", state="*")
async def delete_currency(call: CallbackQuery):
    await call.answer(cache_time=1)
    currency_id = call.data.split(":")[-1]
    await db.delete_currency(id=int(currency_id))
    await call.message.edit_text("Valyuta o'chirildi!", reply_markup=menu_super_admin)

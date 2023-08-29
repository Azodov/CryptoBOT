from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton, ContentTypes

from data.config import ADMINS
from filters import IsUser
from keyboards.inline.userKeyboards import cancel, menu_user
from keyboards.inline.userKeyboards import isCorrect
from loader import dp, db, bot


@dp.callback_query_handler(IsUser(), text="user:buy", state="*")
async def select_currency(call: CallbackQuery):
    await call.answer(cache_time=1)
    currecy_list = await db.select_all_currencies()
    text = "♦️ Valyutani tanlang 👇🏻"
    btn = InlineKeyboardMarkup()
    for currency in currecy_list:
        btn.insert(InlineKeyboardButton(text=str(currency['name']), callback_data=f"user:buy:{currency['id']}"))
    await call.message.edit_text(text=text, reply_markup=btn)


@dp.callback_query_handler(IsUser(), text_contains="user:buy", state="*")
async def buy_handler(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    currency_id = call.data.split(":")[-1]
    await state.update_data(currency_id=currency_id)
    text = "♦️ Valyuta miqdorini kiriting 👇🏻"
    await call.message.edit_text(text=text, reply_markup=cancel)
    await state.set_state("buy:amount")


@dp.message_handler(IsUser(), state="buy:amount")
async def buy_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount=message.text)
    user_info = await db.select_user_wallets(user_id=int(message.from_user.id))
    text = "✅ Hamyoningiz manzilini kiriting"
    if user_info:
        text = ("✅ Hamyonningiz manzilini kiriting \n"
                "Yoki avval kiritgan hamyonlaringizdan birini tanlang 👇🏻")
        btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        for wallet in user_info:
            btn.insert(KeyboardButton(text=wallet['wallet_address']))
        await message.answer(text=text, reply_markup=btn)
    else:
        await message.answer(text=text)
    await state.set_state("buy:wallet:address")


@dp.message_handler(IsUser(), state="buy:wallet:address")
async def buy_wallet_address(message: types.Message, state: FSMContext):
    await db.update_user_wallet_address(telegram_id=int(message.from_user.id), wallet_address=message.text)
    await state.update_data(wallet_address=message.text)
    data = await state.get_data()
    currency_id = data.get("currency_id")
    amount = data.get("amount")
    wallet_address = message.text
    currency_rate = await db.select_currency(id=int(currency_id))
    text = f"""
⚠️ Buyurtmangizni tekshiring!
💰 Valyuta: {currency_rate['name']}
💵 Miqdor: {amount}
📤 Hamyon: {wallet_address}
    """
    await message.answer(text=text, reply_markup=isCorrect)
    await state.set_state("buy:isCorrect")


@dp.callback_query_handler(IsUser(), text="user:isCorrect", state="buy:isCorrect")
async def buy_isCorrect(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    currency_id = data.get("currency_id")
    amount = float(data.get("amount"))
    wallet_address = data.get("wallet_address")
    currency_rate = await db.select_currency(id=int(currency_id))
    btc_rate = format((float(currency_rate['btc_rate']) * amount), '.4f')
    eth_rate = format((float(currency_rate['eth_rate']) * amount), '.4f')
    usdt_rate = format((float(currency_rate['usdt_rate']) * amount), '.2f')
    humo_rate = format((float(currency_rate['humo_rate']) * amount))
    uzcard_rate = format((float(currency_rate['uzcard_rate']) * amount))
    visa_rate = format((float(currency_rate['visa_rate']) * amount), '.2f')
    await state.update_data(
        btc_rate=btc_rate,
        eth_rate=eth_rate,
        usdt_rate=usdt_rate,
        humo_rate=humo_rate,
        uzcard_rate=uzcard_rate,
        visa_rate=visa_rate
    )

    text = ("♦️ Kurslar bilan tanishib tolov turini tanlang 👇🏻"
            "\n\n"
            f"💰 Valyuta: {currency_rate['name']}"
            f"\n💵 Miqdor: {amount}"
            f"\n📤 Hamyon: <b><code>{wallet_address}</code></b>"
            "\n\n"
            "📈 Kurslar:"
            f"\nBTC: {btc_rate}"
            f"\nETH: {eth_rate}"
            f"\nUSDT: {usdt_rate}"
            f"\nHumo: {humo_rate}"
            f"\nUzCard: {uzcard_rate}"
            f"\nVisa: {visa_rate}\n\n"
            )
    payment_method_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 Humo", callback_data="user:payment_method:humo")
            ],
            [
                InlineKeyboardButton(text="💳 UzCard", callback_data="user:payment_method:uzcard")
            ],
            [
                InlineKeyboardButton(text="💳 Visa", callback_data="user:payment_method:visa")
            ],
            [
                InlineKeyboardButton(text="👛 BTC", callback_data="user:payment_method:btc")
            ],
            [
                InlineKeyboardButton(text="👛 ETH", callback_data="user:payment_method:eth")
            ],
            [
                InlineKeyboardButton(text="👛 USDT", callback_data="user:payment_method:usdt")
            ],
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data="user:cancel")
            ]
        ]
    )
    await call.message.edit_text(text=text, reply_markup=payment_method_btn)


@dp.callback_query_handler(IsUser(), text_contains="user:payment_method", state="*")
async def payment_method(call: CallbackQuery, state: FSMContext):
    method = str(call.data.split(":")[-1])
    await state.update_data(method=method)
    data = await state.get_data()
    currency_id = data.get("currency_id")
    wallet_address = data.get("wallet_address")
    currency_rate = await db.select_currency(id=int(currency_id))

    if method == "humo" or method == "uzcard" or method == "visa":
        text = ("♦️ Quydagi kartaga to'lov amalga oshiriladi 👇🏻\n\n"
                "Ma'lumotlar:\n"
                "🏦 Bank: <b>Ipak Yo'li</b>\n"
                "💳 Karta: <b><code>9860 1701 0971 8693</code></b>\n"
                "👤 Ism: <b>SHOHBOZ MAMARASULOV</b>\n"
                f"💵 Summa: <b>{data.get('humo_rate')}</b>\n"
                f"💰 Tanlangan Valyuta: <b>{currency_rate['name']}</b>\n"
                f"📤 Ko'rsatilgan Hamyon: <b><code>{wallet_address}</code></b>\n"
                "\n"
                "To'lov amalga oshirilgandan so'ng <b>📸 Chek rasmini</b> yuboring"
                )
        await call.message.edit_text(text=text, reply_markup=cancel)
    elif method == "btc":
        text = (f"♦️ Quydagi hamyonga to'lov amalga oshiriladi 👇🏻\n\n"
                f"💾 Ma'lumotlar:\n"
                f"👛 Hamyon raqami: <b><code>1MeuKsgXqba8temNYVdFv33boRFSrGAaq6</code></b>\n"
                f"⚠️ Set: <b>Bitcoin</b>\n"
                f"💵 Miqdor: <b>{data.get('btc_rate')}</b>\n"
                f"💰 Tanlangan Valyuta: <b>{currency_rate['name']}</b>\n"
                f"📤 Ko'rsatilgan Hamyon: <b><code>{wallet_address}</code></b>\n"
                "\n"
                "To'lov amalga oshirilgandan so'ng <b>📸 Chek rasmini</b> yuboring"
                )
        await call.message.edit_text(text=text, reply_markup=cancel)
    elif method == "eth":
        text = (f"♦️ Quydagi hamyonga to'lov amalga oshiriladi 👇🏻\n\n"
                f"💾 Ma'lumotlar:\n"
                f"👛 Hamyon raqami: <b><code>0xa2b42c2845657d2bb9f07d583bbe0f7f7c3861dd</code></b>\n"
                f"⚠️ Set: <b>Ethereum (ERC20)</b>\n"
                f"💵 Miqdor: <b>{data.get('eth_rate')}</b>\n"
                f"💰 Tanlangan Valyuta: <b>{currency_rate['name']}</b>\n"
                f"📤 Ko'rsatilgan Hamyon: <b><code>{wallet_address}</code></b>\n"
                "\n"
                "To'lov amalga oshirilgandan so'ng <b>📸 Chek rasmini</b> yuboring"
                )
        await call.message.edit_text(text=text, reply_markup=cancel)
    elif method == "usdt":
        text = (f"♦️ Quydagi hamyonga to'lov amalga oshiriladi 👇🏻\n\n"
                f"💾 Ma'lumotlar:\n"
                f"👛 Hamyon raqami: <b><code>TMZRhHYnQgJ2L1FWvVPua1jdLKzMdG5mHk</code></b>\n"
                f"⚠️ Set: <b>TRC20</b>\n"
                f"💵 Summa: <b>{data.get('usdt_rate')}</b>\n"
                f"💰 Tanlangan Valyuta: <b>{currency_rate['name']}</b>\n"
                f"📤 Ko'rsatilgan Hamyon: <b><code>{wallet_address}</code></b>\n"
                "\n"
                "To'lov amalga oshirilgandan so'ng <b>📸 Chek rasmini</b> yuboring"
                )

        await call.message.edit_text(text=text, reply_markup=cancel)
    await state.update_data(method=method)
    await state.set_state("get:cheque:photo")


@dp.message_handler(IsUser(), state="get:cheque:photo", content_types=ContentTypes.PHOTO)
async def get_cheque_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photo_file_id = message.photo[-1].file_id
    method = data.get("method")
    if method == "humo":
        method = "💳 Humo"
    elif method == "uzcard":
        method = "💳 UzCard"
    elif method == "visa":
        method = "💳 Visa"
    elif method == "btc":
        method = "👛 BTC"
    elif method == "eth":
        method = "👛 ETH"
    elif method == "usdt":
        method = "👛 USDT"
    order_id = await db.add_order(user_id=int(message.from_user.id), currency_id=int(data.get("currency_id")),
                                  amount=data.get("amount"), wallet_address=data.get("wallet_address"),
                                  payment_method=method, cheques=photo_file_id)
    user_info = await db.select_user(telegram_id=int(message.from_user.id))
    currency = await db.select_currency(id=int(data.get("currency_id")))
    text = ("✅ Buyurtma muvaffaqiyatli qabul qilindi!"
            "\n\n"
            f"🆔 Buyurtma raqami: <b>#{order_id['id']}</b>")
    text_for_admin = (f"🆔 Buyurtma raqami: <b>{order_id['id']}</b>\n"
                      f"👤 Foydalanuvchi: <b>{user_info['fullname']}</b>\n"
                      f"📞 Telefon raqami: <b>{user_info['phone_number']}</b>\n"
                      f"💰 Valyuta: <b>{currency['name']}</b>\n"
                      f"💵 Miqdor: <b>{data.get('amount')}</b>\n"
                      f"📤 Hamyon: <b>{data.get('wallet_address')}</b>\n"
                      f"💳 To'lov usuli: <b>{method}</b>\n"
                      f"🕔 Vaqt: <b>{order_id['created_at']}</b>\n"
                      f"⏳ Status: <b>Jarayonda...</b>\n"
                      )
    btn_for_admin = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"superadmin:confirm_order:{order_id['id']}")
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"superadmin:order_cancel:{order_id['id']}")
            ]
        ]
    )
    await message.answer(text=text, reply_markup=menu_user)
    await state.finish()
    await state.reset_data()

    for admin in ADMINS:
        await bot.send_photo(chat_id=admin, photo=photo_file_id, caption=text_for_admin, reply_markup=btn_for_admin)

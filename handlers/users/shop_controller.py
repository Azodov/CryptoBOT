from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton, ContentTypes

from data.config import ADMINS
from filters import IsUser
from keyboards.inline.userKeyboards import cancel_uz, cancel_ru, cancel_en, menu_user_uz, menu_user_ru, menu_user_en
from keyboards.inline.userKeyboards import isCorrect_uz, isCorrect_ru, isCorrect_en
from loader import dp, db, bot


@dp.callback_query_handler(IsUser(), text="user:buy", state="*")
async def select_currency(call: CallbackQuery):
    global text
    await call.answer(cache_time=1)
    user_language = await db.select_user(telegram_id=call.from_user.id)
    lang = user_language['language']
    currecy_list = await db.select_all_currencies()
    btn = InlineKeyboardMarkup(row_width=1)
    for currency in currecy_list:
        btn.insert(InlineKeyboardButton(text=str(currency['name']), callback_data=f"user:buy:{currency['id']}"))

    if lang == "uz":
        text = "🪙 Kriptovalyutani tanlang 👇🏻"
        btn.insert(InlineKeyboardButton(text="🏠 Bosh menyuga qaytish", callback_data="user:cancel"))
    elif lang == "ru":
        text = "🪙 Выберите криптовалюту 👇🏻"
        btn.insert(InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="user:cancel"))
    elif lang == "en":
        text = "🪙 Select cryptocurrency 👇🏻"
        btn.insert(InlineKeyboardButton(text="🏠 Back to main menu", callback_data="user:cancel"))
    await call.message.edit_text(text=text, reply_markup=btn)


@dp.callback_query_handler(IsUser(), text_contains="user:buy", state="*")
async def buy_handler(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    currency_id = call.data.split(":")[-1]
    currency_name = await db.select_currency(id=int(currency_id))
    await state.update_data(currency_id=currency_id)
    user_language = await db.select_user(telegram_id=call.from_user.id)
    lang = user_language['language']
    cancel_btn = InlineKeyboardMarkup(row_width=1)
    text = "."
    if lang == "uz":
        text = f"{currency_name['name']} miqdorini kiriting 👇🏻"
        cancel_btn.insert(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="user:cancel"))
        cancel_btn.insert(InlineKeyboardButton(text="🔙 Orqaga", callback_data="user:buy"))
    elif lang == "ru":
        text = f"Введите количество {currency_name['name']} 👇🏻"
        cancel_btn.insert(InlineKeyboardButton(text="❌ Отменить", callback_data="user:cancel"))
        cancel_btn.insert(InlineKeyboardButton(text="🔙 Назад", callback_data="user:buy"))
    elif lang == "en":
        text = f"Enter the amount of {currency_name['name']} 👇🏻"
        cancel_btn.insert(InlineKeyboardButton(text="❌ Cancel", callback_data="user:cancel"))
        cancel_btn.insert(InlineKeyboardButton(text="🔙 Back", callback_data="user:buy"))
    await call.message.edit_text(text=text, reply_markup=cancel_btn)
    await state.set_state("buy:amount")


@dp.message_handler(IsUser(), state="buy:amount")
async def buy_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount=message.text)
    user_info = await db.select_user_wallets(user_id=int(message.from_user.id))
    user_language = await db.select_user(telegram_id=message.from_user.id)
    lang = user_language['language']
    if lang == "uz":
        text = "💼 Hamyonningiz manzilini kiriting"
        if user_info:
            text = ("💼 Hamyonningiz manzilini kiriting \n"
                    "Yoki avval kiritgan hamyonlaringizdan birini tanlang 👇🏻")
            btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
            for wallet in user_info:
                btn.insert(KeyboardButton(text=wallet['wallet_address']))
            btn.insert(KeyboardButton(text="🔙 Orqaga"))
            await message.answer(text=text, reply_markup=btn)
        else:
            await message.answer(text=text, reply_markup=cancel_uz)
    elif lang == "ru":
        text = "💼 Введите адрес кошелька"
        if user_info:
            text = ("💼 Введите адрес кошелька \n"
                    "Или выберите один из ваших ранее введенных кошельков 👇🏻")
            btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
            for wallet in user_info:
                btn.insert(KeyboardButton(text=wallet['wallet_address']))
            btn.insert(KeyboardButton(text="🔙 Назад"))
            await message.answer(text=text, reply_markup=btn)
        else:
            await message.answer(text=text, reply_markup=cancel_ru)
    elif lang == "en":
        text = "💼 Enter your wallet address"
        if user_info:
            text = ("💼 Enter your wallet address \n"
                    "Or select one of your previously entered wallets 👇🏻")
            btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
            for wallet in user_info:
                btn.insert(KeyboardButton(text=wallet['wallet_address']))
            btn.insert(KeyboardButton(text="🔙 Back"))
            await message.answer(text=text, reply_markup=btn)
        else:
            await message.answer(text=text, reply_markup=cancel_en)
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
    user_language = await db.select_user(telegram_id=message.from_user.id)
    lang = user_language['language']
    "Error"
    if lang == "uz":
        text = (f"\n"
                f"⚠️ Buyurtmangizni tekshiring⁉️\n"
                f"🪙 Kriptovalyuta: {currency_rate['name']}\n"
                f"🛒 Miqdor: {amount}\n"
                f"💼 Hamyon:  {wallet_address}\n")
        await message.answer(text=text, reply_markup=isCorrect_uz)
    elif lang == "ru":
        text = (f"\n"
                f"⚠️ Проверьте ваш заказ⁉️\n"
                f"🪙 Криптовалюта: {currency_rate['name']}\n"
                f"🛒 Количество: {amount}\n"
                f"💼 Кошелек:  {wallet_address}\n")
        await message.answer(text=text, reply_markup=isCorrect_ru)
    elif lang == "en":
        text = (f"\n"
                f"⚠️ Check your order⁉️\n"
                f"🪙 Cryptocurrency: {currency_rate['name']}\n"
                f"🛒 Amount: {amount}\n"
                f"💼 Wallet:  {wallet_address}\n")
        await message.answer(text=text, reply_markup=isCorrect_en)
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
    user_language = await db.select_user(telegram_id=call.from_user.id)
    lang = user_language['language']

    if lang == "uz":
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
    elif lang == "ru":
        text = ("♦️ Ознакомьтесь с курсами и выберите способ оплаты 👇🏻"
                "\n\n"
                f"💰 Валюта: {currency_rate['name']}"
                f"\n💵 Количество: {amount}"
                f"\n📤 Кошелек: <b><code>{wallet_address}</code></b>"
                "\n\n"
                "📈 Курсы:"
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
                    InlineKeyboardButton(text="🔙 Назад", callback_data="user:cancel")
                ]
            ]
        )
        await call.message.edit_text(text=text, reply_markup=payment_method_btn)
    elif lang == "en":
        text = ("♦️ Familiarize yourself with the rates and choose a payment method 👇🏻"
                "\n\n"
                f"💰 Currency: {currency_rate['name']}"
                f"\n💵 Amount: {amount}"
                f"\n📤 Wallet: <b><code>{wallet_address}</code></b>"
                "\n\n"
                "📈 Rates:"
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
                    InlineKeyboardButton(text="🔙 Back", callback_data="user:cancel")
                ]
            ]
        )
        await call.message.edit_text(text=text, reply_markup=payment_method_btn)
    await state.set_state("get:payment:method")


@dp.callback_query_handler(IsUser(), text_contains="user:payment_method", state="*")
async def payment_method(call: CallbackQuery, state: FSMContext):
    global text
    method = str(call.data.split(":")[-1])
    await state.update_data(method=method)
    data = await state.get_data()
    currency_id = data.get("currency_id")
    wallet_address = data.get("wallet_address")
    currency_rate = await db.select_currency(id=int(currency_id))
    user_language = await db.select_user(telegram_id=call.from_user.id)
    lang = user_language['language']
    if lang == "uz":
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
            try:
                await call.message.edit_text(text=text, reply_markup=cancel_uz)
            except Exception as e:
                print(e)
                await call.message.answer(text=text, reply_markup=cancel_uz)
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
            try:
                await call.message.edit_text(text=text, reply_markup=cancel_uz)
            except Exception as e:
                print(e)
                await call.message.answer(text=text, reply_markup=cancel_uz)
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
            try:
                await call.message.edit_text(text=text, reply_markup=cancel_uz)
            except Exception as e:
                print(e)
                await call.message.answer(text=text, reply_markup=cancel_uz)
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
        try:
            await call.message.edit_text(text=text, reply_markup=cancel_uz)
        except Exception as e:
            print(e)
            await call.message.answer(text=text, reply_markup=cancel_uz)
    elif lang == "ru":
        if method == "humo" or method == "uzcard" or method == "visa":
            text = ("♦️ Оплата будет произведена на следующую карту 👇🏻\n\n"
                    "Данные:\n"
                    "🏦 Банк: <b>Ipak Yo'li</b>\n"
                    "💳 Карта: <b><code>9860 1701 0971 8693</code></b>\n"
                    "👤 Имя: <b>SHOHBOZ MAMARASULOV</b>\n"
                    f"💵 Сумма: <b>{data.get('humo_rate')}</b>\n"
                    f"💰 Выбранная валюта: <b>{currency_rate['name']}</b>\n"
                    f"📤 Указанный кошелек: <b><code>{wallet_address}</code></b>\n"
                    "\n"
                    "После оплаты отправьте <b>чек</b>"
                    )
            await call.message.edit_text(text=text, reply_markup=cancel_ru)
        elif method == "btc":
            text = (f"♦️ Оплата будет произведена на следующий кошелек 👇🏻\n\n"
                    f"💾 Данные:\n"
                    f"👛 Номер кошелька: <b><code>1MeuKsgXqba8temNYVdFv33boRFSrGAaq6</code></b>\n"
                    f"⚠️ Set: <b>Bitcoin</b>\n"
                    f"💵 Сумма: <b>{data.get('btc_rate')}</b>\n"
                    f"💰 Выбранная валюта: <b>{currency_rate['name']}</b>\n"
                    f"📤 Указанный кошелек: <b><code>{wallet_address}</code></b>\n"
                    "\n"
                    "После оплаты отправьте <b>чек</b>"
                    )
            await call.message.edit_text(text=text, reply_markup=cancel_ru)
        elif method == "eth":
            text = (f"♦️ Оплата будет произведена на следующий кошелек 👇🏻\n\n"
                    f"💾 Данные:\n"
                    f"👛 Номер кошелька: <b><code>0xa2b42c2845657d2bb9f07d583bbe0f7f7c3861dd</code></b>\n"
                    f"⚠️ Set: <b>Ethereum (ERC20)</b>\n"
                    f"💵 Сумма: <b>{data.get('eth_rate')}</b>\n"
                    f"💰 Выбранная валюта: <b>{currency_rate['name']}</b>\n"
                    f"📤 Указанный кошелек: <b><code>{wallet_address}</code></b>\n"
                    "\n"
                    "После оплаты отправьте <b>чек</b>"
                    )
            await call.message.edit_text(text=text, reply_markup=cancel_ru)
        elif method == "usdt":
            text = (f"♦️ Оплата будет произведена на следующий кошелек 👇🏻\n\n"
                    f"💾 Данные:\n"
                    f"👛 Номер кошелька: <b><code>TMZRhHYnQgJ2L1FWvVPua1jdLKzMdG5mHk</code></b>\n"
                    f"⚠️ Set: <b>TRC20</b>\n"
                    f"💵 Сумма: <b>{data.get('usdt_rate')}</b>\n"
                    f"💰 Выбранная валюта: <b>{currency_rate['name']}</b>\n"
                    f"📤 Указанный кошелек: <b><code>{wallet_address}</code></b>\n"
                    "\n"
                    "После оплаты отправьте <b>чек</b>"
                    )
            await call.message.edit_text(text=text, reply_markup=cancel_ru)
    elif lang == "en":
        text = "Error"
        if method == "humo" or method == "uzcard" or method == "visa":
            text = ("♦️ Payment will be made to the following card 👇🏻\n\n"
                    "Data:\n"
                    "🏦 Bank: <b>Ipak Yo'li</b>\n"
                    "💳 Card: <b><code>9860 1701 0971 8693</code></b>\n"
                    "👤 Name: <b>SHOHBOZ MAMARASULOV</b>\n"
                    f"💵 Amount: <b>{data.get('humo_rate')}</b>\n"
                    f"💰 Selected currency: <b>{currency_rate['name']}</b>\n"
                    f"📤 Specified wallet: <b><code>{wallet_address}</code></b>\n"
                    "\n"
                    "After payment, send a <b>check</b>"
                    )
            await call.message.edit_text(text=text, reply_markup=cancel_en)
        elif method == "btc":
            text = (f"♦️ Payment will be made to the following wallet 👇🏻\n\n"
                    f"💾 Data:\n"
                    f"👛 Wallet number: <b><code>1MeuKsgXqba8temNYVdFv33boRFSrGAaq6</code></b>\n"
                    f"⚠️ Set: <b>Bitcoin</b>\n"
                    f"💵 Amount: <b>{data.get('btc_rate')}</b>\n"
                    f"💰 Selected currency: <b>{currency_rate['name']}</b>\n"
                    f"📤 Specified wallet: <b><code>{wallet_address}</code></b>\n"
                    "\n"
                    "After payment, send a <b>check</b>"
                    )
            await call.message.edit_text(text=text, reply_markup=cancel_en)
        elif method == "eth":
            text = (f"♦️ Payment will be made to the following wallet 👇🏻\n\n"
                    f"💾 Data:\n"
                    f"👛 Wallet number: <b><code>0xa2b42c2845657d2bb9f07d583bbe0f7f7c3861dd</code></b>\n"
                    f"⚠️ Set: <b>Ethereum (ERC20)</b>\n"
                    f"💵 Amount: <b>{data.get('eth_rate')}</b>\n"
                    f"💰 Selected currency: <b>{currency_rate['name']}</b>\n"
                    f"📤 Specified wallet: <b><code>{wallet_address}</code></b>\n"
                    "\n"
                    "After payment, send a <b>check</b>"
                    )
            await call.message.edit_text(text=text, reply_markup=cancel_en)
        elif method == "usdt":
            text = (f"♦️ Payment will be made to the following wallet 👇🏻\n\n"
                    f"💾 Data:\n"
                    f"👛 Wallet number: <b><code>TMZRhHYnQgJ2L1FWvVPua1jdLKzMdG5mHk</code></b>\n"
                    f"⚠️ Set: <b>TRC20</b>\n"
                    f"💵 Amount: <b>{data.get('usdt_rate')}</b>\n"
                    f"💰 Selected currency: <b>{currency_rate['name']}</b>\n"
                    f"📤 Specified wallet: <b><code>{wallet_address}</code></b>\n"
                    "\n"
                    "After payment, send a <b>check</b>"
                    )
            await call.message.edit_text(text=text, reply_markup=cancel_en)
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
    user_language = await db.select_user(telegram_id=message.from_user.id)
    lang = user_language['language']
    if lang == "uz":
        text = ("✅ Buyurtma muvaffaqiyatli qabul qilindi!"
                "\n\n"
                f"🆔 Buyurtma raqami: <b>#{order_id['id']}</b>")

        await message.answer(text=text, reply_markup=menu_user_uz)
    elif lang == "ru":
        text = ("✅ Заказ успешно принят!"
                "\n\n"
                f"🆔 Номер заказа: <b>#{order_id['id']}</b>")
        await message.answer(text=text, reply_markup=menu_user_ru)
    elif lang == "en":
        text = ("✅ Order accepted successfully!"
                "\n\n"
                f"🆔 Order number: <b>#{order_id['id']}</b>")
        await message.answer(text=text, reply_markup=menu_user_en)

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

    await state.finish()
    await state.reset_data()

    for admin in ADMINS:
        await bot.send_photo(chat_id=admin, photo=photo_file_id, caption=text_for_admin, reply_markup=btn_for_admin)

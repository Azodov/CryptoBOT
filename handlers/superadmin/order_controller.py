from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from filters import IsSuperAdmin
from loader import dp, db, bot


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:confirm_order", state="*")
async def confirm_order(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    order_id = call.data.split(":")[-1]
    order = await db.select_order(id=int(order_id))
    currency = await db.select_currency(id=int(order['currency_id']))
    user = await db.select_user(telegram_id=order['user_id'])
    caption = (f"🆔 Buyurtma raqami: <b>#{order['id']}</b>\n"
               f"👤 Foydalanuvchi: <b>{user['fullname']}</b>\n"
               f"📞 Telefon raqami: <b>{user['phone_number']}</b>\n"
               f"💰 Valyuta: <b>{currency['name']}</b>\n"
               f"💵 Miqdor: <b>{order['amount']}</b>\n"
               f"📤 Hamyon: <b>{order['wallet_address']}</b>\n"
               f"💳 To'lov usuli: <b>{order['payment_method']}</b>\n"
               f"🕔 Vaqt: <b>{order['created_at']}</b>\n"
               f"✅ Status: <b>Tasdiqlangan</b>\n"
               )
    if order['status'] == "SUCCESS":
        await call.message.edit_caption(caption, reply_markup=None)
        return
    else:
        await db.update_order_status(id=int(order_id), status="SUCCESS")
        await call.message.edit_caption(caption, reply_markup=None)
        await bot.send_message(chat_id=order['user_id'],
                               text=f"✅ Sizning #{order['id']} buyurtmangiz muvaffaqiyatli amalga oshirildi!\n"
                                    f"👛 Sizning hisobingizga {order['amount']} {currency['name']} yuborildi!\n\n"
                                    f'⚠️ Agar tushmagan bo`lsa "🆘 Yordam" bo`limida ko`rsatilgan adminga murajat '
                                    f'qiling!',
                               reply_markup=ReplyKeyboardRemove())


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:order_cancel", state="*")
async def cancel_order(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    order_id = call.data.split(":")[-1]
    order = await db.select_order(id=int(order_id))
    currency = await db.select_currency(id=int(order['currency_id']))
    user = await db.select_user(telegram_id=order['user_id'])
    caption = (f"🆔 Buyurtma raqami: <b>#{order['id']}</b>\n"
               f"👤 Foydalanuvchi: <b>{user['fullname']}</b>\n"
               f"📞 Telefon raqami: <b>{user['phone_number']}</b>\n"
               f"💰 Valyuta: <b>{currency['name']}</b>\n"
               f"💵 Miqdor: <b>{order['amount']}</b>\n"
               f"📤 Hamyon: <b>{order['wallet_address']}</b>\n"
               f"💳 To'lov usuli: <b>{order['payment_method']}</b>\n"
               f"🕔 Vaqt: <b>{order['created_at']}</b>\n"
               f"❌ Status: <b>Bekor qilindi</b>\n"
               )
    if order['status'] == "CANCELED":
        await call.message.edit_caption(caption, reply_markup=None)
        return
    else:
        await db.update_order_status(id=int(order_id), status="CANCELED")
        await call.message.edit_caption(caption, reply_markup=None)
        await bot.send_message(chat_id=order['user_id'],
                               text=f"❌ Sizning #{order['id']} raqamli buyurtmangiz bekor qilindi!\n"
                                    f"'🆘 Yordam' bo'limida ko'rsatilgan adminga murajat qiling!",
                               reply_markup=ReplyKeyboardRemove())

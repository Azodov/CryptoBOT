from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsUser
from keyboards.inline.userKeyboards import settings_uz, settings_ru, settings_en, langs_uz, langs_ru, langs_en, \
    back_uz, back_ru, back_en
from loader import dp, db


@dp.callback_query_handler(IsUser(), text="user:about", state="*")
async def settings(call: CallbackQuery):
    await call.answer(cache_time=1)
    user_languege = await db.select_user(telegram_id=call.from_user.id)
    lang = user_languege['language']
    if lang == "uz":
        text = """
        Solex24Bot barchaga kriptovalyuta portfelini yaratish uchun samarali va foydali echimlarni taqdim etadi.
        
Bizning maqsadimiz nima?
Raqamli valyutaning afzalliklaridan foydalanishda imkon qadar ko'proq odamlarga yordam berish.
        
Nega buni qilyapmiz?
Dunyo bugun boshdan kechirayotgan kriptovalyutaga ehtiyoj mustaqil raqamli pullar kelajak ekanligini yaqqol ko‘rsatib turibdi. Inflyatsiyaga duchor bo'lgan va beqaror iqtisodiyotga qaramli bo'lgan milliy valyutalar asta-sekin o'z o'rnini yo'qotmoqda. Yangi moliyaviy davr keladi va bu voqeadan chetda qolmaslik kerak.
        """
        await call.message.edit_text(text=text, reply_markup=back_uz)
    elif lang == "ru":
        text = """
        Solex24Bot предлагает эффективные и полезные решения для создания криптовалютного кошелька всем.
        
Наша цель?
Помочь как можно большему количеству людей в использовании преимуществ цифровой валюты.

Почему мы это делаем?
Сегодня мир показывает, что цифровые деньги будущее. Национальные валюты, которые подвержены инфляции и нестабильной экономике, постепенно теряют свои позиции. Наступает новая финансовая эра, и нам нужно быть впереди этого события.
        """
        await call.message.edit_text(text=text, reply_markup=back_ru)
    elif lang == "en":
        text = """
        Solex24Bot offers effective and useful solutions for creating a cryptocurrency wallet to everyone.
        
        
Our goal?
To help as many people as possible in using the benefits of digital currency.

Why are we doing this?
Today the world shows that digital money is the future. National currencies, which are subject to inflation and an unstable economy, are gradually losing their positions. A new financial era is coming and we need to be ahead of this event.
        """
        await call.message.edit_text(text=text, reply_markup=back_en)
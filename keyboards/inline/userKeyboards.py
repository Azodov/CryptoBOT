from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_user_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Sotib olish", callback_data="user:buy")
        ],
        [
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="user:settings")
        ],
        [
            InlineKeyboardButton(text="📚 Qo’llanma", callback_data="user:help")
        ],
        [
            InlineKeyboardButton(text=" 📋 Biz haqimizda!", callback_data="user:about")
        ],
        [
            InlineKeyboardButton(text="✉️ Xabar yuborish", url="https://t.me/shahbozGold")
        ]
    ]
)
menu_user_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Купить", callback_data="user:buy")
        ],
        [
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="user:settings")
        ],
        [
            InlineKeyboardButton(text="📚 Помощь", callback_data="user:help"),
        ],
        [
            InlineKeyboardButton(text=" 📋 О нас!", callback_data="user:about")
        ],
        [
            InlineKeyboardButton(text="✉️ Написать нам", url="https://t.me/shahbozGold")
        ]
    ]
)

menu_user_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Buy", callback_data="user:buy")
        ],
        [
            InlineKeyboardButton(text="⚙️ Settings", callback_data="user:settings")
        ],
        [
            InlineKeyboardButton(text="📚 Help", callback_data="user:help"),
        ],
        [
            InlineKeyboardButton(text=" 📋 About us!", callback_data="user:about")
        ],
        [
            InlineKeyboardButton(text="✉️ Write to us", url="https://t.me/shahbozGold")
        ]
    ]
)

settings_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🌐 Tilni o'zgartirish",
                                 callback_data="user:change_language")
        ],
        [
            InlineKeyboardButton(text="👤 Ismni o’zgartirish", callback_data="user:change_name")
        ],
        [
            InlineKeyboardButton(text="☎️ Telefon raqamni almashtirish", callback_data="user:change_phone")
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="user:cancel")
        ]
    ]
)

settings_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🌐 Изменить язык",
                                 callback_data="user:change_language")
        ],
        [
            InlineKeyboardButton(text="👤 Изменить имя", callback_data="user:change_name")
        ],
        [
            InlineKeyboardButton(text="☎️ Изменить номер телефона", callback_data="user:change_phone")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="user:cancel")
        ]
    ]
)

settings_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🌐 Change language",
                                    callback_data="user:change_language")
        ],
        [
            InlineKeyboardButton(text="👤 Change name", callback_data="user:change_name")
        ],
        [
            InlineKeyboardButton(text="☎️ Change phone number", callback_data="user:change_phone")
        ],
        [
            InlineKeyboardButton(text="🔙 Back", callback_data="user:cancel")
        ]
    ]
)

cancel_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🏠 Bosh menyuga qaytish", callback_data="user:cancel")
        ]
    ]
)
cancel_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="user:cancel")
        ]
    ]
)

cancel_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🏠 Back to main menu", callback_data="user:cancel")
        ]
    ]
)

back_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="user:cancel")
        ]
    ]
)

back_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="user:cancel")
        ]
    ]
)

back_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Back", callback_data="user:cancel")
        ]
    ]
)

isCorrect_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="user:isCorrect")
        ],
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="user:cancel")
        ],
        [
            InlineKeyboardButton(text="🏠 Bosh menyuga qaytish", callback_data="user:cancel")
        ]
    ]
)

isCorrect_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="user:isCorrect")
        ],
        [
            InlineKeyboardButton(text="❌ Отменить", callback_data="user:cancel")
        ],
        [
            InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="user:cancel")
        ]
    ]
)

isCorrect_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm", callback_data="user:isCorrect")
        ],
        [
            InlineKeyboardButton(text="❌ Cancel", callback_data="user:cancel")
        ],
        [
            InlineKeyboardButton(text="🏠 Back to main menu", callback_data="user:cancel")
        ]
    ]
)

langs_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="user:lang_uz")
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Ruscha", callback_data="user:lang_ru")
        ],
        [
            InlineKeyboardButton(text="🇬🇧 Inglizcha", callback_data="user:lang_en")
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="user:cancel")
        ]
    ]
)

langs_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 Узбекский", callback_data="user:lang_uz")
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="user:lang_ru")
        ],
        [
            InlineKeyboardButton(text="🇬🇧 Английский", callback_data="user:lang_en")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="user:cancel")
        ]
    ]
)

langs_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 Uzbek", callback_data="user:lang_uz")
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Russian", callback_data="user:lang_ru")
        ],
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data="user:lang_en")
        ],
        [
            InlineKeyboardButton(text="🔙 Back", callback_data="user:cancel")
        ]
    ]
)

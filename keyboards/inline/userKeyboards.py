from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Sotib Olish", callback_data="user:buy")
        ],
        [
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="user:settings")
        ],
        [
            InlineKeyboardButton(text="🆘 Yordam", callback_data="user:help"),
        ]
    ]
)

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🌐 Tilni o'zgartirish",
                                 callback_data="user:change_language")
        ],
        [
            InlineKeyboardButton(text="👛 Hamyonni o'zgartirish", callback_data="user:change_wallet")
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="user:back")
        ]
    ]
)

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="user:cancel")
        ]
    ]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="user:cancel")
        ]
    ]
)

isCorrect = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ To'g'ri", callback_data="user:isCorrect")
        ],
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="user:cancel")
        ]
    ]
)

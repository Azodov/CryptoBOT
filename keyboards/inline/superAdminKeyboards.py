from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_super_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👨‍💻 Adminlar", callback_data="superadmin:admins"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="superadmin:stat"),
        ],
        [
            InlineKeyboardButton(text="💲 Valyutalar", callback_data="superadmin:currency")
        ],
        [
            InlineKeyboardButton(text="📝 Reklama yuborish", callback_data="superadmin:send_ads"),
        ]
    ]
)

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="superadmin:cancel")
        ]
    ]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="superadmin:cancel")
        ]
    ]
)

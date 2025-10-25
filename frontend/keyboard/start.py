from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

pre_start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="english 🇺🇸", callback_data="lang_en"),
            KeyboardButton(text="русский 🇷🇺", callback_data="lang_ru"),
            KeyboardButton(text="español 🇪🇸", callback_data="lang_es"),
            KeyboardButton(text="français 🇫🇷", callback_data="lang_fr"),
            KeyboardButton(text="italiano 🇮🇹", callback_data="lang_it"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder="Choose a language:"
)

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Roll 🎲"),
            KeyboardButton(text="Help ❓"),
        ],
        [
            KeyboardButton(text="Profile 👤"),
            KeyboardButton(text="Top up 🔝"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder="Choose an option..."
)

keyboard_stars = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="15 ⭐", callback_data="star15"),
            InlineKeyboardButton(text="50 ⭐", callback_data="star50"),
            InlineKeyboardButton(text="75 ⭐", callback_data="star75"),
            InlineKeyboardButton(text="100 ⭐", callback_data="star100"),
        ],
        [
            InlineKeyboardButton(text="150 ⭐", callback_data="star150"),
            InlineKeyboardButton(text="250 ⭐", callback_data="star250"),
            InlineKeyboardButton(text="350 ⭐", callback_data="star350"),
            InlineKeyboardButton(text="750 ⭐", callback_data="star750"),
        ],
        [
            InlineKeyboardButton(text="1 000 ⭐", callback_data="star1000"),
            InlineKeyboardButton(text="1 500 ⭐", callback_data="star1500"),
            InlineKeyboardButton(text="2 500 ⭐", callback_data="star2500"),
            InlineKeyboardButton(text="5 000 ⭐", callback_data="star5000"),
        ],
        [
            InlineKeyboardButton(text="10 000 ⭐", callback_data="star10000"),
            InlineKeyboardButton(text="25 000 ⭐", callback_data="star25000"),
            InlineKeyboardButton(text="35 000 ⭐", callback_data="star35000"),
            InlineKeyboardButton(text="50 000 ⭐", callback_data="star50000"),
        ],
        [
            InlineKeyboardButton(text="100 000 ⭐", callback_data="star100000"),
            InlineKeyboardButton(text="150 000 ⭐", callback_data="star150000"),
            InlineKeyboardButton(text="500 000 ⭐", callback_data="star500000"),
        ],
        [
            InlineKeyboardButton(text="1 000 000 ⭐", callback_data="star1000000"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder="Choose a payment amount:"
    )

game_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Dice 🎲", callback_data="game_dice"),
            KeyboardButton(text="Target 🎯", callback_data="game_target"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder="Choose a game to play:"
)

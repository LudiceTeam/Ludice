from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Roll 🎲"),
            KeyboardButton(text="Help ❓"),
        ],
        {
            KeyboardButton(text="Profile 👤"),
            KeyboardButton(text="Statictic 📊"),
        }
    ],
    resize_keyboard=True,
   input_field_placeholder="Choose an option..."
)

statictic_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Back ⬅️")
        ]
    ]
)

del_keyboard = ReplyKeyboardRemove()
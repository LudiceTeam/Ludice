from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Roll 🎲"),
            KeyboardButton(text="Help ❓"),
        ],
        {
            KeyboardButton(text="Profile 👤"),
            KeyboardButton(text="About ℹ️"),
        }
    ],
    resize_keyboard=True,
   input_field_placeholder="Choose an option..."
)

del_keyboard = ReplyKeyboardRemove()
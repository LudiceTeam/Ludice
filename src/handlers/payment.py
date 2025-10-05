from aiogram.utils.keyboard import InlineKeyboardBuilder  
  
  
def tw_payment_keyboard():  
    builder = InlineKeyboardBuilder()  
    builder.button(text=f"Pay 20 ⭐️", pay=True)  
    return builder.as_markup()
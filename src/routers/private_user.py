from aiogram import F,Router, types
from aiogram.types import LabeledPrice
from aiogram.filters import CommandStart

from handlers.payment import tw_payment_keyboard
from keyboard import answer

start_router = Router()
game = Router()

@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Welcome to the ludicé bot. Choose an option:", reply_markup=answer.start_kb)

@start_router.message(F.text == "Top up 🔝")
async def stars(message: types.Message):
    await message.answer("Choose a payment amount:", reply_markup=answer.keyboard_stars)


@start_router.callback_query(F.data == "star15")
async def handle_star15(callback: types.CallbackQuery):
    prices = [LabeledPrice(label="15 ⭐", amount=20)]
    await callback.message.answer_invoice(
        title="❖ Top up 15⭐",
        description="Your account will be credited with 15⭐ for 20⭐ when you complete the Telegram Stars payment.",
        payload="topup_20",
        provider_token="",    
        currency="XTR",
        prices=prices,
        reply_markup=tw_payment_keyboard(),
    )
    await callback.answer() 
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()
    
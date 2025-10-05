from aiogram import F,Router, types
from aiogram.types import LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from keyboard import start

start_router = Router()
payment_router = Router()
game = Router()

@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Welcome to the ludicé bot. Choose an option:", reply_markup=start.start_kb)

@start_router.message(F.text == "Top up 🔝")
async def stars(message: types.Message):
    await message.answer("Choose a payment amount:", reply_markup=start.keyboard_stars)


@start_router.callback_query(F.data == "star15")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(label="15 ⭐", amount=20)]
    
    pay_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pay 20 ⭐", pay=True)]]
    )
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 15 stars for 20 starts when you complete the payment.",
        payload="topup_20",
        provider_token="",
        prices=prices,  
        currency="XTR",    
        reply_markup=pay_kb
    )

    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None)

@start_router.pre_checkout_query()
async def pre_checkout(pre_q: PreCheckoutQuery):
    print("💫 pre_checkout_query получен")
    await pre_q.answer(ok=True)


@start_router.message(F.successful_payment)
async def payment_success(msg: types.Message):
    sp = msg.successful_payment
    print("✅ Successful Payment:", sp)
    await msg.answer(
        f"✅ Your payment has been added to your balance. Thank you for choosing Ludicé"
    )
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

#15 stars
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

# 50 stars
@start_router.callback_query(F.data == "star50")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(lebel="50 ⭐", amount=67)]
    
    pay_kb = InlineKeyboardMarkup(
        InlineKeyboardButton(text="Pay 67 ⭐", pay=True)
    )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 50 stars for 67 starts when you complete the payment.",
        playload="topup_67",
        provider_token="",
        prices=prices,
        currency ="XTR",
        reply_markup=pay_kb
    )
    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 

#75 stars
@start_router.callback_query(F == "star75")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(lebel="75 ⭐", amount=100)]
    
    pay_kb = InlineKeyboardMarkup(
        InlineKeyboardButton(text="Pay 100 ⭐")
    )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        discription="Your account will be credited with 75 stars for 100 starts when you complete the payment.",
        playload="topup_100",
        provider_token="",
        prices=prices,
        currency ="XTR",
        reply_markup=pay_kb
    )
    
    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 

#100 stars
@start_router.callback_query(F.data == "star100")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(lebel="100 ⭐",amount=133)] 
    pay_kb = InlineKeyboardMarkup(
        InlineKeyboardButton(text="Pay 133 ⭐")
        )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        discription="Your account will be credited with 100 stars for 133 starts when you complete the payment.",
        playload="topup_133",
        provider_token="",
        prices=prices,
        currency ="XTR",
        reply_markup=pay_kb
    )
    
    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 

#150 stars
@start_router.callback_query(F.data == "star150")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(lebel="150 ⭐",amount=200)] 
    pay_kb = InlineKeyboardMarkup(
        InlineKeyboardButton(text="Pay 200 ⭐")
        )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        discription="Your account will be credited with 150 stars for 200 starts when you complete the payment.",
        playload="topup_150",
        provider_token="",
        prices=prices,
        currency ="XTR",
        reply_markup=pay_kb
    )
    
    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 

#250 stars
@start_router.callback_query(F.data == "star250")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(lebel="250 ⭐",amount=333)] 
    pay_kb = InlineKeyboardMarkup(
        InlineKeyboardButton(text="Pay 333 ⭐")
        )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        discription="Your account will be credited with 250 stars for 333 starts when you complete the payment.",
        playload="topup_333",
        provider_token="",
        prices=prices,
        currency ="XTR",
        reply_markup=pay_kb
    )
    
    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 

@start_router.pre_checkout_query()
async def pre_checkout(pre_q: PreCheckoutQuery):
    print("💫 pre_checkout_query ")
    await pre_q.answer(ok=True)


@start_router.message(F.successful_payment)
async def payment_success(msg: types.Message):
    sp = msg.successful_payment
    print("✅ Successful Payment:", sp)
    await msg.answer(
        f"✅ Your payment has been added to your balance. Thank you for choosing Ludicé"
    )
from aiogram import F,Router, types
from aiogram.types import LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from keyboard import start
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
import asyncio
import os
import requests
import json
import hashlib
import hmac





# Legal text import
from common.legal_text import TERMS_FULL

# Gambling reminder function
GAMBLING_REMINDER = """
⚠️ **Responsible Gaming Reminder**

• Only bet what you can afford to lose
• Gambling should be entertainment, not income
• Set limits and stick to them
• Take breaks regularly

🔞 By continuing, you confirm you are 18+ and accept the risks.
"""

async def show_gambling_reminder(message):
    """Show responsible gambling reminder before playing."""
    await message.answer(GAMBLING_REMINDER, parse_mode="Markdown")

load_dotenv(find_dotenv())
secret_token = os.getenv("secret_token")

# State group
class BetStates(StatesGroup):
    waiting_for_bet = State()

class LegalStates(StatesGroup):
    """FSM states for terms acceptance flow."""
    waiting_for_acceptance = State()
    age_verification = State()


API_URL = "http://127.0.0.1:8000/register"

# Routers
start_router = Router()
payment_router = Router()
game_router = Router()
legal_router = Router()

# Helper function for legal keyboard
def get_legal_nav_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for terms acceptance."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ I Accept (18+)", callback_data="accept_terms"),
            InlineKeyboardButton(text="📖 Read Full Terms", callback_data="view_full_terms")
        ],
        [
            InlineKeyboardButton(text="❌ I Decline", callback_data="decline_terms")
        ]
    ])


@start_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Show terms and set FSM state to wait for acceptance
    await state.set_state(LegalStates.waiting_for_acceptance)
    await message.answer(
        TERMS_FULL,
        parse_mode="Markdown",
        reply_markup=get_legal_nav_keyboard()
    )


# Callback handlers for terms acceptance
@start_router.callback_query(F.data == "accept_terms", LegalStates.waiting_for_acceptance)
async def accept_terms_handler(callback: types.CallbackQuery, state: FSMContext):
    """Handle user accepting terms of service."""
    user_id = callback.from_user.id

    await state.clear()
    await callback.message.edit_text("✅ Thank you for accepting the terms!")
    await callback.message.answer(
        "Welcome to Ludicé! Choose an option:",
        reply_markup=start.start_kb
    )
    await callback.answer()


@start_router.callback_query(F.data == "decline_terms", LegalStates.waiting_for_acceptance)
async def decline_terms_handler(callback: types.CallbackQuery, state: FSMContext):
    """Handle user declining terms of service."""
    await state.clear()
    await callback.message.edit_text(
        "❌ You must accept the terms to use Ludicé.\n\n"
        "If you change your mind, use /start to try again."
    )
    await callback.answer()


@start_router.callback_query(F.data == "view_full_terms", LegalStates.waiting_for_acceptance)
async def view_full_terms_handler(callback: types.CallbackQuery):
    """Show full terms in a separate message."""
    await callback.answer("Showing full terms...")
    await callback.message.answer(
        f"{TERMS_FULL}\n\n"
        "Please return to the previous message to accept or decline.",
        parse_mode="Markdown"
    )


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
    prices = [LabeledPrice(label="50 ⭐", amount=67)]
    
    pay_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pay 67 ⭐", pay=True)]]
    )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 50 stars for 67 starts when you complete the payment.",
        payload="topup_67",
        provider_token="",
        prices=prices,
        currency ="XTR",
        reply_markup=pay_kb
    )
    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 

#75 stars 100
@start_router.callback_query(F.data == "star75")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(label="75 ⭐", amount=100)]
    
    pay_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pay 100 ⭐", pay=True)]]
    )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 75 stars for 100 starts when you complete the payment.",
        payload="topup_100",
        provider_token="",
        prices=prices,
        currency ="XTR",
        reply_markup=pay_kb
    )
    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 

#100 stars 133
@start_router.callback_query(F.data == "star100")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(label="100 ⭐", amount=133)]
    
    pay_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pay 133 ⭐", pay=True)]]
    )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 100 stars for 133 starts when you complete the payment.",
        payload="topup_133",
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
    prices = [LabeledPrice(label="150 ⭐", amount=200)]
    
    pay_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pay 200 ⭐", pay=True)]]
    )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 150 stars for 200 starts when you complete the payment.",
        payload="topup_200",
        provider_token="",
        prices=prices,
        currency ="XTR",
        reply_markup=pay_kb
    )
    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 
#250 stars 333
@start_router.callback_query(F.data == "star250")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(label="250 ⭐", amount=333)]
    
    pay_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pay 333 ⭐", pay=True)]]
    )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 250 stars for 333 starts when you complete the payment.",
        payload="topup_333",
        provider_token="",
        prices=prices,
        currency ="XTR",
        reply_markup=pay_kb
    )
    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 
# 750 stars
@start_router.callback_query(F.data == "star750")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(label="750 ⭐", amount=1000)]
    pay_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pay 1000 ⭐", pay=True)]]
    )

    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 750 stars for 1000 stars when you complete the payment.",
        payload="topup_1000",
        provider_token="",
        prices=prices,
        currency="XTR",
        reply_markup=pay_kb
    )

    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 

# 1000 stars
@start_router.callback_query(F.data == "star1000")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(label="1000 ⭐", amount=1333)]
    pay_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pay 1333 ⭐", pay=True)]]
    )

    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 1000 stars for 1333 stars when you complete the payment.",
        payload="topup_1333",
        provider_token="",
        prices=prices,
        currency="XTR",
        reply_markup=pay_kb
    )

    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None)
#1500 stars


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

# Game section
@game_router.message(F.text == "Roll 🎲")
async def play_game(message: types.Message):
    await message.answer("Choose a game to play:", reply_markup=start.game_kb)

@game_router.message(F.text == "Dice 🎲")
async def play_dice(message: types.Message, state: FSMContext):
    # Show responsible gambling reminder
    await show_gambling_reminder(message)

    await message.answer("🎲 You chose to play Dice! What amount are you willing to bet?")
    await state.set_state(BetStates.waiting_for_bet)


@game_router.message(BetStates.waiting_for_bet)
async def process_bet(message: types.Message, state: FSMContext):
    bet_amount = message.text

    if not bet_amount.isdigit():
        await message.answer("❌ Please enter a valid number for your bet.")
        return

    await state.update_data(bet=int(bet_amount))
    
    await message.answer(f"You have placed a bet of {bet_amount} ⭐. Good luck!")
    print(bet_amount, 'Bet amount received')
    
    
    
    
    # api call to backend with bet amount and user id
    # data = {
    #     "user_id": message.from_user.id,
    #     "bet": bet_amount
    # }
    # data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
    
    # signature = hmac.new(
    #     SYSTE_SECRET.encode(),
    #     data_str.encode(),
    #     hashlib.sha256
    # )
    
        # headers ={
    #     "Content-Type": "application/json",
    #     "X-Signature": signature.hexdigest()
    # }

    # response = requests.post(API_URL, headers=headers, json=data)
    # print(response.status_code, response.text)
    
    # check if bet amount is a number and greater than 10
    # try:
    #     if int(bet_amount) < 10:
    #         await message.answer("❌ Minimum bet is 10 stars. Please enter a valid bet amount.")
    #         return
    # except ValueError:
    #     await message.answer("❌ Please enter a valid number for your bet.")
    #     return

@game_router.message(F.text == "Target 🎯")
async def play_target(callback: types.CallbackQuery):
    await callback.answer("In development...")

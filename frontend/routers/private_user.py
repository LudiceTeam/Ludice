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

load_dotenv(find_dotenv())
secret_token = os.getenv("secret_token")

# State group
class Form(StatesGroup):
    waiting_for_bet = State()

API_URL = "http://127.0.0.1:8000/register"

start_router = Router()
payment_router = Router()
game_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    
    # terms_and_conditions = InlineKeyboardMarkup(
    #     inline_keyboard=[[InlineKeyboardButton(text="Agree ✅", pay=True)]]
    # )
    
    
    await message.answer("Welcome to the ludicé bot. Choose an option:", reply_markup=start.start_kb)
    # user_username = message.from_user.username
    # user_id = message.from_user.id
    # data = {
    #     "username": user_username,
    #     "id": user_id
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
    prices = [LabeledPrice(lebel="750 ⭐",amount=1000)] 
    pay_kb = InlineKeyboardMarkup(
        InlineKeyboardButton(text="Pay 1000 ⭐")
        )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        discription="Your account will be credited with 750 stars for 1000 starts when you complete the payment.",
        playload="topup_1000",
        provider_token="",
        prices=prices,
        currency ="XTR",
        reply_markup=pay_kb
    )
 
    await callback.answer()
    await callback.message.delete()
    await callback.message.edit_reply_markup(reply_markup=None) 

# 1000 stars 
@start_router.callback_query(F.data == "star1000")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(lebel="1000 ⭐",amount=1333)] 
    pay_kb = InlineKeyboardMarkup(
        InlineKeyboardButton(text="Pay 1333 ⭐")
        )
    
    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        discription="Your account will be credited with 1000 stars for 1333 starts when you complete the payment.",
        playload="topup_1333",
        provider_token="",
        prices=prices,
        currency ="XTR",
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
    await message.answer("🎲 You chose to play Dice! What amount are you willing to bet?")
    await state.set_state(Form.waiting_for_bet)


@game_router.message(Form.waiting_for_bet)
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

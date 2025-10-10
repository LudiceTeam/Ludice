from aiogram import F,Router, types
from aiogram.types import LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from keyboard import start
from dotenv import load_dotenv, find_dotenv
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram_dialog import (
    Dialog,
    DialogManager,
    Window,
)
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Next
from aiogram_dialog.widgets.text import Const, Jinja
import os
import requests
import json
import hashlib
import hmac

load_dotenv(find_dotenv())
secret_token = os.getenv("secret_token")

class SG(StatesGroup):
    bet = State()

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

@game_router.message(F.text == "Roll Dice 🎲")
async def play_dice(message: types.Message):
    await message.answer("You chose to play Dice 🎲! What amount are you willing to bet?")

@game_router.message(F.text == int)
async def process_bet(message: types.Message):
    bet_amount = int(message.text)
    await message.answer(f"You are betting {bet_amount} 🎲!, if you win, you will receive {bet_amount * 2} 🎲. To reset bey /start!")

# @game_router.message(SG.bet == None or SG.bet == "" or SG.bet.isdigit() == False or SG.bet == "0" or SG.bet.startswith("0"), SG.bet == str)
# async def error(
#         message: Message,
#         dialog_: Any,
#         manager: DialogManager,
#         error_: ValueError
# ):
#     await message.answer("Bet must be a number!")



# async def getter(dialog_manager: DialogManager, **kwargs):
#     return {
#         "bet": dialog_manager.find("bet").get_value(),
#         "country": dialog_manager.find("country").get_value(),
#     }

    

@game_router.message(F.text == "Target 🎯")
async def play_target(callback: types.CallbackQuery):
    await callback.answer("In development...")

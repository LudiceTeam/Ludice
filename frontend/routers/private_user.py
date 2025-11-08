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
import aiohttp
import json
import hashlib
import hmac
import time





# Legal text import
from common.legal_text import TERMS_FULL

# Gamling reminder function
GAMBLING_REMINDER = """
⚠️ **Responsible Gaming Reminder**

• Only bet what you can afford to lose

• Set limits and stick to them
• Take breaks regularly
"""

async def show_gambling_reminder(message):
    """Show responsible gambling reminder before playing."""
    await message.answer(GAMBLING_REMINDER, parse_mode="Markdown")


secrets_path = "/Users/vikrorkhanin/Ludice/data/secrets.json"
load_dotenv(find_dotenv())
secret_token = os.getenv("secret_token")
def get_key_for_api() -> str:
    try:
        with open(secrets_path,"r") as file:
            data = json.load(file)
        return data["key"]  
    except Exception as e:
        print(f"Error while geting api key : {e}")
        raise TypeError("Error")
# System secret for API signature verification
SYSTEM_SECRET = get_key_for_api()
BACKEND_API_URL = "http://127.0.0.1:8000"

# State groups
class BetStates(StatesGroup):
    waiting_for_bet = State()
    waiting_for_opponent = State()
    game_active = State()
    rolling_dice = State()

class LegalStates(StatesGroup):
    """FSM states for terms acceptance flow."""
    waiting_for_acceptance = State()
    verification = State()


API_URL = BACKEND_API_URL + "/register"

# Routers
start_router = Router()
payment_router = Router()
game_router = Router()
legal_router = Router()

# Helper functions
def generate_signature(data: dict) -> str:
    """Generate HMAC-SHA256 signature for API requests."""
    # Create a copy without signature field
    data_to_sign = data.copy()
    data_to_sign.pop("signature", None)

    # Serialize with sorted keys and no spaces
    data_str = json.dumps(data_to_sign, sort_keys=True, separators=(',', ':'))

    # Generate HMAC signature
    signature = hmac.new(
        SYSTEM_SECRET.encode(),
        data_str.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature


def get_legal_nav_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for terms acceptance."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ I Accept", callback_data="accept_terms"),
            InlineKeyboardButton(text="📖 Read Full Terms", callback_data="view_full_terms")
        ],
        [
            InlineKeyboardButton(text="❌ I Decline", callback_data="decline_terms")
        ]
    ])


def get_waiting_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for waiting for opponent."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Cancel Search", callback_data="cancel_search")]
    ])


def get_dice_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for rolling dice."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Roll Dice", callback_data="roll_dice")]
    ])


def get_play_again_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for playing again."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Play Again", callback_data="play_again")],
        [InlineKeyboardButton(text="🏠 Main Menu", callback_data="main_menu")]
    ])


@start_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    # Prepare API request data with signature
    data = {
        "timestamp": time.time()
    }
    
    # Generate signature
    data["signature"] = generate_signature(data)
    
    
    
    
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
@start_router.message(F.text == "Balance test")
async def balance_test(message: types.Message):
    """Test handler to increase user balance by 100 stars."""
    user_id = str(message.from_user.id)
    test_amount = 100  # Test credit amount

    # Prepare API request data with signature
    data = {
        "username": user_id,
        "amount": test_amount,
        "timestamp": time.time()
    }

    # Generate signature
    data["signature"] = generate_signature(data)

    try:
        async with aiohttp.ClientSession() as session:
            # Increase balance using the Python backend endpoint
            async with session.post(
                f"{BACKEND_API_URL}/user/increase",
                json=data,
                headers={"Content-Type": "application/json"}
            ) as increase_response:
                if increase_response.status == 200:
                    await message.answer(
                        f"✅ Balance test successful!\n\n"
                        f"Added: {test_amount} ⭐ to your account"
                    )
                elif increase_response.status == 404:
                    await message.answer(
                        "❌ User not found. Please start a game first to create your account."
                    )
                elif increase_response.status == 403:
                    await message.answer("❌ Authentication failed. Invalid signature.")
                elif increase_response.status == 429:
                    await message.answer("❌ Too many requests. Please wait a moment.")
                else:
                    error_text = await increase_response.text()
                    await message.answer(f"❌ Error: {error_text}")

    except aiohttp.ClientError as e:
        await message.answer(f"❌ Network error: {str(e)}")
    except Exception as e:
        await message.answer(f"❌ Unexpected error: {str(e)}")

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
    """Process user's bet and join/create game lobby."""
    bet_amount = message.text

    # Validate bet is a number
    if not bet_amount.isdigit():
        await message.answer("❌ Please enter a valid number for your bet.")
        return

    bet = int(bet_amount)

    # Validate minimum bet
    if bet < 10:
        await message.answer("❌ Minimum bet is 10 stars. Please enter a valid bet amount.")
        return

    # Store bet in state
    await state.update_data(bet=bet)

    # Prepare API request data
    data = {
        "username": str(message.from_user.id),
        "bet": bet,
        "timestamp": time.time()
    }

    # Generate signature
    data["signature"] = generate_signature(data)

    try:
        # Make API call to start game
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BACKEND_API_URL}/start/game",
                json=data,
                headers={"Content-Type": "application/json"}
            ) as response:

                if response.status == 200:
                    # Player joined existing lobby - game started
                    game_id = await response.text()
                    game_id = game_id.strip('"')  # Remove quotes from JSON string

                    await state.update_data(game_id=game_id, lobby_status="game_started")
                    await state.set_state(BetStates.game_active)

                    await message.answer(
                        f"🎮 Opponent found!\n"
                        f"Bet: {bet} ⭐\n\n"
                        f"Roll your dice!",
                        reply_markup=get_dice_keyboard()
                    )

                elif response.status == 400:
                    # Player created new lobby - waiting for opponent
                    response_data = await response.json()
                    game_id = response_data.get("detail", "")

                    await state.update_data(game_id=game_id, lobby_status="waiting")
                    await state.set_state(BetStates.waiting_for_opponent)

                    await message.answer(
                        f"🔍 Searching for opponent...\n"
                        f"Bet: {bet} ⭐\n\n"
                        f"Please wait while we find you a match.",
                        reply_markup=get_waiting_keyboard()
                    )

                    # Start polling for opponent
                    asyncio.create_task(poll_for_opponent(message, state, game_id))

                elif response.status == 403:
                    await message.answer("❌ Authentication failed. Please try again.")
                    await state.clear()

                elif response.status == 429:
                    await message.answer("❌ Too many requests. Please wait a moment and try again.")
                    await state.clear()

                else:
                    error_text = await response.text()
                    await message.answer(f"❌ Error: {error_text}")
                    await state.clear()

    except aiohttp.ClientError as e:
        await message.answer(
            f"❌ Network error. Please check your connection and try again.\n"
            f"Error: {str(e)}"
        )
        await state.clear()

    except Exception as e:
        await message.answer(f"❌ An unexpected error occurred: {str(e)}")
        await state.clear()


async def poll_for_opponent(message: types.Message, state: FSMContext, game_id: str):
    """Poll backend to check if opponent has joined the lobby."""
    bot = message.bot
    max_wait_time = 300  # 5 minutes
    poll_interval = 2  # 2 seconds

    for _ in range(max_wait_time // poll_interval):
        await asyncio.sleep(poll_interval)

        # Check if user cancelled search
        current_state = await state.get_state()
        if current_state != BetStates.waiting_for_opponent:
            return

        try:
            user_data = await state.get_data()

        except Exception as e:
            print(f"Polling error: {e}")
            continue

    # Timeout - cancel search
    current_state = await state.get_state()
    if current_state == BetStates.waiting_for_opponent:
        await bot.send_message(
            message.chat.id,
            "⏰ Search timeout. No opponent found.\n"
            "Please try again.",
            reply_markup=start.start_kb
        )
        await state.clear()


@game_router.callback_query(F.data == "cancel_search", BetStates.waiting_for_opponent)
async def cancel_search(callback: types.CallbackQuery, state: FSMContext):
    """Handle canceling opponent search."""
    user_data = await state.get_data()
    game_id = user_data.get("game_id")

    if game_id:
        # Call backend to cancel the lobby
        data = {
            "username": str(callback.from_user.id),
            "id": game_id,
            "timestamp": time.time()
        }
        data["signature"] = generate_signature(data)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{BACKEND_API_URL}/cancel/find",
                    json=data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        await callback.message.edit_text(
                            "❌ Search cancelled.",
                            reply_markup=None
                        )
                        await callback.message.answer(
                            "Welcome back to Ludicé!",
                            reply_markup=start.start_kb
                        )
                    else:
                        await callback.message.edit_text(
                            "⚠️ Could not cancel search. The game may have already started.",
                            reply_markup=None
                        )
        except Exception as e:
            await callback.message.edit_text(
                f"❌ Error canceling search: {str(e)}",
                reply_markup=None
            )

    await state.clear()
    await callback.answer()


@game_router.callback_query(F.data == "roll_dice", BetStates.game_active)
async def roll_dice(callback: types.CallbackQuery, state: FSMContext):
    """Handle dice roll action."""
    # Send dice using Telegram's built-in dice
    await callback.message.edit_text("🎲 Rolling...", reply_markup=None)

    dice_msg = await callback.message.answer_dice(emoji="🎲")

    # Wait for dice animation
    await asyncio.sleep(3)

    dice_value = dice_msg.dice.value
    user_data = await state.get_data()
    game_id = user_data.get("game_id")

    # Submit result to backend
    data = {
        "user_id": str(callback.from_user.id),
        "game_id": game_id,
        "result": dice_value,
        "timestamp": time.time()
    }
    data["signature"] = generate_signature(data)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BACKEND_API_URL}/write/res",
                json=data,
                headers={"Content-Type": "application/json"}
            ) as response:

                if response.status == 200:
                    await callback.message.answer(
                        f"Your roll: {dice_value}\n\n"
                        f"⏳ Waiting for opponent's roll..."
                    )

                    # Start polling for game result
                    asyncio.create_task(poll_for_game_result(callback.message, state, game_id, dice_value))

                else:
                    error_text = await response.text()
                    await callback.message.answer(f"❌ Error submitting result: {error_text}")

    except Exception as e:
        await callback.message.answer(f"❌ Error: {str(e)}")

    await callback.answer()


async def poll_for_game_result(message: types.Message, state: FSMContext, game_id: str, user_roll: int):
    """Poll backend to check if both players have rolled and determine winner."""
    bot = message.bot
    max_wait = 60  # 1 minute
    poll_interval = 2

    for _ in range(max_wait // poll_interval):
        await asyncio.sleep(poll_interval)

        try:
            # Check game data to see if both players have submitted results
            # This would require reading the game state from backend
            # For a complete implementation, you'd need a /get/game/{game_id} endpoint

            # For now, we'll use a placeholder
            # In production, fetch game data and check if both results are in

            # Placeholder: assume game completes and we need to determine winner
            # You'd call an endpoint like /get/game/result/{game_id}

            continue

        except Exception as e:
            print(f"Polling error: {e}")
            continue

    # Timeout
    await bot.send_message(
        message.chat.id,
        "⏰ Game timeout. Opponent did not roll in time.",
        reply_markup=start.start_kb
    )
    await state.clear()


@game_router.callback_query(F.data == "play_again")
async def play_again(callback: types.CallbackQuery, state: FSMContext):
    """Handle play again action."""
    await state.clear()
    await callback.message.edit_text("Choose a game to play:", reply_markup=start.game_kb)
    await callback.answer()


@game_router.callback_query(F.data == "main_menu")
async def main_menu(callback: types.CallbackQuery, state: FSMContext):
    """Return to main menu."""
    await state.clear()
    await callback.message.edit_text(
        "Welcome to Ludicé! Choose an option:",
        reply_markup=start.start_kb
    )
    await callback.answer()


@game_router.message(F.text == "Target 🎯")
async def play_target(callback: types.CallbackQuery):
    await callback.answer("In development...")

# Ludicé API Documentation

Complete API reference for the Ludicé backend services and bot integration.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Backend Game API](#backend-game-api)
4. [Balance Service API](#balance-service-api)
5. [Frontend Bot Integration](#frontend-bot-integration)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Examples](#examples)

---

## Overview

Ludicé consists of three API layers:

| Service | Port | Purpose | Protocol |
|---------|------|---------|----------|
| Game API | 8080 | Game logic, user management | HTTP + HMAC |
| Balance Service | 8000 | User balance management | HTTP (REST) |
| Bot | N/A | Telegram interface | aiogram 3.x |

---

## Authentication

### HMAC-SHA256 Signature

All requests to the Game API (port 8080) require HMAC-SHA256 authentication.

#### Request Signing Process

**Step 1: Prepare Data**
```python
data = {
    "username": "player123",
    "bet": 50
}
```

**Step 2: Create JSON String**
```python
import json

# CRITICAL: Sort keys and remove spaces
data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
# Result: '{"bet":50,"username":"player123"}'
```

**Step 3: Generate Signature**
```python
import hmac
import hashlib

SECRET_KEY = "your-secret-key"

signature = hmac.new(
    SECRET_KEY.encode(),
    data_str.encode(),
    hashlib.sha256
).hexdigest()
```

**Step 4: Send Request**
```python
import requests

headers = {
    "Content-Type": "application/json",
    "X-Signature": signature
}

response = requests.post(
    "http://localhost:8080/endpoint",
    headers=headers,
    json=data
)
```

#### Helper Function (Python)

```python
async def send_to_backend(url: str, data: dict) -> dict:
    """
    Send authenticated request to backend.

    Args:
        url: Full endpoint URL
        data: Request payload

    Returns:
        Response JSON or None on error
    """
    try:
        # Create signature
        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            SECRET_KEY.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Send request
        headers = {
            "Content-Type": "application/json",
            "X-Signature": signature
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Request failed: {e}")
        return None
```

---

## Backend Game API

Base URL: `http://localhost:8080`

### Endpoints

#### 1. User Registration

**Endpoint:** `POST /register`

**Description:** Register a new user or update existing user info.

**Request:**
```json
{
    "username": "player123",
    "id": 123456789
}
```

**Response (Success):**
```json
{
    "status": "success",
    "message": "User registered successfully"
}
```

**Response (Error):**
```json
{
    "status": "error",
    "message": "User already exists"
}
```

**Example:**
```python
data = {
    "username": "player123",
    "id": 123456789
}
response = await send_to_backend("http://localhost:8080/register", data)
```

---

#### 2. Start/Join Game

**Endpoint:** `POST /start/game`

**Description:** Start a new game or join existing lobby with matching bet.

**Request:**
```json
{
    "username": "player123",
    "bet": 50
}
```

**Response (Lobby Created):**
```json
{
    "status": "waiting",
    "message": "Searching for opponent...",
    "lobby_id": "abc123",
    "bet": 50
}
```

**Response (Game Started):**
```json
{
    "status": "game_started",
    "message": "Opponent found!",
    "game_id": "def456",
    "opponent": "player456",
    "bet": 50
}
```

**Response (Error - Insufficient Balance):**
```json
{
    "status": "error",
    "message": "Insufficient balance"
}
```

**Example:**
```python
data = {
    "username": "player123",
    "bet": 50
}
response = await send_to_backend("http://localhost:8080/start/game", data)
```

---

#### 3. Submit Game Result

**Endpoint:** `POST /write/res`

**Description:** Submit dice roll result for active game.

**Request:**
```json
{
    "username": "player123",
    "game_id": "def456",
    "result": 6
}
```

**Response (Waiting for Opponent):**
```json
{
    "status": "waiting",
    "message": "Waiting for opponent to roll..."
}
```

**Response (Game Complete - Win):**
```json
{
    "status": "win",
    "message": "You won!",
    "your_roll": 6,
    "opponent_roll": 3,
    "winnings": 100
}
```

**Response (Game Complete - Loss):**
```json
{
    "status": "loss",
    "message": "You lost.",
    "your_roll": 3,
    "opponent_roll": 6,
    "loss": 50
}
```

**Response (Game Complete - Tie):**
```json
{
    "status": "tie",
    "message": "It's a tie! Bet refunded.",
    "your_roll": 4,
    "opponent_roll": 4
}
```

**Example:**
```python
data = {
    "username": "player123",
    "game_id": "def456",
    "result": 6
}
response = await send_to_backend("http://localhost:8080/write/res", data)
```

---

#### 4. Leave Lobby

**Endpoint:** `POST /leave`

**Description:** Leave a game lobby before match starts.

**Request:**
```json
{
    "username": "player123"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Left lobby successfully"
}
```

**Example:**
```python
data = {
    "username": "player123"
}
response = await send_to_backend("http://localhost:8080/leave", data)
```

---

## Balance Service API

Base URL: `http://localhost:8000`

**No authentication required** (internal service only, should not be exposed publicly).

### Endpoints

#### 1. Create User

**Endpoint:** `POST /create_user`

**Description:** Create a new user with initial balance.

**Request:**
```json
{
    "username": "player123",
    "initial_balance": 1000
}
```

**Response (Success):**
```json
{
    "status": "success",
    "username": "player123",
    "balance": 1000
}
```

**Response (Error):**
```json
{
    "error": "User already exists"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/create_user \
  -H "Content-Type: application/json" \
  -d '{"username": "player123", "initial_balance": 1000}'
```

---

#### 2. Get Balance

**Endpoint:** `GET /get_balance`

**Description:** Query user's current balance.

**Query Parameters:**
- `username` (string, required): User's username

**Response (Success):**
```json
{
    "username": "player123",
    "balance": 750
}
```

**Response (Error):**
```json
{
    "error": "User not found"
}
```

**Example:**
```bash
curl http://localhost:8000/get_balance?username=player123
```

---

#### 3. Modify Balance

**Endpoint:** `POST /modify_balance`

**Description:** Add or subtract from user balance.

**Request:**
```json
{
    "username": "player123",
    "amount": 100,
    "operation": "add"
}
```

**Operations:**
- `"add"` - Add to balance
- `"subtract"` - Subtract from balance

**Response (Success):**
```json
{
    "status": "success",
    "username": "player123",
    "new_balance": 850
}
```

**Response (Error - Insufficient Funds):**
```json
{
    "error": "Insufficient balance"
}
```

**Example (Add):**
```bash
curl -X POST http://localhost:8000/modify_balance \
  -H "Content-Type: application/json" \
  -d '{"username": "player123", "amount": 100, "operation": "add"}'
```

**Example (Subtract):**
```bash
curl -X POST http://localhost:8000/modify_balance \
  -H "Content-Type: application/json" \
  -d '{"username": "player123", "amount": 50, "operation": "subtract"}'
```

---

## Frontend Bot Integration

### Telegram Bot Handlers

#### 1. Start Command

**Trigger:** `/start`

**Flow:**
```
User sends /start
    ↓
Show Terms of Service
    ↓
Set FSM State: LegalStates.waiting_for_acceptance
    ↓
User clicks "Accept"
    ↓
Call: POST /register
    ↓
Show main menu
```

**Code:**
```python
@start_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await state.set_state(LegalStates.waiting_for_acceptance)
    await message.answer(
        TERMS_FULL,
        parse_mode="Markdown",
        reply_markup=get_legal_nav_keyboard()
    )

@start_router.callback_query(F.data == "accept_terms")
async def accept_terms_handler(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    username = callback.from_user.username or f"user_{user_id}"

    # Register user
    data = {
        "username": username,
        "id": user_id
    }
    response = await send_to_backend(
        "http://localhost:8080/register",
        data
    )

    await state.clear()
    await callback.message.answer(
        "Welcome to Ludicé!",
        reply_markup=start.start_kb
    )
```

---

#### 2. Game Start

**Trigger:** User clicks "Roll 🎲" → "Dice 🎲"

**Flow:**
```
User clicks "Dice 🎲"
    ↓
Show gambling reminder
    ↓
Ask for bet amount
    ↓
Set FSM State: BetStates.waiting_for_bet
    ↓
User enters amount
    ↓
Validate (>= 10 stars)
    ↓
Call: POST /start/game
    ↓
Wait for opponent or start game
```

**Code:**
```python
@game_router.message(F.text == "Dice 🎲")
async def play_dice(message: types.Message, state: FSMContext):
    await show_gambling_reminder(message)
    await message.answer("What amount are you willing to bet?")
    await state.set_state(BetStates.waiting_for_bet)

@game_router.message(BetStates.waiting_for_bet)
async def process_bet(message: types.Message, state: FSMContext):
    bet_amount = message.text

    if not bet_amount.isdigit():
        await message.answer("❌ Please enter a valid number.")
        return

    bet = int(bet_amount)

    if bet < 10:
        await message.answer("❌ Minimum bet is 10 stars.")
        return

    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"

    # Start game
    data = {
        "username": username,
        "bet": bet
    }
    response = await send_to_backend(
        "http://localhost:8080/start/game",
        data
    )

    if response:
        await message.answer(
            f"✅ Bet placed: {bet} ⭐\nSearching for opponent..."
        )
    else:
        await message.answer("❌ Failed to place bet.")
        await state.clear()
```

---

#### 3. Payment Flow

**Trigger:** User clicks "Top up 🔝"

**Flow:**
```
User clicks "Top up 🔝"
    ↓
Show payment keyboard
    ↓
User selects amount (e.g., "100 ⭐")
    ↓
Send invoice (Telegram Stars)
    ↓
User pays
    ↓
pre_checkout_query → answer(ok=True)
    ↓
successful_payment → Update balance
```

**Code:**
```python
@start_router.callback_query(F.data == "star100")
async def send_invoice(callback: types.CallbackQuery):
    prices = [LabeledPrice(label="100 ⭐", amount=133)]

    pay_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pay 133 ⭐", pay=True)]]
    )

    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 100 stars.",
        payload="topup_133",
        provider_token="",
        prices=prices,
        currency="XTR",
        reply_markup=pay_kb
    )

@start_router.pre_checkout_query()
async def pre_checkout(pre_q: PreCheckoutQuery):
    await pre_q.answer(ok=True)

@start_router.message(F.successful_payment)
async def payment_success(msg: types.Message):
    sp = msg.successful_payment
    amount = int(sp.invoice_payload.replace("topup_", ""))

    # TODO: Update backend balance
    # await send_to_backend("http://localhost:8000/modify_balance", {...})

    await msg.answer("✅ Payment successful!")
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 400 | Bad Request | Invalid data format |
| 401 | Unauthorized | Invalid signature |
| 403 | Forbidden | Rate limit exceeded |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Retry later |

### Common Errors

#### 1. Invalid Signature

**Error:**
```json
{
    "detail": "Invalid signature"
}
```

**Cause:** HMAC signature doesn't match

**Solutions:**
- Check `SECRET_KEY` matches between frontend and backend
- Verify JSON serialization (sorted keys, no spaces)
- Check timestamp is within 5 minutes

---

#### 2. Rate Limit Exceeded

**Error:**
```json
{
    "detail": "Rate limit exceeded"
}
```

**Cause:** Too many requests

**Solutions:**
- Wait 1 second between user requests
- Implement client-side throttling
- Show user "Please wait..." message

---

#### 3. Insufficient Balance

**Error:**
```json
{
    "status": "error",
    "message": "Insufficient balance"
}
```

**Cause:** User doesn't have enough stars to bet

**Solutions:**
- Check balance before allowing bet
- Show "Top up" prompt
- Set maximum bet based on balance

---

## Rate Limiting

### Game API (Port 8080)

**IP-based:** 10 requests/minute (slowapi)

**User-based:** 1 request/second minimum

**Implementation:**
```python
# Backend
@limiter.limit("10/minute")
async def endpoint():
    if not check_time_seciruty(username):
        raise HTTPException(status_code=429, detail="Rate limit")
    ...
```

### Balance Service (Port 8000)

**No rate limiting** (internal service only)

**Should be behind firewall** and not publicly accessible.

---

## Examples

### Complete Game Flow Example

**1. Register User**

```python
# User accepts terms
data = {
    "username": "alice",
    "id": 123456
}
response = await send_to_backend(
    "http://localhost:8080/register",
    data
)
# Response: {"status": "success", ...}
```

**2. Start Game**

```python
# Alice bets 50 stars
data = {
    "username": "alice",
    "bet": 50
}
response = await send_to_backend(
    "http://localhost:8080/start/game",
    data
)
# Response: {"status": "waiting", "lobby_id": "xyz123", ...}
```

**3. Bob Joins**

```python
# Bob also bets 50 stars
data = {
    "username": "bob",
    "bet": 50
}
response = await send_to_backend(
    "http://localhost:8080/start/game",
    data
)
# Response: {"status": "game_started", "game_id": "abc456", "opponent": "alice", ...}
```

**4. Alice Rolls**

```python
# Alice rolls a 5
data = {
    "username": "alice",
    "game_id": "abc456",
    "result": 5
}
response = await send_to_backend(
    "http://localhost:8080/write/res",
    data
)
# Response: {"status": "waiting", ...}
```

**5. Bob Rolls**

```python
# Bob rolls a 3
data = {
    "username": "bob",
    "game_id": "abc456",
    "result": 3
}
response = await send_to_backend(
    "http://localhost:8080/write/res",
    data
)
# Response: {"status": "loss", "your_roll": 3, "opponent_roll": 5, ...}
```

**Result:** Alice wins 100 stars total (her 50 + Bob's 50)

---

### Payment Integration Example

**1. User Pays 133 Stars**

```python
# Telegram processes payment
# successful_payment event triggers

sp = msg.successful_payment
amount_paid = sp.total_amount  # 133 stars
amount_credited = 100  # After ~25% fee
```

**2. Credit User Balance**

```python
# Update in Balance Service
data = {
    "username": "alice",
    "amount": amount_credited,
    "operation": "add"
}

response = requests.post(
    "http://localhost:8000/modify_balance",
    json=data
)
# Response: {"status": "success", "new_balance": 1100}
```

**3. Record Transaction**

```python
# Save to payments.json
transaction = {
    "id": "txn_123",
    "user": "alice",
    "amount_paid": 133,
    "amount_credited": 100,
    "timestamp": datetime.now().isoformat(),
    "payment_provider": "telegram_stars"
}
# Append to payments.json
```

---

## Testing

### Test Signature Generation

```python
import hmac
import hashlib
import json

SECRET_KEY = "test-secret-key"

data = {"username": "test", "bet": 10}
data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
signature = hmac.new(
    SECRET_KEY.encode(),
    data_str.encode(),
    hashlib.sha256
).hexdigest()

print(f"Data: {data_str}")
print(f"Signature: {signature}")
```

### Test API Endpoints

```bash
# Register user (with correct signature)
python scripts/test_api.py register alice 123456

# Start game
python scripts/test_api.py start_game alice 50

# Check balance
curl http://localhost:8000/get_balance?username=alice
```

---

**Last Updated:** January 2025

# Ludicé Development Guide

Guide for developers contributing to or extending the Ludicé Telegram bot.

## Table of Contents

1. [Development Environment](#development-environment)
2. [Code Structure](#code-structure)
3. [Adding Features](#adding-features)
4. [Testing](#testing)
5. [Code Style](#code-style)
6. [Git Workflow](#git-workflow)
7. [Common Development Tasks](#common-development-tasks)

---

## Development Environment

### Required Tools

- **Python 3.9+**
- **Go 1.19+**
- **Redis**
- **Git**
- **Code Editor** (VS Code, PyCharm, etc.)

### Recommended VS Code Extensions

- Python
- Go
- Pylance
- GitLens
- Better Comments
- Markdown All in One

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/Wizer27/Ludice.git
cd Ludice

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
cd frontend && pip install -r requirements.txt && cd ..

# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

---

## Code Structure

### Frontend (Telegram Bot)

```
frontend/
├── app.py                      # Main entry point
│   - Bot initialization
│   - Dispatcher setup
│   - Router registration
│
├── routers/
│   └── private_user.py         # Main user handlers
│       - /start command
│       - Terms acceptance flow
│       - Payment handlers
│       - Game handlers
│       - Backend API integration
│
├── keyboard/
│   └── start.py                # UI components
│       - Main menu keyboard
│       - Payment keyboard
│       - Game selection keyboard
│
├── common/
│   ├── legal_text.py           # Legal text constants
│   └── bot_cmds_list.py        # Bot commands
│
└── auth/
    └── auth.py                 # JWT utilities (legacy)
```

### Backend (Game API)

```
backend/
├── new.py                      # Main FastAPI application
│   - Signature verification
│   - Rate limiting
│   - Game logic
│   - User management
│   - JSON file operations
│
├── financne.py                 # Payment API
│   - TON payment integration
│
├── redis/
│   └── main.go                 # Balance service (Go)
│       - User creation
│       - Balance queries
│       - Balance modifications
│
└── secrets.json                # Shared secret key
```

---

## Adding Features

### Add a New Bot Command

**Example: Add a `/stats` command to show user statistics**

**Step 1: Add Handler**

Edit `frontend/routers/private_user.py`:

```python
@start_router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"

    # Call backend to get stats
    data = {"username": username}
    response = await send_to_backend(
        "http://localhost:8080/get_stats",
        data
    )

    if response:
        wins = response.get("wins", 0)
        total = response.get("total_games", 0)
        win_rate = (wins / total * 100) if total > 0 else 0

        await message.answer(
            f"📊 Your Statistics:\n\n"
            f"Total Games: {total}\n"
            f"Wins: {wins}\n"
            f"Win Rate: {win_rate:.1f}%"
        )
    else:
        await message.answer("❌ Failed to load statistics.")
```

**Step 2: Add Backend Endpoint**

Edit `backend/new.py`:

```python
@app.post("/get_stats")
async def get_stats(request: StatsRequest):
    # Verify signature
    if not verify_signature(request.dict(), request.signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Load stats from JSON
    with open("data/stats.json", "r") as f:
        stats = json.load(f)

    user_stats = stats.get(request.username, {"wins": 0, "total_games": 0})

    return user_stats
```

**Step 3: Update BotFather**

Message @BotFather:

```
/setcommands

start - Start the bot
stats - View your statistics
help - Get help
```

---

### Add a New Payment Tier

**Example: Add 500 stars option**

Edit `frontend/keyboard/start.py`:

```python
keyboard_stars = InlineKeyboardMarkup(
    inline_keyboard=[
        # ... existing options ...
        [
            InlineKeyboardButton(text="500 ⭐", callback_data="star500"),
        ],
        # ... rest of options ...
    ]
)
```

Edit `frontend/routers/private_user.py`:

```python
@start_router.callback_query(F.data == "star500")
async def send_invoice_500(callback: types.CallbackQuery):
    # 500 stars for 667 stars (25% fee)
    prices = [LabeledPrice(label="500 ⭐", amount=667)]

    pay_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pay 667 ⭐", pay=True)]]
    )

    await callback.message.answer_invoice(
        title="❖ Telegram Stars",
        description="Your account will be credited with 500 stars for 667 stars.",
        payload="topup_667",
        provider_token="",
        prices=prices,
        currency="XTR",
        reply_markup=pay_kb
    )

    await callback.answer()
    await callback.message.delete()
```

---

### Add a New Game Mode

**Example: Add a "Target Number" game**

**Step 1: Create FSM State**

Edit `frontend/routers/private_user.py`:

```python
class TargetStates(StatesGroup):
    waiting_for_bet = State()
    waiting_for_target = State()
```

**Step 2: Add Game Handler**

```python
@game_router.message(F.text == "Target 🎯")
async def play_target(message: types.Message, state: FSMContext):
    await show_gambling_reminder(message)
    await message.answer("🎯 Target Number Game!\n\nEnter your bet amount:")
    await state.set_state(TargetStates.waiting_for_bet)

@game_router.message(TargetStates.waiting_for_bet)
async def target_bet(message: types.Message, state: FSMContext):
    bet = int(message.text)

    if bet < 10:
        await message.answer("❌ Minimum bet is 10 stars.")
        return

    await state.update_data(bet=bet)
    await message.answer("Choose a target number (1-6):")
    await state.set_state(TargetStates.waiting_for_target)

@game_router.message(TargetStates.waiting_for_target)
async def target_number(message: types.Message, state: FSMContext):
    target = int(message.text)

    if target < 1 or target > 6:
        await message.answer("❌ Target must be between 1 and 6.")
        return

    # Get bet from state
    data = await state.get_data()
    bet = data["bet"]

    # Call backend to start target game
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"

    game_data = {
        "username": username,
        "bet": bet,
        "target": target,
        "game_type": "target"
    }

    response = await send_to_backend(
        "http://localhost:8080/start/target_game",
        game_data
    )

    if response:
        await message.answer(
            f"🎲 Rolling...\n\n"
            f"Target: {target}\n"
            f"Result: {response['roll']}\n\n"
            f"{response['message']}"
        )
    else:
        await message.answer("❌ Failed to start game.")

    await state.clear()
```

**Step 3: Add Backend Endpoint**

Edit `backend/new.py`:

```python
@app.post("/start/target_game")
async def start_target_game(request: TargetGameRequest):
    if not verify_signature(request.dict(), request.signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Roll dice
    roll = random.randint(1, 6)

    # Check if user hit target
    if roll == request.target:
        # Win: 5x bet
        winnings = request.bet * 5
        # Update balance...
        return {
            "status": "win",
            "roll": roll,
            "message": f"🎉 You won {winnings} stars!",
            "winnings": winnings
        }
    else:
        # Loss
        return {
            "status": "loss",
            "roll": roll,
            "message": f"💔 You lost {request.bet} stars.",
            "loss": request.bet
        }
```

---

## Testing

### Unit Tests (Python)

Create `tests/test_signature.py`:

```python
import pytest
import hmac
import hashlib
import json

def create_signature(data, secret_key):
    data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hmac.new(
        secret_key.encode(),
        data_str.encode(),
        hashlib.sha256
    ).hexdigest()

def test_signature_generation():
    data = {"username": "test", "bet": 10}
    secret = "test-key"

    sig1 = create_signature(data, secret)
    sig2 = create_signature(data, secret)

    assert sig1 == sig2

def test_signature_order_independence():
    data1 = {"bet": 10, "username": "test"}
    data2 = {"username": "test", "bet": 10}
    secret = "test-key"

    sig1 = create_signature(data1, secret)
    sig2 = create_signature(data2, secret)

    assert sig1 == sig2  # Order shouldn't matter
```

Run tests:

```bash
pytest tests/
```

### Integration Tests

Create `tests/test_api.py`:

```python
import requests
import pytest

BASE_URL = "http://localhost:8080"

def test_register_user():
    # Assumes backend is running
    data = {
        "username": "testuser",
        "id": 999999
    }

    # Create signature...
    signature = create_signature(data, SECRET_KEY)

    response = requests.post(
        f"{BASE_URL}/register",
        json=data,
        headers={"X-Signature": signature}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

### Manual Testing

Create `scripts/test_bot.py`:

```python
#!/usr/bin/env python3
"""Manual bot testing script"""

import asyncio
from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def test_bot():
    bot = Bot(TOKEN)

    # Test 1: Get bot info
    me = await bot.get_me()
    print(f"✅ Bot: @{me.username}")

    # Test 2: Get updates
    updates = await bot.get_updates()
    print(f"✅ Updates: {len(updates)}")

    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test_bot())
```

---

## Code Style

### Python (PEP 8)

**Use Black formatter:**

```bash
pip install black
black frontend/ backend/
```

**Linting with flake8:**

```bash
pip install flake8
flake8 frontend/ backend/
```

**Example good code:**

```python
async def process_bet(message: types.Message, state: FSMContext):
    """
    Process user's bet amount.

    Args:
        message: Incoming message with bet amount
        state: FSM context

    Returns:
        None
    """
    bet_amount = message.text

    # Validate input
    if not bet_amount.isdigit():
        await message.answer("❌ Please enter a valid number.")
        return

    bet = int(bet_amount)

    # Check minimum
    if bet < 10:
        await message.answer("❌ Minimum bet is 10 stars.")
        return

    # Process bet
    await state.update_data(bet=bet)
    ...
```

### Go (gofmt)

```bash
cd backend/redis
go fmt ./...
goimports -w .
```

### Comments

```python
# ✅ Good: Explain WHY
# We use sorted JSON to ensure signature consistency across requests
data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))

# ❌ Bad: Explain WHAT (code is self-explanatory)
# Create JSON string
data_str = json.dumps(data)
```

---

## Git Workflow

### Branch Strategy

- `main` - Production-ready code
- `dev` - Active development
- `feature/*` - New features
- `bugfix/*` - Bug fixes

### Creating a Feature

```bash
# Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/add-stats-command

# Make changes...
git add .
git commit -m "feat: add /stats command for user statistics"

# Push to remote
git push origin feature/add-stats-command
```

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: add new feature
fix: bug fix
docs: documentation changes
style: code style changes
refactor: code refactoring
test: add tests
chore: build/config changes
```

**Examples:**

```bash
git commit -m "feat: add target number game mode"
git commit -m "fix: resolve signature verification issue"
git commit -m "docs: update API documentation for new endpoints"
git commit -m "refactor: extract signature logic to helper function"
```

### Pull Request Process

1. **Create PR** from feature branch to `dev`
2. **Write description** explaining changes
3. **Link issues** if applicable
4. **Request review**
5. **Address feedback**
6. **Merge** when approved

---

## Common Development Tasks

### Add New Backend Endpoint

```python
# 1. Define request model
class MyRequest(BaseModel):
    username: str
    data: dict
    signature: str

# 2. Create endpoint
@app.post("/my_endpoint")
async def my_endpoint(request: MyRequest):
    # Verify signature
    if not verify_signature(request.dict(), request.signature):
        raise HTTPException(status_code=401)

    # Rate limiting
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429)

    # Process request
    result = process_data(request.data)

    return {"status": "success", "result": result}
```

### Add FSM State Flow

```python
# 1. Define states
class MyStates(StatesGroup):
    step1 = State()
    step2 = State()

# 2. Start flow
@router.message(F.text == "Start Flow")
async def start_flow(message: types.Message, state: FSMContext):
    await message.answer("Step 1: Enter name")
    await state.set_state(MyStates.step1)

# 3. Handle step 1
@router.message(MyStates.step1)
async def handle_step1(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)

    await message.answer("Step 2: Enter age")
    await state.set_state(MyStates.step2)

# 4. Handle step 2
@router.message(MyStates.step2)
async def handle_step2(message: types.Message, state: FSMContext):
    age = message.text
    data = await state.get_data()

    await message.answer(f"Name: {data['name']}, Age: {age}")
    await state.clear()
```

### Debug HMAC Signatures

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

def send_to_backend(url, data):
    data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
    print(f"DEBUG: Data string: {data_str}")

    signature = hmac.new(
        SECRET_KEY.encode(),
        data_str.encode(),
        hashlib.sha256
    ).hexdigest()
    print(f"DEBUG: Signature: {signature}")

    # ... rest of function
```

### Add Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use in code
logger.info(f"User {username} registered successfully")
logger.warning(f"Failed bet attempt: {bet_amount}")
logger.error(f"Backend connection failed: {e}")
```

---

## Resources

- [aiogram Documentation](https://docs.aiogram.dev/en/latest/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**Last Updated:** January 2025

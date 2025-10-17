# Ludicé Technical Architecture

## Overview

Ludicé is a Telegram bot dice-rolling game built with a multi-language microservices architecture:
- **Frontend**: Python + aiogram 3.x (Telegram bot)
- **Backend API**: Python + FastAPI (game logic, user management, payments)
- **Balance Service**: Go + Gin + Redis (user balance management)

## System Architecture

```
┌─────────────────┐
│  Telegram User  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         Frontend (Python/aiogram)        │
│  ┌──────────────────────────────────┐   │
│  │  app.py (Main Entry Point)       │   │
│  │  ├── start_router                │   │
│  │  └── game_router                 │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │  routers/private_user.py         │   │
│  │  - Terms acceptance (FSM)        │   │
│  │  - Payment handling (Stars)      │   │
│  │  - Game interaction              │   │
│  │  - Backend API calls (HMAC)      │   │
│  └──────────────────────────────────┘   │
└───────────┬─────────────────────────────┘
            │
            │ HMAC-SHA256 Signed Requests
            ▼
┌─────────────────────────────────────────┐
│      Backend API (Python/FastAPI)       │
│         Port: 8080, 8000                │
│  ┌──────────────────────────────────┐   │
│  │  new.py - Main Game API          │   │
│  │  - Signature verification        │   │
│  │  - Rate limiting (slowapi)       │   │
│  │  - Game logic                    │   │
│  │  - JSON file persistence         │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │  financne.py - Payment API       │   │
│  │  - TON payment integration       │   │
│  └──────────────────────────────────┘   │
└───────────┬─────────────────────────────┘
            │
            │ HTTP Requests
            ▼
┌─────────────────────────────────────────┐
│   Balance Service (Go/Gin/Redis)        │
│            Port: 8000                   │
│  ┌──────────────────────────────────┐   │
│  │  redis/main.go                   │   │
│  │  - User creation                 │   │
│  │  - Balance queries               │   │
│  │  - Balance modifications         │   │
│  └──────────┬───────────────────────┘   │
│             │                            │
│             ▼                            │
│  ┌──────────────────────────────────┐   │
│  │  Redis (localhost:6379)          │   │
│  │  - User balances                 │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│       Data Layer (JSON Files)           │
│         Directory: data/                │
│  - bank.json (user balances)            │
│  - game.json (active games)             │
│  - users.json (user accounts)           │
│  - stats.json (player statistics)       │
│  - lobby.json (game lobbies)            │
│  - bets.json (betting records)          │
│  - payments.json (payment history)      │
│  - times_sec.json (rate limiting)       │
└─────────────────────────────────────────┘
```

## Frontend Architecture

### Directory Structure

```
frontend/
├── app.py                    # Main bot entry point
├── routers/
│   └── private_user.py       # User interaction handlers
├── keyboard/
│   └── start.py              # UI keyboard layouts
├── common/
│   ├── legal_text.py         # Legal text constants
│   └── bot_cmds_list.py      # Bot commands list
├── auth/
│   └── auth.py               # JWT token utilities
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables
```

### Key Components

#### 1. App Entry Point (`app.py`)
```python
# Initializes bot, dispatcher, and routers
bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(game_router)
```

#### 2. Private User Router (`routers/private_user.py`)

**FSM States:**
- `LegalStates.waiting_for_acceptance` - Terms acceptance flow
- `BetStates.waiting_for_bet` - Betting amount input

**Key Handlers:**
- `/start` - Shows terms of service
- `accept_terms` - Registers user to backend
- `Top up 🔝` - Payment flow
- `Dice 🎲` - Game initiation
- `process_bet` - Bet placement

**Backend Integration:**
```python
async def send_to_backend(url: str, data: dict) -> dict:
    # Creates HMAC-SHA256 signature
    # Sends POST with X-Signature header
    # Returns JSON response or None
```

#### 3. Keyboards (`keyboard/start.py`)

**Main Menu (`start_kb`):**
- Roll 🎲
- Help ❓
- Profile 👤
- Top up 🔝

**Payment Options (`keyboard_stars`):**
- 15-1,000,000 stars
- Inline keyboard with callback data

**Game Selection (`game_kb`):**
- Dice 🎲
- Target 🎯

### Payment Flow

```
User clicks "Top up 🔝"
    ↓
Show payment keyboard (15-1M stars)
    ↓
User selects amount (e.g., "star100")
    ↓
Bot sends invoice (Telegram Stars/XTR)
    ↓
User pays via Telegram
    ↓
pre_checkout_query → answer(ok=True)
    ↓
successful_payment → Confirm to user
    ↓
(TODO: Update backend balance)
```

### Game Flow

```
User clicks "Roll 🎲" → "Dice 🎲"
    ↓
Show gambling reminder
    ↓
Ask for bet amount
    ↓
Set FSM state: BetStates.waiting_for_bet
    ↓
User enters amount
    ↓
Validate: isdigit() and >= 10
    ↓
Send to backend: POST /start/game
    {
        "username": username,
        "bet": bet_amount
    }
    ↓
Backend matches players or creates lobby
    ↓
Game proceeds (handled by backend)
```

## Backend Architecture

### Main API (`backend/new.py`)

**Port:** 8080
**Framework:** FastAPI

**Key Features:**
- HMAC-SHA256 signature verification
- Rate limiting (slowapi + custom per-user checks)
- Thread-safe file operations (filelock)
- JSON file persistence

**Security:**
```python
# Every request must include signature
def verify_signature(data: dict, signature: str) -> bool:
    # Compute HMAC-SHA256 from sorted JSON
    # Compare with provided signature
    # Check timestamp (5min expiry)
```

**Rate Limiting:**
```python
@limiter.limit("10/minute")  # IP-based
def check_time_seciruty(username):  # User-based (1s minimum)
```

**API Endpoints:**
- `POST /register` - User registration
- `POST /start/game` - Start/join game
- `POST /write/res` - Submit game result
- `POST /leave` - Leave lobby

### Finance API (`backend/financne.py`)

**Port:** 8080 (configure different port if needed)
**Purpose:** TON payment integration

**Features:**
- Payment processing
- Transaction history
- TON Payment interface

### Balance Service (`backend/redis/main.go`)

**Port:** 8000
**Framework:** Gin
**Database:** Redis (localhost:6379)

**Endpoints:**
```go
POST /create_user     // Create user account
GET  /get_balance     // Query user balance
POST /modify_balance  // Add/subtract balance
```

**Redis Schema:**
```
Key: user:{username}
Value: balance (integer)
```

## Data Persistence

### JSON Files (`data/`)

All backend data stored as JSON files with thread-safe access:

**1. users.json**
```json
{
    "username": {
        "id": 12345,
        "password": "hashed_password"
    }
}
```

**2. bank.json**
```json
{
    "username": 1000
}
```

**3. game.json**
```json
{
    "game_id": {
        "players": ["user1", "user2"],
        "bet": 50,
        "status": "active"
    }
}
```

**4. lobby.json**
```json
{
    "username": {
        "bet": 50,
        "game_id": "unique_id"
    }
}
```

**5. stats.json**
```json
{
    "username": {
        "wins": 10,
        "total_games": 25
    }
}
```

**6. payments.json**
```json
{
    "transaction_id": {
        "user": "username",
        "amount": 100,
        "timestamp": "2025-01-15T10:30:00"
    }
}
```

**7. times_sec.json** (Rate limiting)
```json
{
    "username": 1673800000.0
}
```

## Security Architecture

### 1. HMAC Signature Verification

**Frontend (Python):**
```python
# Create signature
data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
signature = hmac.new(
    SECRET_KEY.encode(),
    data_str.encode(),
    hashlib.sha256
).hexdigest()

headers = {"X-Signature": signature}
```

**Backend (Python):**
```python
# Verify signature
def verify_signature(data: dict, signature: str) -> bool:
    expected = compute_signature(data)
    return hmac.compare_digest(expected, signature)
```

### 2. Rate Limiting

**Two-layer approach:**
1. **IP-based** (slowapi): 10 requests/minute
2. **User-based**: 1 request/second minimum

### 3. Environment Variables

**Required in `.env`:**
```bash
# Telegram bot token
TOKEN=your_bot_token_here

# HMAC secret key (shared with backend)
SECRET_KEY=your_shared_secret_key

# Telegram payment token (for Stars)
secret_token=your_payment_token
```

### 4. Secrets Management

**Backend secrets.json:**
```json
{
    "secret_key": "your_shared_secret_key",
    "api_keys": {}
}
```

## Communication Protocols

### Frontend → Backend API

**Authentication:** HMAC-SHA256 signature

**Request Format:**
```python
{
    "username": "user123",
    "bet": 50,
    "timestamp": 1673800000
}
```

**Headers:**
```
Content-Type: application/json
X-Signature: abc123def456...
```

**Response Format:**
```json
{
    "status": "success",
    "data": {...}
}
```

### Backend API → Redis Service

**Standard HTTP REST:**
```python
POST http://127.0.0.1:8000/create_user
{
    "username": "user123",
    "initial_balance": 0
}
```

## Scalability Considerations

### Current Limitations

1. **JSON file storage** - Not suitable for high traffic
2. **No database** - No ACID guarantees
3. **File locking** - Bottleneck for concurrent writes
4. **In-memory state** - No horizontal scaling

### Migration Path

**Phase 1: Database Migration**
```
JSON files → PostgreSQL/MySQL
- Atomic transactions
- Better concurrency
- Query optimization
```

**Phase 2: Caching**
```
Add Redis caching layer
- Reduce database load
- Faster reads
- Session management
```

**Phase 3: Microservices**
```
Split services:
- User Service
- Game Service
- Payment Service
- Notification Service
```

**Phase 4: Message Queue**
```
Add RabbitMQ/Kafka
- Async processing
- Event-driven architecture
- Better reliability
```

## Deployment Architecture

### Development
```
Local machine
- Frontend: python app.py
- Backend: python new.py
- Redis: localhost:6379
- Go service: go run main.go
```

### Production (Recommended)
```
Docker Compose:
├── frontend (aiogram bot)
├── backend (FastAPI)
├── redis-service (Go)
├── redis (database)
└── nginx (reverse proxy)
```

## Monitoring & Logging

### Current Logging

**Frontend:**
```python
print(f"✅ User {username} registered")
print(f"⚠️ Failed to place bet")
```

**Backend:**
```python
print(response.status_code, response.text)
```

### Recommended Improvements

1. **Structured logging** (Python `logging` module)
2. **Log aggregation** (ELK stack, Grafana Loki)
3. **Metrics** (Prometheus + Grafana)
4. **Error tracking** (Sentry)
5. **Health checks** (Kubernetes probes)

## Technology Stack Summary

| Component | Technology | Version |
|-----------|-----------|---------|
| Bot Framework | aiogram | 3.22.0 |
| Backend API | FastAPI | 0.119.0 |
| Balance Service | Go + Gin | - |
| Database | Redis | - |
| Data Storage | JSON files | - |
| Payment | Telegram Stars | XTR |
| Authentication | HMAC-SHA256 | - |
| HTTP Client | requests | 2.32.5 |
| Environment | python-dotenv | 1.1.1 |

## Performance Characteristics

### Expected Load
- **Users:** 1-1000 concurrent
- **Games:** 1-500 active games
- **Payments:** ~100/day

### Bottlenecks
1. JSON file I/O
2. File locking contention
3. Synchronous request handling
4. No caching layer

### Optimization Opportunities
1. Database migration
2. Async file I/O
3. Connection pooling
4. Response caching
5. Load balancing

---

**Last Updated:** January 2025

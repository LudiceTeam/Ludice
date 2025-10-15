# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ludicé is a Telegram bot dice-rolling game where users compete against each other. The project uses a multi-language architecture with Python for backend APIs and Telegram bot, and Go for Redis-based user balance management.

## Architecture

### Backend (Python/FastAPI)
- **Main API**: `backend/new.py` - Central FastAPI application handling game logic, user management, and payments
  - Runs on port 8080
  - Uses HMAC-SHA256 signature verification for request authentication
  - Rate limiting via `slowapi` with per-user time-based security checks
  - Thread-safe file operations with locks for concurrent access
  - JSON file-based persistence in `data/` directory

- **Finance API**: `backend/financne.py` - Separate FastAPI service for TON payment integration
  - Handles payment processing and transaction history
  - Implements TON Payment interface for cryptocurrency transactions

- **Redis Service** (Go): `backend/redis/main.go` - Balance management microservice using Gin framework
  - Runs on port 8000
  - Manages user balances in Redis (localhost:6379)
  - Provides endpoints for user creation, balance queries, and balance modifications

### Frontend (Python/Aiogram)
- **Bot Application**: `frontend/app.py` - Main entry point for the Telegram bot
  - Uses aiogram 3.x framework
  - Includes routers: `start_router`, `game_router`
  - Token loaded from `.env` file

- **Bot Routers**: `frontend/routers/private_user.py` - Handles user interactions
  - Payment flows using Telegram Stars (XTR currency)
  - Game selection and betting system with FSM (Finite State Machine)
  - Multiple payment tiers (15-1000 stars)

- **Keyboards**: `frontend/keyboard/start.py` - UI components for bot interactions

### Data Persistence
All data stored as JSON files in `data/`:
- `bank.json` - User balances
- `game.json` - Active game sessions
- `users.json` - User accounts
- `stats.json` - Player statistics (wins, total games)
- `lobby.json` - User lobby associations
- `bets.json` - Betting records
- `payments.json` - Payment transaction history
- `times_sec.json` - Rate limiting timestamps
- `data_second_game.json` - Second game mode data
- `drotic.json` - Drotic game mode data

## Development Setup

### Running the Backend API
```bash
cd backend
python new.py
# Starts FastAPI server on 0.0.0.0:8080
```

### Running the Finance API
```bash
cd backend
python financne.py
# Starts on 0.0.0.0:8080 (configure different port if needed)
```

### Running the Redis Balance Service (Go)
```bash
cd backend/redis
go run main.go
# Starts Gin server on :8000
# Requires Redis running on localhost:6379
```

### Running the Telegram Bot
```bash
cd frontend
python app.py
# Requires TOKEN in .env file
```

### Dependencies
Install Python dependencies:
```bash
pip install -r requirements.txt
```

Key dependencies:
- `fastapi` - Web framework for backend APIs
- `aiogram==3.22.0` - Telegram bot framework
- `slowapi` - Rate limiting
- `passlib` - Password hashing
- `jose`/`jwt` - JWT token handling
- `redis` - Redis client
- `filelock` - Thread-safe file operations

For Go service:
```bash
cd backend/redis
go mod download
```

### Environment Variables
Create `.env` files:
- `frontend/.env` - Contains `TOKEN` for Telegram bot
- Backend expects `secrets.json` for API keys and shared secret key

## Key Implementation Details

### Request Signature Verification
All backend API endpoints use HMAC-SHA256 signature verification:
- Requests include `signature` and `timestamp` fields
- Timestamps expire after 300 seconds (5 minutes)
- Signature computed from sorted JSON payload excluding the signature field itself
- Shared secret key loaded from `secrets.json`

### Rate Limiting
Two-layer approach:
1. `slowapi` for IP-based rate limiting
2. Custom per-user time checks in `check_time_seciruty()` function
   - Minimum 1 second between requests per user
   - Cleans stale entries (>1 hour old) automatically
   - Thread-safe with locking

### Game Flow
1. User starts game via `/start/game` endpoint with bet amount
2. System searches for existing lobby with matching bet or creates new one
3. When 2 players join, game becomes active
4. Each player submits dice result via `/write/res`
5. Winner determined and stats updated
6. Lobby cleaned up via `/leave` endpoint

### Multi-Game Support
The backend supports three game modes:
1. **Standard Dice Game** - Main game logic in `backend/new.py`
2. **Second Game** - Tracked in `data_second_game.json` with number guessing
3. **Drotic Game** - Alternative dice variant in `data/drotic.json`

## Testing

The project structure indicates tests may be in `test/` directory, but implementation details should be verified.

## Docker Support

Dockerfiles exist for:
- Root `Dockerfile` (project-level)
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml` (currently empty - needs configuration)

## Security Considerations

- All API endpoints validate HMAC signatures before processing
- Passwords stored in JSON (consider migrating to hashed storage)
- Secrets loaded from `secrets.json` (ensure this file is in `.gitignore`)
- `.env.example` provided as template for environment variables
- Rate limiting protects against abuse

## Branch Strategy

- `main` - Main production branch
- `dev` - Active development branch (use for PRs)

## Common Tasks

### Adding a New API Endpoint
1. Add endpoint handler in `backend/new.py`
2. Create Pydantic model for request validation
3. Include signature verification: `verify_signature(request.dict(), request.signature)`
4. Add rate limiting check: `check_time_seciruty(username)`
5. Implement thread-safe file operations if accessing JSON data

### Adding a New Bot Command
1. Define handler in `frontend/routers/private_user.py`
2. Use appropriate router (`start_router` or `game_router`)
3. Create keyboard layouts in `frontend/keyboard/start.py` if needed
4. Use FSM states for multi-step interactions

### Modifying Game Logic
1. Update endpoint handlers in `backend/new.py`
2. Modify JSON data structures in `data/` directory
3. Update stats tracking functions (`add_win`, `add_game`)
4. Ensure thread-safe access to shared data files

### Working with Redis Balance Service
The Go service provides REST endpoints for balance operations. When making changes:
1. Update handlers in `backend/redis/main.go`
2. Ensure Redis connection maintained via global `rdb` client
3. All balance operations check existence before modification
4. Return appropriate HTTP status codes for error handling

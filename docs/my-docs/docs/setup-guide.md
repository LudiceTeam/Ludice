# Ludicé Setup Guide

Complete guide to setting up and running the Ludicé Telegram bot locally and in production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Environment Setup](#environment-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Redis Service Setup](#redis-service-setup)
7. [Running the Application](#running-the-application)
8. [Telegram Bot Configuration](#telegram-bot-configuration)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)
11. [Production Deployment](#production-deployment)

---

## Prerequisites

### Required Software

- **Python 3.9+**
- **Go 1.19+** (for Redis balance service)
- **Redis 6.0+**
- **Git**
- **Telegram Bot Token** (from [@BotFather](https://t.me/botfather))

### System Requirements

- **OS:** macOS, Linux, or Windows (WSL recommended)
- **RAM:** 2GB minimum
- **Disk:** 1GB free space

---

## Project Structure

```
Ludice/
├── backend/
│   ├── new.py              # Main FastAPI game API
│   ├── financne.py         # Payment API
│   ├── redis/
│   │   ├── main.go         # Go balance service
│   │   └── go.mod
│   └── secrets.json        # Backend secrets (create this)
├── frontend/
│   ├── app.py              # Bot entry point
│   ├── routers/
│   │   └── private_user.py # Main bot logic
│   ├── keyboard/
│   │   └── start.py        # UI keyboards
│   ├── common/
│   │   ├── legal_text.py   # Legal texts
│   │   └── bot_cmds_list.py
│   ├── requirements.txt
│   └── .env                # Frontend environment (create this)
├── data/                   # JSON data files (auto-created)
├── docs/                   # Documentation
└── requirements.txt        # Project-wide dependencies
```

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Wizer27/Ludice.git
cd Ludice
```

### 2. Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Project Dependencies

```bash
# Install main dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
pip install -r requirements.txt
cd ..
```

---

## Backend Setup

### 1. Create Backend Secrets File

Create `backend/secrets.json`:

```json
{
    "secret_key": "your-strong-random-secret-key-here-min-32-chars"
}
```

**Generate a secure secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Create Data Directory

```bash
mkdir -p data
```

The following JSON files will be auto-created on first run:
- `bank.json`
- `game.json`
- `users.json`
- `stats.json`
- `lobby.json`
- `bets.json`
- `payments.json`
- `times_sec.json`

### 3. Install Redis

**macOS (Homebrew):**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

**Verify Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

### 4. Test Backend API

```bash
cd backend
python new.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8080
```

**Test the API:**
```bash
curl http://localhost:8080/
```

---

## Frontend Setup

### 1. Create Telegram Bot

1. Message [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow prompts to name your bot
4. Copy the bot token (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Create Environment File

Create `frontend/.env`:

```bash
# Telegram Bot Token from BotFather
TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# HMAC Secret Key (MUST MATCH backend/secrets.json)
SECRET_KEY=your-strong-random-secret-key-here-min-32-chars

# Telegram Payment Token (for Stars payment)
# Get from BotFather: /mybots → select bot → Payments
secret_token=your_telegram_payment_token
```

**Important:** The `SECRET_KEY` must match the `secret_key` in `backend/secrets.json`

### 3. Verify Installation

```bash
cd frontend
python -c "import aiogram; print(aiogram.__version__)"
# Should print: 3.22.0
```

---

## Redis Service Setup

### 1. Install Go Dependencies

```bash
cd backend/redis
go mod download
```

### 2. Build the Service

```bash
go build -o balance-service main.go
```

### 3. Test the Service

```bash
go run main.go
```

You should see:
```
[GIN-debug] Listening and serving HTTP on :8000
```

**Test the service:**
```bash
curl -X POST http://localhost:8000/create_user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "initial_balance": 100}'
```

---

## Running the Application

### Option 1: Manual (Development)

**Terminal 1 - Backend API:**
```bash
cd backend
python new.py
```

**Terminal 2 - Redis Balance Service:**
```bash
cd backend/redis
go run main.go
```

**Terminal 3 - Telegram Bot:**
```bash
cd frontend
python app.py
```

**Terminal 4 - Redis (if not running as service):**
```bash
redis-server
```

### Option 2: Using tmux (Linux/macOS)

```bash
# Install tmux
brew install tmux  # macOS
# or
sudo apt install tmux  # Linux

# Run all services
./scripts/start-all.sh  # (create this script)
```

**Example `scripts/start-all.sh`:**
```bash
#!/bin/bash
tmux new-session -d -s ludice
tmux send-keys -t ludice 'cd backend && python new.py' C-m
tmux split-window -t ludice
tmux send-keys -t ludice 'cd backend/redis && go run main.go' C-m
tmux split-window -t ludice
tmux send-keys -t ludice 'cd frontend && python app.py' C-m
tmux attach -t ludice
```

### Option 3: Docker Compose (Recommended for Production)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend-api:
    build:
      context: ./backend
    ports:
      - "8080:8080"
    environment:
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - redis

  balance-service:
    build:
      context: ./backend/redis
    ports:
      - "8000:8000"
    depends_on:
      - redis

  bot:
    build:
      context: ./frontend
    environment:
      - TOKEN=${TOKEN}
      - SECRET_KEY=${SECRET_KEY}
      - secret_token=${secret_token}
    depends_on:
      - backend-api
      - balance-service
```

**Run with Docker:**
```bash
docker-compose up
```

---

## Telegram Bot Configuration

### 1. Set Bot Commands

Message [@BotFather](https://t.me/botfather):

```
/setcommands

start - Start the bot and view terms
help - Get help and support
```

### 2. Enable Payments

1. Message [@BotFather](https://t.me/botfather)
2. Send `/mybots`
3. Select your bot
4. Click "Payments"
5. Choose payment provider (for Telegram Stars, select the Stars option)
6. Copy the payment token to `frontend/.env` as `secret_token`

### 3. Set Bot Description

```
/setdescription

Ludicé - A dice rolling game where you compete against other players. Bet Stars and win! 18+ only.
```

### 4. Set About Text

```
/setabouttext

Play dice, compete, and win! 🎲
```

---

## Testing

### 1. Test Bot Startup

```bash
cd frontend
python app.py
```

Expected output:
```
✅ Bot started! Waiting for updates...
Press Ctrl+C to stop the bot.
Included routers: start_router, game_router
```

### 2. Test Bot Commands

Open Telegram and message your bot:

1. **Send `/start`**
   - Should show Terms of Service
   - Should have "Accept" and "Decline" buttons

2. **Click "Accept"**
   - Should register user to backend
   - Should show main menu

3. **Click "Top up 🔝"**
   - Should show payment options

4. **Click "Roll 🎲" → "Dice 🎲"**
   - Should show gambling reminder
   - Should ask for bet amount

5. **Enter bet amount (e.g., "50")**
   - Should send to backend
   - Should search for opponent

### 3. Test Backend API Manually

**Register User:**
```bash
# Generate signature (use Python script)
python scripts/test_api.py register testuser 123456
```

**Start Game:**
```bash
python scripts/test_api.py start_game testuser 50
```

### 4. Test Redis Service

```bash
# Create user
curl -X POST http://localhost:8000/create_user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "initial_balance": 1000}'

# Check balance
curl http://localhost:8000/get_balance?username=testuser
```

---

## Troubleshooting

### Bot Won't Start

**Error: `ImportError: attempted relative import beyond top-level package`**

**Solution:**
```bash
# Make sure you're in the frontend directory
cd frontend
python app.py
```

---

### Backend Won't Connect

**Error: `Connection refused on port 8080`**

**Solution:**
```bash
# Check if backend is running
curl http://localhost:8080/

# Start backend if not running
cd backend
python new.py
```

---

### Redis Connection Failed

**Error: `Redis connection refused`**

**Solution:**
```bash
# Check Redis status
redis-cli ping

# If not running, start Redis
# macOS:
brew services start redis

# Linux:
sudo systemctl start redis

# Manual:
redis-server
```

---

### Signature Verification Failed

**Error: `Invalid signature`**

**Cause:** `SECRET_KEY` mismatch between frontend and backend

**Solution:**
```bash
# Make sure these match:
cat frontend/.env | grep SECRET_KEY
cat backend/secrets.json | grep secret_key
```

---

### Payment Not Working

**Error: `Invalid payment token`**

**Solution:**
1. Get correct token from BotFather: `/mybots` → Your Bot → Payments
2. Update `secret_token` in `frontend/.env`
3. Restart bot

---

### Port Already in Use

**Error: `Address already in use: 8080`**

**Solution:**
```bash
# Find process using port
lsof -i :8080

# Kill process
kill -9 <PID>
```

---

## Production Deployment

### 1. Environment Variables

**Never commit `.env` or `secrets.json` to Git!**

Add to `.gitignore`:
```
.env
secrets.json
*.pyc
__pycache__/
```

### 2. Use Process Manager

**PM2 (Node.js):**
```bash
npm install -g pm2

pm2 start backend/new.py --name backend-api
pm2 start backend/redis/main.go --name balance-service
pm2 start frontend/app.py --name telegram-bot
pm2 save
pm2 startup
```

**systemd (Linux):**
Create `/etc/systemd/system/ludice-bot.service`:
```ini
[Unit]
Description=Ludicé Telegram Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/Ludice/frontend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ludice-bot
sudo systemctl start ludice-bot
```

### 3. Use Reverse Proxy

**nginx configuration:**
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Database Migration

For production, migrate from JSON files to PostgreSQL:

```python
# Install dependencies
pip install asyncpg sqlalchemy

# Create tables
# See backend/models.py (create this)
```

### 5. Monitoring

**Add logging:**
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
```

**Add health checks:**
```python
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": time.time()}
```

### 6. Security Hardening

1. **Use HTTPS** (Let's Encrypt)
2. **Firewall rules** (UFW, iptables)
3. **Rate limiting** (nginx, slowapi)
4. **Input validation** (Pydantic models)
5. **Secret rotation** (regularly update SECRET_KEY)

### 7. Backup Strategy

```bash
# Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Backup Redis
redis-cli --rdb dump.rdb
```

---

## Next Steps

1. Read [TECHNICAL_ARCHITECTURE.md](technical-architecture) for system details
2. Read [API_DOCUMENTATION.md](api-documentation) for API reference
3. Review [DEVELOPMENT_GUIDE.md](development-guide) for contribution guidelines
4. Check legal documentation in `docs/legal/`

---

**Last Updated:** January 2025

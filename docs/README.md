# Ludicé Documentation

Complete documentation for the Ludicé Telegram bot dice-rolling game.

## 📚 Documentation Index

### Getting Started

- **[Setup Guide](SETUP_GUIDE.md)** - Complete installation and configuration guide
  - Prerequisites and system requirements
  - Environment setup
  - Running the application
  - Troubleshooting

### Technical Documentation

- **[Technical Architecture](TECHNICAL_ARCHITECTURE.md)** - System design and architecture
  - Architecture overview
  - Component descriptions
  - Data flow diagrams
  - Technology stack
  - Scalability considerations

- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference
  - Backend Game API
  - Balance Service API
  - Frontend Bot Integration
  - Authentication (HMAC-SHA256)
  - Error handling

### Development

- **[Development Guide](DEVELOPMENT_GUIDE.md)** - For contributors and developers
  - Development environment setup
  - Code structure
  - Adding features
  - Testing
  - Git workflow

### Legal

- **[Legal Documents](legal/)** - Terms, privacy, and compliance
  - [Bot Summary](legal/BOT_SUMMARY.md) - Quick legal reference
  - [Terms of Service](legal/TERMS_OF_SERVICE.md) - Full terms
  - [Privacy Policy](legal/PRIVACY_POLICY.md) - Privacy and data handling
  - [Responsible Gambling](legal/RESPONSIBLE_GAMBLING.md) - Gambling policy
  - [Legal Implementation Guide](legal/README.md) - Integration instructions

---

## Quick Links

### 🚀 I want to...

**Get started quickly:**
→ [Setup Guide](SETUP_GUIDE.md)

**Understand the architecture:**
→ [Technical Architecture](TECHNICAL_ARCHITECTURE.md)

**Integrate with the API:**
→ [API Documentation](API_DOCUMENTATION.md)

**Add new features:**
→ [Development Guide](DEVELOPMENT_GUIDE.md)

**Review legal requirements:**
→ [Legal Documents](legal/)

---

## Project Overview

### What is Ludicé?

Ludicé is a Telegram bot that lets users play dice-rolling games against each other. Players bet Telegram Stars (in-app currency) and compete to win their opponent's bet.

### Key Features

- **🎲 Dice Game** - Roll dice, highest wins
- **⭐ Telegram Stars Payment** - Buy-in with Telegram's native currency
- **🔒 Secure** - HMAC-SHA256 authenticated API calls
- **⚖️ Fair** - No house edge (100% winner takes all)
- **🔞 Responsible Gaming** - Built-in gambling safeguards

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Python 3.9+ / aiogram 3.22.0 |
| **Backend API** | Python 3.9+ / FastAPI 0.119.0 |
| **Balance Service** | Go 1.19+ / Gin / Redis |
| **Data Storage** | JSON files (development) |
| **Payment** | Telegram Stars (XTR) |
| **Authentication** | HMAC-SHA256 |

---

## Architecture Overview

```
┌─────────────┐
│ Telegram    │
│ User        │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Frontend (aiogram)  │
│ - Bot handlers      │
│ - FSM states        │
│ - Payment UI        │
└──────┬──────────────┘
       │ HMAC Auth
       ▼
┌─────────────────────┐
│ Backend (FastAPI)   │
│ - Game logic        │
│ - User management   │
│ - Signature verify  │
└──────┬──────────────┘
       │ HTTP
       ▼
┌─────────────────────┐
│ Balance (Go/Redis)  │
│ - User balances     │
│ - Redis storage     │
└─────────────────────┘
```

**For detailed architecture:**
→ [Technical Architecture](TECHNICAL_ARCHITECTURE.md)

---

## Quick Start

### 1. Prerequisites

- Python 3.9+
- Go 1.19+
- Redis
- Telegram Bot Token

### 2. Install

```bash
# Clone repository
git clone https://github.com/Wizer27/Ludice.git
cd Ludice

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
cd frontend && pip install -r requirements.txt
```

### 3. Configure

Create `frontend/.env`:

```bash
TOKEN=your_telegram_bot_token
SECRET_KEY=your_shared_secret_key
secret_token=your_payment_token
```

Create `backend/secrets.json`:

```json
{
    "secret_key": "your_shared_secret_key"
}
```

### 4. Run

```bash
# Terminal 1: Backend API
cd backend
python new.py

# Terminal 2: Balance Service
cd backend/redis
go run main.go

# Terminal 3: Bot
cd frontend
python app.py
```

**For detailed setup:**
→ [Setup Guide](SETUP_GUIDE.md)

---

## Game Flow

### User Journey

1. **Start** - User sends `/start` to bot
2. **Terms** - User accepts Terms of Service
3. **Registration** - Bot registers user to backend
4. **Main Menu** - User sees menu (Roll, Top up, Profile, Help)
5. **Play** - User clicks "Roll 🎲" → "Dice 🎲"
6. **Bet** - User enters bet amount (min 10 stars)
7. **Match** - System finds opponent or creates lobby
8. **Roll** - Both players roll dice
9. **Result** - Winner gets 100% of both bets

### Payment Flow

1. **Top Up** - User clicks "Top up 🔝"
2. **Select Amount** - Choose from 15-1,000,000 stars
3. **Pay** - Telegram processes payment (Telegram Stars)
4. **Credit** - Balance updated (~25% fee applied)

**For API details:**
→ [API Documentation](API_DOCUMENTATION.md)

---

## Development

### Project Structure

```
Ludice/
├── frontend/           # Telegram bot (Python/aiogram)
│   ├── app.py
│   ├── routers/
│   ├── keyboard/
│   └── common/
├── backend/            # Game API (Python/FastAPI)
│   ├── new.py
│   ├── financne.py
│   └── redis/          # Balance service (Go)
├── data/               # JSON data files
├── docs/               # Documentation (you are here!)
│   ├── legal/
│   └── my-docs/        # Docusaurus site
└── requirements.txt
```

### Adding a Feature

1. Read [Development Guide](DEVELOPMENT_GUIDE.md)
2. Create feature branch: `git checkout -b feature/my-feature`
3. Implement changes
4. Test locally
5. Submit pull request to `dev` branch

**For contribution guidelines:**
→ [Development Guide](DEVELOPMENT_GUIDE.md)

---

## API Reference

### Backend Game API (Port 8080)

**Authentication:** HMAC-SHA256 signature required

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register` | POST | Register new user |
| `/start/game` | POST | Start/join game |
| `/write/res` | POST | Submit dice result |
| `/leave` | POST | Leave lobby |

### Balance Service API (Port 8000)

**Authentication:** None (internal service)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/create_user` | POST | Create user account |
| `/get_balance` | GET | Query user balance |
| `/modify_balance` | POST | Add/subtract balance |

**For complete API reference:**
→ [API Documentation](API_DOCUMENTATION.md)

---

## Security

### HMAC Authentication

All frontend → backend requests use HMAC-SHA256 signatures:

```python
# Create signature
data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
signature = hmac.new(
    SECRET_KEY.encode(),
    data_str.encode(),
    hashlib.sha256
).hexdigest()

# Send with X-Signature header
headers = {"X-Signature": signature}
```

### Rate Limiting

- **IP-based:** 10 requests/minute
- **User-based:** 1 request/second minimum

### Environment Variables

Never commit:
- `.env` files
- `secrets.json`
- API tokens

**For security details:**
→ [Technical Architecture](TECHNICAL_ARCHITECTURE.md#security-architecture)

---

## Testing

### Run Tests

```bash
# Python tests
pytest tests/

# Type checking
mypy frontend/ backend/

# Linting
flake8 frontend/ backend/
black --check frontend/ backend/
```

### Manual Testing

```bash
# Test bot
cd frontend
python scripts/test_bot.py

# Test API
python scripts/test_api.py register testuser 123456

# Test balance service
curl http://localhost:8000/get_balance?username=testuser
```

**For testing guide:**
→ [Development Guide](DEVELOPMENT_GUIDE.md#testing)

---

## Legal Compliance

### Required Actions

Before deploying to production:

- [ ] Update jurisdiction in Terms of Service
- [ ] Add physical address in Privacy Policy
- [ ] Specify server locations
- [ ] Review with legal counsel
- [ ] Implement terms acceptance tracking
- [ ] Set up age verification

### Available Legal Documents

- Terms of Service (22 sections)
- Privacy Policy (GDPR/CCPA compliant)
- Responsible Gambling Policy
- Bot Summary (quick reference)

**For legal implementation:**
→ [Legal Documents](legal/)

---

## Deployment

### Development

```bash
# Run locally (see Quick Start above)
```

### Production (Docker Compose)

```yaml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
  backend-api:
    build: ./backend
  balance-service:
    build: ./backend/redis
  bot:
    build: ./frontend
```

```bash
docker-compose up -d
```

### Production (Manual)

1. Use process manager (PM2, systemd)
2. Set up reverse proxy (nginx)
3. Enable HTTPS (Let's Encrypt)
4. Configure firewall
5. Set up monitoring
6. Implement backups

**For deployment guide:**
→ [Setup Guide](SETUP_GUIDE.md#production-deployment)

---

## Troubleshooting

### Common Issues

**Bot won't start**
→ Check `TOKEN` in `.env`

**Signature verification failed**
→ Ensure `SECRET_KEY` matches in frontend/.env and backend/secrets.json

**Redis connection refused**
→ Start Redis: `redis-server`

**Port already in use**
→ `lsof -i :8080` then `kill -9 <PID>`

**For more troubleshooting:**
→ [Setup Guide](SETUP_GUIDE.md#troubleshooting)

---

## Resources

### Official Documentation

- [aiogram](https://docs.aiogram.dev/) - Telegram bot framework
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Telegram Bot API](https://core.telegram.org/bots/api) - Bot API reference
- [Telegram Payments](https://core.telegram.org/bots/payments) - Payment integration

### Community

- GitHub: [github.com/Wizer27/Ludice](https://github.com/Wizer27/Ludice)
- Telegram Support: [@ludicegifter](https://t.me/ludicegifter)

---

## Contributing

We welcome contributions! Please:

1. Read [Development Guide](DEVELOPMENT_GUIDE.md)
2. Fork the repository
3. Create feature branch
4. Make changes
5. Submit pull request to `dev` branch

### Code Style

- Python: Follow PEP 8, use Black formatter
- Go: Use gofmt
- Commits: Use Conventional Commits format

---

## License

Copyright © 2025 Ludicé

See LICENSE file for details.

---

## Support

### For Users

- Telegram: [@ludicegifter](https://t.me/ludicegifter)
- Email: support@ludice.com (if available)

### For Developers

- GitHub Issues: [Report bugs](https://github.com/Wizer27/Ludice/issues)
- Documentation: Read this documentation
- Pull Requests: Contribute code

---

## Changelog

### Version 1.0.0 (January 2025)

- Initial release
- Dice game implementation
- Telegram Stars payment integration
- Terms acceptance flow
- HMAC authentication
- Rate limiting
- Comprehensive documentation

---

**Last Updated:** January 2025
**Documentation Version:** 1.0.0

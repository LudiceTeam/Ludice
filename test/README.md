# Ludicé Test Suite

Comprehensive test suite for the Ludicé Telegram dice gambling bot.

## Overview

This test suite covers:
- **Backend API** (FastAPI) - Authentication, user management, game logic
- **Frontend Bot** (Aiogram) - Message handlers, payments, FSM states
- **Security** - HMAC signatures, rate limiting, timestamp validation
- **Integration** - Cross-service interactions

## Test Structure

```
test/
├── conftest.py                    # Shared fixtures and configuration
├── backend/
│   ├── test_auth.py              # Authentication & security tests
│   ├── test_user_endpoints.py    # User registration & balance tests
│   ├── test_game_endpoints.py    # Game logic & lobby tests
│   └── test_stats.py             # Statistics & leaderboard tests
├── frontend/
│   ├── test_handlers.py          # Message & callback handlers
│   ├── test_legal_router.py      # Legal commands & terms acceptance
│   └── test_keyboards.py         # Keyboard layouts & buttons
└── README.md                      # This file
```

## Installation

### Install Test Dependencies

```bash
# From project root
pip install pytest pytest-asyncio pytest-cov httpx

# Or install from requirements
pip install -r requirements.txt
```

### Required Packages

- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `httpx` - FastAPI test client
- `unittest.mock` - Mocking (built-in)

## Running Tests

### Run All Tests

```bash
# From project root
pytest

# With verbose output
pytest -v

# With coverage
pytest --cov=backend --cov=frontend --cov-report=html
```

### Run Specific Test Suites

```bash
# Backend tests only
pytest test/backend/

# Frontend tests only
pytest test/frontend/

# Specific test file
pytest test/backend/test_auth.py

# Specific test class
pytest test/backend/test_auth.py::TestSignatureVerification

# Specific test method
pytest test/backend/test_auth.py::TestSignatureVerification::test_valid_signature
```

### Run Tests by Marker

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Backend tests
pytest -m backend

# Frontend tests
pytest -m frontend

# Exclude slow tests
pytest -m "not slow"
```

### Run Tests with Output Options

```bash
# Show print statements
pytest -s

# Show local variables on failure
pytest -l

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run failed tests first
pytest --ff
```

## Test Coverage

### Generate Coverage Report

```bash
# HTML report (opens in browser)
pytest --cov=backend --cov=frontend --cov-report=html
open htmlcov/index.html

# Terminal report
pytest --cov=backend --cov=frontend --cov-report=term-missing

# Coverage with branch analysis
pytest --cov=backend --cov=frontend --cov-branch --cov-report=term
```

### Coverage Goals

- **Overall**: >80% code coverage
- **Critical paths**: 100% coverage
  - Authentication & security
  - Payment processing
  - Game result submission

## Test Categories

### Backend Tests

#### Authentication Tests (`test_auth.py`)
- HMAC-SHA256 signature verification
- Timestamp validation (300s expiry)
- Rate limiting (1 request/second per user)
- Tamper detection
- Timing attack resistance

**Key Tests:**
- `test_valid_signature` - Valid HMAC passes
- `test_invalid_signature` - Invalid HMAC fails
- `test_tampered_data_fails_verification` - Data tampering detected
- `test_expired_timestamp_fails` - Old timestamps rejected
- `test_rapid_requests_blocked` - Rate limiting enforced

#### User Endpoint Tests (`test_user_endpoints.py`)
- User registration
- Balance increase/decrease
- Withdrawals
- User info retrieval

**Key Tests:**
- `test_register_new_user_success` - User registration works
- `test_register_duplicate_user_fails` - Duplicates rejected
- `test_increase_balance_success` - Balance updates
- `test_withdraw_insufficient_balance` - Prevents overdraft

#### Game Endpoint Tests (`test_game_endpoints.py`)
- Game lobby creation
- Lobby matching by bet amount
- Player join/leave
- Result submission
- Winner determination

**Key Tests:**
- `test_create_new_lobby` - Creates lobby when none exists
- `test_join_existing_lobby` - Joins matching lobby
- `test_cannot_join_own_lobby` - Self-join prevention
- `test_write_dice_result` - Result recording
- `test_write_winner` - Winner tracking

#### Stats Tests (`test_stats.py`)
- Win tracking
- Game counting
- Win percentage calculation
- Leaderboards
- Data integrity

**Key Tests:**
- `test_add_win_existing_user` - Win counting
- `test_calculate_win_percentage_50_percent` - Stats math
- `test_leaderboard_most_games` - Rankings
- `test_wins_cannot_exceed_total_games` - Data validation

### Frontend Tests

#### Handler Tests (`test_handlers.py`)
- `/start` command
- Payment callbacks (15-1000 stars)
- Pre-checkout handling
- Successful payment confirmation
- FSM state management
- Bet processing

**Key Tests:**
- `test_start_command_sends_welcome` - Start message
- `test_star15_payment_callback` - Payment flow
- `test_pre_checkout_answers_ok` - Checkout approval
- `test_process_bet_valid_number` - Bet validation
- `test_dice_game_shows_gambling_reminder` - Responsible gambling

#### Legal Router Tests (`test_legal_router.py`)
- `/terms`, `/privacy`, `/gambling` commands
- Callback navigation
- Terms acceptance flow
- Age verification
- Gambling reminders

**Key Tests:**
- `test_terms_command` - Terms display
- `test_accept_terms_callback` - Terms acceptance
- `test_underage_callback` - Age restriction
- `test_show_gambling_reminder` - Reminder display

#### Keyboard Tests (`test_keyboards.py`)
- Start menu keyboard
- Payment options keyboard
- Game selection keyboard
- Button structure
- Callback data

**Key Tests:**
- `test_start_keyboard_has_buttons` - Main menu buttons
- `test_all_tier_options_present` - Payment tiers
- `test_dice_button_has_emoji` - Button formatting

## Writing New Tests

### Test Structure (AAA Pattern)

```python
def test_feature_description(self):
    """Test that feature behaves as expected."""
    # Arrange - Set up test data and mocks
    user_data = {"username": "test_user", "balance": 100}

    # Act - Execute the code under test
    result = some_function(user_data)

    # Assert - Verify expected behavior
    assert result == expected_value
```

### Async Tests

```python
@pytest.mark.asyncio
async def test_async_handler(self, mock_message, mock_fsm_context):
    """Test async handler function."""
    # Arrange
    message = mock_message("/start")
    message.answer = AsyncMock()

    # Act
    await handler_function(message, mock_fsm_context)

    # Assert
    message.answer.assert_called_once()
```

### Using Fixtures

```python
def test_with_fixtures(self, signature_generator, test_secret_key):
    """Test using pytest fixtures."""
    # Fixtures are automatically provided
    data = {"username": "test"}
    signature = signature_generator(data)

    assert len(signature) == 64  # SHA256 hex length
```

### Mocking

```python
def test_with_mocking(self):
    """Test with mocked dependencies."""
    with patch("backend.new.verify_signature", return_value=True):
        # Code that calls verify_signature will get True
        result = some_function_that_verifies()
        assert result is True
```

## Common Issues & Solutions

### Issue: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'backend'`

**Solution**:
```bash
# Run tests from project root
cd /path/to/Ludice
pytest

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/Ludice"
pytest
```

### Issue: Async Tests Not Running

**Problem**: Async tests are skipped or fail

**Solution**:
```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Ensure pytest.ini has asyncio_mode = auto
```

### Issue: Fixture Not Found

**Problem**: `fixture 'some_fixture' not found`

**Solution**:
- Ensure `conftest.py` is in the test directory
- Check fixture name spelling
- Verify fixture scope

### Issue: Mock Not Working

**Problem**: Mocked function still calls real implementation

**Solution**:
```python
# Use correct import path (where it's used, not where it's defined)
with patch("backend.new.verify_signature"):  # ✓ Correct
with patch("backend.helper.verify_signature"):  # ✗ Wrong
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-asyncio pytest-cov
      - run: pytest --cov=backend --cov=frontend
```

## Test Data

### Mock Users

The test suite uses these mock users:
- `test_user_123` - Standard test user (ID: 123456789)
- `player1`, `player2` - Game participants
- `new_user` - Fresh registration tests

### Mock Secrets

- **Test Secret Key**: `test_secret_key_for_hmac_signatures_12345`
- **Test Bot Token**: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

**⚠️ Never use these in production!**

## Performance

### Test Execution Time

- **Fast tests** (unit): <1s per test
- **Slow tests** (integration): 1-5s per test
- **Full suite**: ~30-60s

### Optimization Tips

1. **Run in parallel**:
   ```bash
   pip install pytest-xdist
   pytest -n auto
   ```

2. **Skip slow tests during development**:
   ```bash
   pytest -m "not slow"
   ```

3. **Use test database/mock files**:
   - Fixtures create temporary files
   - No need for real data

## Continuous Improvement

### Adding Coverage

Check uncovered lines:
```bash
pytest --cov=backend --cov-report=term-missing
```

Look for:
- Missing edge cases
- Error handling
- Boundary conditions

### Test Maintenance

- **Update tests when code changes**
- **Remove obsolete tests**
- **Refactor duplicated test code into fixtures**
- **Keep tests focused and isolated**

## Support

For questions or issues:
- Check existing tests for examples
- Review `conftest.py` for available fixtures
- See [pytest documentation](https://docs.pytest.org/)
- Contact: @ludicegifter (Telegram)

## License

Tests are part of the Ludicé project and follow the same license.

---

**Last Updated**: January 2025
**Test Coverage**: 80%+ (target)
**Total Tests**: 150+

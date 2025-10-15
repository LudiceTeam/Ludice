# Quick Start Guide - Ludicé Tests

Quick reference for running and understanding tests.

## Installation (One-Time Setup)

```bash
cd /Users/vikrorkhanin/Ludice
pip install pytest pytest-asyncio pytest-cov httpx
```

## Running Tests

### Most Common Commands

```bash
# Run all tests
pytest

# Run all tests with detailed output
pytest -v

# Run all tests with coverage report
pytest --cov=backend --cov=frontend --cov-report=term-missing

# Run only backend tests
pytest test/backend/

# Run only frontend tests
pytest test/frontend/

# Run specific test file
pytest test/backend/test_auth.py

# Stop at first failure (useful for debugging)
pytest -x
```

## Understanding Test Output

### Successful Test Run
```
test/backend/test_auth.py::TestSignatureVerification::test_valid_signature PASSED [1%]
test/backend/test_auth.py::TestSignatureVerification::test_invalid_signature PASSED [2%]
...
==================== 189 passed in 5.23s ====================
```

### Failed Test
```
test/backend/test_auth.py::TestSignatureVerification::test_valid_signature FAILED

======================================== FAILURES ========================================
______ TestSignatureVerification.test_valid_signature ______

    def test_valid_signature(self):
>       assert result is True
E       AssertionError: assert False is True

test/backend/test_auth.py:45: AssertionError
```

## Test Categories

### Backend Tests
- **test_auth.py** - Security, signatures, rate limiting
- **test_user_endpoints.py** - User registration, balance
- **test_game_endpoints.py** - Game creation, lobbies
- **test_stats.py** - Win tracking, leaderboards

### Frontend Tests
- **test_handlers.py** - Bot commands, payments
- **test_legal_router.py** - Terms, privacy, gambling
- **test_keyboards.py** - Button layouts

## Common Scenarios

### Before Committing Code
```bash
# Run all tests
pytest

# Or with coverage
pytest --cov=backend --cov=frontend
```

### After Changing Backend
```bash
pytest test/backend/ -v
```

### After Changing Frontend
```bash
pytest test/frontend/ -v
```

### Debugging a Failing Test
```bash
# Run specific test with verbose output
pytest test/backend/test_auth.py::TestSignatureVerification::test_valid_signature -v

# Show print statements
pytest test/backend/test_auth.py::TestSignatureVerification::test_valid_signature -s

# Stop at first failure with local variables
pytest test/backend/test_auth.py -x -l
```

### Generate HTML Coverage Report
```bash
pytest --cov=backend --cov=frontend --cov-report=html
open htmlcov/index.html
```

## Test Markers

Run specific types of tests:

```bash
# Backend tests only
pytest -m backend

# Frontend tests only
pytest -m frontend

# Unit tests only
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

## Troubleshooting

### "Module not found" error
```bash
# Make sure you're in the project root
cd /Users/vikrorkhanin/Ludice
pytest
```

### Async tests not running
```bash
# Install pytest-asyncio
pip install pytest-asyncio
```

### Tests fail with import errors
```bash
# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/Users/vikrorkhanin/Ludice"
pytest
```

## Test Count

- **Total Tests**: 189
- **Backend**: ~100 tests
- **Frontend**: ~89 tests
- **Execution Time**: ~5-10 seconds

## Coverage Goals

- **Target**: >80% overall coverage
- **Critical paths**: 100% coverage
  - Authentication
  - Payment processing
  - Game logic

## Next Steps

1. Read `test/README.md` for detailed documentation
2. Review `TEST_SUMMARY.md` for complete overview
3. Check `conftest.py` for available fixtures
4. Look at existing tests as examples

## Quick Tips

- Tests follow **Arrange-Act-Assert** pattern
- Use `@pytest.mark.asyncio` for async tests
- Mock external dependencies (files, Redis, Telegram API)
- Keep tests isolated and independent
- Test both success and failure scenarios

## Support

- Detailed guide: `test/README.md`
- Test overview: `TEST_SUMMARY.md`
- Contact: @ludicegifter

---

**Last Updated**: January 2025

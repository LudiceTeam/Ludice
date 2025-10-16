"""
Test configuration and shared fixtures for Ludicé test suite.

This module provides pytest fixtures for backend and frontend testing,
including mock data, test clients, and signature generation utilities.
"""

import pytest
import json
import hmac
import hashlib
import time
import tempfile
import os
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, Generator
from pathlib import Path

# FastAPI testing
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Aiogram testing
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import User, Chat, Message, CallbackQuery, Update


# ============================================================================
# Test Configuration
# ============================================================================

TEST_SECRET_KEY = "test_secret_key_for_hmac_signatures_12345"
TEST_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"


# ============================================================================
# Backend Fixtures - FastAPI
# ============================================================================

@pytest.fixture
def test_secret_key() -> str:
    """Provide test secret key for HMAC signatures."""
    return TEST_SECRET_KEY


@pytest.fixture
def mock_secrets_file(tmp_path: Path, test_secret_key: str) -> Generator[Path, None, None]:
    """Create temporary secrets.json file for testing."""
    secrets_path = tmp_path / "secrets.json"
    secrets_data = {"key": test_secret_key}

    with open(secrets_path, "w") as f:
        json.dump(secrets_data, f)

    # Patch the secrets file path in the backend
    with patch("backend.new.open", create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(secrets_data)
        yield secrets_path


@pytest.fixture
def signature_generator(test_secret_key: str):
    """
    Provide a function to generate valid HMAC-SHA256 signatures for requests.

    Usage:
        signature = signature_generator({"username": "test", "amount": 100})
    """
    def generate(data: Dict[str, Any]) -> str:
        """Generate HMAC signature for request data."""
        # Add timestamp if not present
        if "timestamp" not in data:
            data["timestamp"] = time.time()

        # Remove signature field if present
        data_copy = data.copy()
        data_copy.pop("signature", None)

        # Create signature
        data_str = json.dumps(data_copy, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        return signature

    return generate


@pytest.fixture
def mock_json_files(tmp_path: Path) -> Dict[str, Path]:
    """Create temporary JSON data files for testing."""
    data_dir = tmp_path / "data"
    data_dir.mkdir(exist_ok=True)

    files = {
        "users": data_dir / "users.json",
        "bank": tmp_path / "bank.json",
        "game": tmp_path / "game.json",
        "stats": tmp_path / "stats.json",
        "lobby": tmp_path / "lobby.json",
        "bets": tmp_path / "bets.json",
        "payments": tmp_path / "payments.json",
        "times_sec": tmp_path / "time_sec.json",
        "data_second_game": tmp_path / "data_second_game.json",
        "drotic": tmp_path / "drotic.json",
    }

    # Initialize with empty or default data
    default_data = {
        "users": {},
        "bank": [],
        "game": [],
        "stats": [],
        "lobby": [],
        "bets": [],
        "payments": [],
        "times_sec": {},
        "data_second_game": [],
        "drotic": [],
    }

    for key, path in files.items():
        with open(path, "w") as f:
            json.dump(default_data[key], f)

    return files


@pytest.fixture
def test_user_data() -> Dict[str, Any]:
    """Provide test user data."""
    return {
        "username": "test_user_123",
        "user_id": "123456789",
        "balance": 100,
        "psw": "test_password"
    }


@pytest.fixture
def test_game_data() -> Dict[str, Any]:
    """Provide test game data."""
    return {
        "id": "test_game_123",
        "bet": 10,
        "players": [],
        "winner": "",
        "result_test_user_123": None,
    }


@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    with patch("backend.new.redis") as mock:
        mock.exists.return_value = False
        mock.set.return_value = True
        mock.get.return_value = None
        yield mock


@pytest.fixture
def fastapi_client(mock_json_files: Dict[str, Path], test_secret_key: str):
    """
    Provide FastAPI test client with mocked dependencies.

    Note: This requires proper patching of file operations in backend.new
    """
    # Import the FastAPI app
    from backend.new import app

    # Create test client
    with TestClient(app) as client:
        yield client


@pytest.fixture
def reset_rate_limit(mock_json_files: Dict[str, Path]):
    """Reset rate limiting data between tests."""
    with open(mock_json_files["times_sec"], "w") as f:
        json.dump({}, f)
    yield
    # Cleanup after test
    with open(mock_json_files["times_sec"], "w") as f:
        json.dump({}, f)


# ============================================================================
# Frontend Fixtures - Aiogram Bot
# ============================================================================

@pytest.fixture
def bot() -> Bot:
    """Provide mock Telegram bot instance."""
    return Bot(token=TEST_BOT_TOKEN, parse_mode="HTML")


@pytest.fixture
def storage() -> MemoryStorage:
    """Provide memory storage for FSM."""
    return MemoryStorage()


@pytest.fixture
def dispatcher(storage: MemoryStorage) -> Dispatcher:
    """Provide Telegram dispatcher with test configuration."""
    dp = Dispatcher(storage=storage)
    return dp


@pytest.fixture
def mock_user() -> User:
    """Provide mock Telegram user."""
    return User(
        id=123456789,
        is_bot=False,
        first_name="Test",
        last_name="User",
        username="testuser",
        language_code="en"
    )


@pytest.fixture
def mock_chat() -> Chat:
    """Provide mock Telegram chat."""
    return Chat(
        id=123456789,
        type="private"
    )


@pytest.fixture
def mock_message(mock_user: User, mock_chat: Chat):
    """Provide mock Telegram message."""
    def create_message(text: str = "/start", **kwargs) -> Message:
        """Create a mock message with given text and optional parameters."""
        return Message(
            message_id=1,
            date=int(time.time()),
            chat=mock_chat,
            from_user=mock_user,
            text=text,
            **kwargs
        )
    return create_message


@pytest.fixture
def mock_callback_query(mock_user: User, mock_message):
    """Provide mock Telegram callback query."""
    def create_callback(data: str = "test_callback", **kwargs) -> CallbackQuery:
        """Create a mock callback query with given data."""
        message = mock_message()
        message.edit_text = AsyncMock()
        message.edit_reply_markup = AsyncMock()
        message.answer = AsyncMock()
        message.delete = AsyncMock()

        return CallbackQuery(
            id="test_callback_id",
            from_user=mock_user,
            chat_instance="test_chat_instance",
            data=data,
            message=message,
            **kwargs
        )
    return create_callback


@pytest.fixture
def mock_fsm_context():
    """Provide mock FSM context for state testing."""
    context = AsyncMock(spec=FSMContext)
    context.get_data.return_value = {}
    context.update_data = AsyncMock()
    context.set_state = AsyncMock()
    context.clear = AsyncMock()
    return context


@pytest.fixture
def mock_bot_instance():
    """Provide fully mocked bot instance for handler testing."""
    bot = AsyncMock(spec=Bot)
    bot.send_message = AsyncMock()
    bot.send_invoice = AsyncMock()
    bot.answer_pre_checkout_query = AsyncMock()
    bot.delete_webhook = AsyncMock()
    return bot


# ============================================================================
# Helper Functions
# ============================================================================

def create_signed_request(data: Dict[str, Any], secret_key: str) -> Dict[str, Any]:
    """
    Create a request with valid HMAC signature.

    Args:
        data: Request data dictionary
        secret_key: Secret key for signature

    Returns:
        Request data with signature and timestamp added
    """
    request_data = data.copy()

    # Add timestamp
    if "timestamp" not in request_data:
        request_data["timestamp"] = time.time()

    # Generate signature
    data_copy = request_data.copy()
    data_copy.pop("signature", None)
    data_str = json.dumps(data_copy, sort_keys=True, separators=(',', ':'))
    signature = hmac.new(
        secret_key.encode(),
        data_str.encode(),
        hashlib.sha256
    ).hexdigest()

    request_data["signature"] = signature
    return request_data


# ============================================================================
# Pytest Configuration
# ============================================================================

@pytest.fixture(autouse=True)
def reset_test_environment():
    """Reset environment before each test."""
    # Clear any cached data
    yield
    # Cleanup after test


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "backend: mark test as backend API test"
    )
    config.addinivalue_line(
        "markers", "frontend: mark test as frontend bot test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

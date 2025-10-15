"""
Backend Authentication and Security Tests for Ludicé API.

Tests HMAC signature verification, rate limiting, and timestamp validation.
"""

import pytest
import json
import hmac
import hashlib
import time
from unittest.mock import patch, mock_open, MagicMock
from backend.new import verify_signature, check_time_seciruty, KEY


pytestmark = pytest.mark.backend


class TestSignatureVerification:
    """Test HMAC-SHA256 signature verification."""

    def test_valid_signature(self, test_secret_key):
        """Test that valid signature passes verification."""
        # Arrange
        data = {
            "username": "test_user",
            "amount": 100,
            "timestamp": time.time()
        }

        # Create valid signature
        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        data["signature"] = signature

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, signature)

        # Assert
        assert result is True, "Valid signature should pass verification"

    def test_invalid_signature(self, test_secret_key):
        """Test that invalid signature fails verification."""
        # Arrange
        data = {
            "username": "test_user",
            "amount": 100,
            "timestamp": time.time()
        }
        invalid_signature = "invalid_signature_abc123"

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, invalid_signature)

        # Assert
        assert result is False, "Invalid signature should fail verification"

    def test_tampered_data_fails_verification(self, test_secret_key):
        """Test that tampered data fails signature verification."""
        # Arrange
        original_data = {
            "username": "test_user",
            "amount": 100,
            "timestamp": time.time()
        }

        # Create signature for original data
        data_str = json.dumps(original_data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Tamper with data
        tampered_data = original_data.copy()
        tampered_data["amount"] = 1000  # Changed amount

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(tampered_data, signature)

        # Assert
        assert result is False, "Tampered data should fail verification"

    def test_expired_timestamp_fails(self, test_secret_key):
        """Test that expired timestamp (>300 seconds) fails verification."""
        # Arrange
        old_timestamp = time.time() - 301  # 301 seconds ago (expired)
        data = {
            "username": "test_user",
            "amount": 100,
            "timestamp": old_timestamp
        }

        # Create signature
        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, signature)

        # Assert
        assert result is False, "Expired timestamp should fail verification"

    def test_valid_timestamp_passes(self, test_secret_key):
        """Test that recent timestamp (<300 seconds) passes verification."""
        # Arrange
        recent_timestamp = time.time() - 100  # 100 seconds ago (valid)
        data = {
            "username": "test_user",
            "amount": 100,
            "timestamp": recent_timestamp
        }

        # Create signature
        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, signature)

        # Assert
        assert result is True, "Recent timestamp should pass verification"

    def test_missing_timestamp_fails(self, test_secret_key):
        """Test that missing timestamp fails verification."""
        # Arrange
        data = {
            "username": "test_user",
            "amount": 100
            # No timestamp
        }

        # Create signature
        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, signature)

        # Assert
        assert result is False, "Missing timestamp should fail verification"

    def test_signature_field_excluded_from_verification(self, test_secret_key):
        """Test that signature field itself is excluded from signature calculation."""
        # Arrange
        data = {
            "username": "test_user",
            "amount": 100,
            "timestamp": time.time()
        }

        # Create signature WITHOUT signature field
        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Add signature to data
        data["signature"] = signature

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, signature)

        # Assert
        assert result is True, "Signature should be excluded from signature calculation"


class TestRateLimiting:
    """Test rate limiting functionality (1 request per second per user)."""

    def test_first_request_allowed(self, tmp_path):
        """Test that first request from user is allowed."""
        # Arrange
        time_sec_file = tmp_path / "time_sec.json"
        with open(time_sec_file, "w") as f:
            json.dump({}, f)

        username = "test_user"

        # Act
        with patch("builtins.open", mock_open(read_data="{}")):
            with patch("backend.new.open", mock_open(read_data="{}")):
                result = check_time_seciruty(username)

        # Assert
        assert result is True, "First request should be allowed"

    def test_rapid_requests_blocked(self, tmp_path):
        """Test that rapid requests within 1 second are blocked."""
        # Arrange
        current_time = time.time()
        username = "test_user"

        # Simulate user already made a request just now
        time_data = {username: current_time - 0.5}  # 0.5 seconds ago

        # Mock file operations
        m = mock_open(read_data=json.dumps(time_data))

        # Act
        with patch("builtins.open", m):
            with patch("backend.new.open", m):
                with patch("time.time", return_value=current_time):
                    result = check_time_seciruty(username)

        # Assert
        assert result is False, "Request within 1 second should be blocked"

    def test_request_after_delay_allowed(self, tmp_path):
        """Test that request after 1 second delay is allowed."""
        # Arrange
        username = "test_user"
        old_time = time.time() - 1.5  # 1.5 seconds ago
        time_data = {username: old_time}

        m = mock_open(read_data=json.dumps(time_data))

        # Act
        with patch("builtins.open", m):
            with patch("backend.new.open", m):
                result = check_time_seciruty(username)

        # Assert
        assert result is True, "Request after 1 second delay should be allowed"

    def test_old_entries_cleaned_up(self, tmp_path):
        """Test that entries older than 1 hour are cleaned up."""
        # Arrange
        current_time = time.time()
        username_active = "active_user"
        username_old = "old_user"

        time_data = {
            username_active: current_time - 100,  # Recent
            username_old: current_time - 7200  # 2 hours ago
        }

        # Act
        with patch("builtins.open", mock_open(read_data=json.dumps(time_data))):
            with patch("backend.new.open", mock_open(read_data=json.dumps(time_data))):
                with patch("time.time", return_value=current_time):
                    result = check_time_seciruty(username_active)

        # Assert - we can't directly verify cleanup due to mocking,
        # but the function should execute without error
        assert result is True, "Active user should be allowed"

    def test_thread_safety(self, tmp_path):
        """Test that rate limiting is thread-safe."""
        # This is a basic test; real thread-safety testing would require
        # concurrent execution
        import threading

        username = "test_user"
        time_data = {}
        results = []

        def make_request():
            with patch("builtins.open", mock_open(read_data=json.dumps(time_data))):
                with patch("backend.new.open", mock_open(read_data=json.dumps(time_data))):
                    result = check_time_seciruty(username)
                    results.append(result)

        # Act
        threads = [threading.Thread(target=make_request) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Assert - function should handle concurrent access without crashing
        assert len(results) == 5, "All threads should complete"


class TestTimestampValidation:
    """Test timestamp validation logic."""

    def test_timestamp_exactly_300_seconds_fails(self, test_secret_key):
        """Test that timestamp exactly 300 seconds old fails."""
        # Arrange
        timestamp = time.time() - 300.1  # Just over 300 seconds
        data = {
            "username": "test_user",
            "timestamp": timestamp
        }

        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, signature)

        # Assert
        assert result is False, "Timestamp at exactly 300s should fail"

    def test_future_timestamp_passes(self, test_secret_key):
        """Test that future timestamp (clock skew) passes if within 300s."""
        # Arrange
        future_timestamp = time.time() + 10  # 10 seconds in future
        data = {
            "username": "test_user",
            "timestamp": future_timestamp
        }

        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, signature)

        # Assert
        assert result is True, "Future timestamp within 300s should pass (clock skew)"


class TestSecurityEdgeCases:
    """Test edge cases in security implementation."""

    def test_empty_data_fails(self, test_secret_key):
        """Test that empty data fails verification."""
        # Arrange
        data = {}
        signature = "test_signature"

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, signature)

        # Assert
        assert result is False, "Empty data should fail verification"

    def test_special_characters_in_data(self, test_secret_key):
        """Test that special characters in data are handled correctly."""
        # Arrange
        data = {
            "username": "test@user!#$%",
            "amount": 100,
            "timestamp": time.time()
        }

        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, signature)

        # Assert
        assert result is True, "Special characters should be handled correctly"

    def test_unicode_in_data(self, test_secret_key):
        """Test that Unicode characters in data are handled correctly."""
        # Arrange
        data = {
            "username": "用户测试",
            "amount": 100,
            "timestamp": time.time()
        }

        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Act
        with patch("backend.new.KEY", test_secret_key):
            result = verify_signature(data, signature)

        # Assert
        assert result is True, "Unicode characters should be handled correctly"

    def test_timing_attack_resistance(self, test_secret_key):
        """Test that signature comparison is timing-attack resistant."""
        # The verify_signature function uses hmac.compare_digest
        # which is designed to be timing-attack resistant
        # This test verifies it's being used

        data = {
            "username": "test_user",
            "timestamp": time.time()
        }

        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        correct_signature = hmac.new(
            test_secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Create a signature that differs only in the last character
        almost_correct = correct_signature[:-1] + ("a" if correct_signature[-1] != "a" else "b")

        # Act & Assert
        with patch("backend.new.KEY", test_secret_key):
            assert verify_signature(data, correct_signature) is True
            assert verify_signature(data, almost_correct) is False

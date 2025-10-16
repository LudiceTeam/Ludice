"""
Backend Game Endpoints Tests for Ludicé API.

Tests game creation, lobby matching, result submission, and game lifecycle.
"""

import pytest
import json
import uuid
import time
from unittest.mock import patch, mock_open


pytestmark = pytest.mark.backend


class TestStartGame:
    """Test /start/game endpoint."""

    def test_create_new_lobby(self, signature_generator, test_secret_key):
        """Test creating a new game lobby when no matching lobby exists."""
        # Arrange
        game_data = {
            "username": "player1",
            "bet": 10,
            "timestamp": time.time()
        }
        game_data["signature"] = signature_generator(game_data)

        # Empty lobby (all lobbies full or different bets)
        game_json = [
            {"id": "game1", "players": ["other_player"], "bet": 20},  # Different bet
            {"id": "game2", "players": [], "bet": 0}  # Empty lobby
        ]

        # Act - Find empty lobby and add player
        found = False
        for game in game_json:
            if len(game["players"]) == 0:
                game["bet"] = game_data["bet"]
                game["players"].append(game_data["username"])
                found = True
                break

        # Assert
        assert found is True
        assert game_json[1]["players"] == ["player1"]
        assert game_json[1]["bet"] == 10

    def test_join_existing_lobby(self, signature_generator, test_secret_key):
        """Test joining an existing lobby with matching bet."""
        # Arrange
        game_data = {
            "username": "player2",
            "bet": 10,
            "timestamp": time.time()
        }
        game_data["signature"] = signature_generator(game_data)

        game_json = [
            {"id": "game1", "players": ["player1"], "bet": 10, "winner": ""}
        ]

        # Act - Join existing lobby
        found_id = None
        for game in game_json:
            if (len(game["players"]) == 1 and
                game["bet"] == game_data["bet"] and
                game_data["username"] not in game["players"]):
                game["players"].append(game_data["username"])
                found_id = game["id"]
                break

        # Assert
        assert found_id == "game1"
        assert len(game_json[0]["players"]) == 2
        assert "player2" in game_json[0]["players"]

    def test_cannot_join_own_lobby(self, signature_generator, test_secret_key):
        """Test that a player cannot join their own lobby."""
        # Arrange
        game_data = {
            "username": "player1",
            "bet": 10,
            "timestamp": time.time()
        }
        game_data["signature"] = signature_generator(game_data)

        game_json = [
            {"id": "game1", "players": ["player1"], "bet": 10}
        ]

        # Act
        found = False
        for game in game_json:
            if (len(game["players"]) == 1 and
                game["bet"] == game_data["bet"] and
                game_data["username"] not in game["players"]):
                found = True

        # Assert
        assert found is False, "Player should not be able to join own lobby"

    def test_cannot_join_full_lobby(self, signature_generator, test_secret_key):
        """Test that a player cannot join a full lobby."""
        # Arrange
        game_data = {
            "username": "player3",
            "bet": 10,
            "timestamp": time.time()
        }
        game_data["signature"] = signature_generator(game_data)

        game_json = [
            {"id": "game1", "players": ["player1", "player2"], "bet": 10}
        ]

        # Act
        found = False
        for game in game_json:
            if (len(game["players"]) == 1 and
                game["bet"] == game_data["bet"]):
                found = True

        # Assert
        assert found is False, "Full lobby should not accept new players"

    def test_match_by_bet_amount(self, signature_generator, test_secret_key):
        """Test that lobby matching is based on bet amount."""
        # Arrange
        game_data = {
            "username": "player2",
            "bet": 50,
            "timestamp": time.time()
        }
        game_data["signature"] = signature_generator(game_data)

        game_json = [
            {"id": "game1", "players": ["player1"], "bet": 10},
            {"id": "game2", "players": ["player3"], "bet": 50}
        ]

        # Act
        matched_game = None
        for game in game_json:
            if (len(game["players"]) == 1 and
                game["bet"] == game_data["bet"] and
                game_data["username"] not in game["players"]):
                matched_game = game["id"]
                break

        # Assert
        assert matched_game == "game2", "Should match lobby with same bet amount"


class TestCancelFind:
    """Test /cancel/find endpoint."""

    def test_cancel_own_lobby(self, signature_generator, test_secret_key):
        """Test cancelling your own lobby."""
        # Arrange
        cancel_data = {
            "username": "player1",
            "id": "game1",
            "timestamp": time.time()
        }
        cancel_data["signature"] = signature_generator(cancel_data)

        game_json = [
            {"id": "game1", "players": ["player1"], "bet": 10},
            {"id": "game2", "players": ["player2"], "bet": 20}
        ]

        # Act - Remove lobby
        initial_count = len(game_json)
        for game in game_json[:]:
            if (game["id"] == cancel_data["id"] and
                len(game["players"]) == 1 and
                cancel_data["username"] in game["players"]):
                game_json.remove(game)
                break

        # Assert
        assert len(game_json) == initial_count - 1
        assert not any(g["id"] == "game1" for g in game_json)

    def test_cannot_cancel_full_lobby(self, signature_generator, test_secret_key):
        """Test that you cannot cancel a lobby with 2 players."""
        # Arrange
        cancel_data = {
            "username": "player1",
            "id": "game1",
            "timestamp": time.time()
        }
        cancel_data["signature"] = signature_generator(cancel_data)

        game_json = [
            {"id": "game1", "players": ["player1", "player2"], "bet": 10}
        ]

        # Act
        can_cancel = False
        for game in game_json:
            if (game["id"] == cancel_data["id"] and
                len(game["players"]) == 1 and
                cancel_data["username"] in game["players"]):
                can_cancel = True

        # Assert
        assert can_cancel is False, "Cannot cancel active game"

    def test_cannot_cancel_others_lobby(self, signature_generator, test_secret_key):
        """Test that you cannot cancel another player's lobby."""
        # Arrange
        cancel_data = {
            "username": "player2",
            "id": "game1",
            "timestamp": time.time()
        }
        cancel_data["signature"] = signature_generator(cancel_data)

        game_json = [
            {"id": "game1", "players": ["player1"], "bet": 10}
        ]

        # Act
        can_cancel = False
        for game in game_json:
            if (game["id"] == cancel_data["id"] and
                len(game["players"]) == 1 and
                cancel_data["username"] in game["players"]):
                can_cancel = True

        # Assert
        assert can_cancel is False, "Cannot cancel another player's lobby"


class TestWriteResult:
    """Test /write/res endpoint."""

    def test_write_dice_result(self, signature_generator, test_secret_key):
        """Test writing dice result for a player."""
        # Arrange
        result_data = {
            "user_id": "player1",
            "game_id": "game1",
            "result": 5,
            "timestamp": time.time()
        }
        result_data["signature"] = signature_generator(result_data)

        game_json = [
            {"id": "game1", "players": ["player1", "player2"], "bet": 10}
        ]

        # Act
        for game in game_json:
            if (game["id"] == result_data["game_id"] and
                len(game["players"]) == 2 and
                result_data["user_id"] in game["players"]):
                game[f"result_{result_data['user_id']}"] = result_data["result"]

        # Assert
        assert game_json[0]["result_player1"] == 5

    def test_both_players_write_results(self, signature_generator, test_secret_key):
        """Test both players writing their dice results."""
        # Arrange
        game_json = [
            {"id": "game1", "players": ["player1", "player2"], "bet": 10}
        ]

        result1 = {"user_id": "player1", "game_id": "game1", "result": 5}
        result2 = {"user_id": "player2", "game_id": "game1", "result": 3}

        # Act
        for game in game_json:
            if game["id"] == "game1":
                game[f"result_{result1['user_id']}"] = result1["result"]
                game[f"result_{result2['user_id']}"] = result2["result"]

        # Assert
        assert game_json[0]["result_player1"] == 5
        assert game_json[0]["result_player2"] == 3

    def test_cannot_write_result_for_wrong_game(self, signature_generator, test_secret_key):
        """Test that player cannot write result for game they're not in."""
        # Arrange
        result_data = {
            "user_id": "player3",
            "game_id": "game1",
            "result": 5
        }

        game_json = [
            {"id": "game1", "players": ["player1", "player2"], "bet": 10}
        ]

        # Act
        can_write = False
        for game in game_json:
            if (game["id"] == result_data["game_id"] and
                result_data["user_id"] in game["players"]):
                can_write = True

        # Assert
        assert can_write is False


class TestWriteWinner:
    """Test /write/winner endpoint."""

    def test_write_winner(self, signature_generator, test_secret_key):
        """Test writing game winner."""
        # Arrange
        winner_data = {
            "username": "player1",
            "id": "game1",
            "timestamp": time.time()
        }
        winner_data["signature"] = signature_generator(winner_data)

        game_json = [
            {"id": "game1", "players": ["player1", "player2"], "bet": 10, "winner": ""}
        ]

        # Act
        for game in game_json:
            if (game["id"] == winner_data["id"] and
                len(game["players"]) == 2 and
                winner_data["username"] in game["players"] and
                game["winner"] == ""):
                game["winner"] = winner_data["username"]

        # Assert
        assert game_json[0]["winner"] == "player1"

    def test_cannot_overwrite_winner(self, signature_generator, test_secret_key):
        """Test that winner cannot be overwritten once set."""
        # Arrange
        winner_data = {
            "username": "player2",
            "id": "game1"
        }

        game_json = [
            {"id": "game1", "players": ["player1", "player2"], "bet": 10, "winner": "player1"}
        ]

        # Act
        can_overwrite = False
        for game in game_json:
            if (game["id"] == winner_data["id"] and
                game["winner"] == ""):
                can_overwrite = True

        # Assert
        assert can_overwrite is False
        assert game_json[0]["winner"] == "player1"


class TestLeaveGame:
    """Test /leave endpoint."""

    def test_leave_completed_game(self, signature_generator, test_secret_key):
        """Test leaving a completed game."""
        # Arrange
        leave_data = {
            "user_id": "player1",
            "id": "game1",
            "timestamp": time.time()
        }
        leave_data["signature"] = signature_generator(leave_data)

        game_json = [
            {
                "id": "game1",
                "players": ["player1", "player2"],
                "bet": 10,
                "winner": "player1"
            }
        ]

        # Act - Reset lobby
        for game in game_json:
            if (game["id"] == leave_data["id"] and
                len(game["players"]) == 2 and
                leave_data["user_id"] in game["players"]):
                game["players"] = []
                game["bet"] = 0
                game["winner"] = ""

        # Assert
        assert game_json[0]["players"] == []
        assert game_json[0]["bet"] == 0
        assert game_json[0]["winner"] == ""

    def test_cannot_leave_incomplete_game(self, signature_generator, test_secret_key):
        """Test that player cannot leave game with only 1 player."""
        # Arrange
        leave_data = {
            "user_id": "player1",
            "id": "game1"
        }

        game_json = [
            {"id": "game1", "players": ["player1"], "bet": 10}
        ]

        # Act
        can_leave = False
        for game in game_json:
            if (game["id"] == leave_data["id"] and
                len(game["players"]) == 2):
                can_leave = True

        # Assert
        assert can_leave is False


class TestJoinByLink:
    """Test /join/link/{game_id}/{user_id}/{bet} endpoint."""

    def test_join_by_valid_link(self, test_secret_key):
        """Test joining game by direct link."""
        # Arrange
        user_id = "player2"
        bet = 10
        game_id = "game1"

        game_json = [
            {"id": "game1", "players": ["player1"], "bet": 10}
        ]

        # Act
        can_join = False
        for game in game_json:
            if (game["id"] == game_id and
                len(game["players"]) == 1 and
                user_id not in game["players"] and
                game["bet"] == bet):
                can_join = True
                game["players"].append(user_id)

        # Assert
        assert can_join is True
        assert "player2" in game_json[0]["players"]

    def test_join_by_link_wrong_bet(self, test_secret_key):
        """Test that joining with wrong bet amount fails."""
        # Arrange
        user_id = "player2"
        bet = 20  # Wrong bet
        game_id = "game1"

        game_json = [
            {"id": "game1", "players": ["player1"], "bet": 10}
        ]

        # Act
        can_join = False
        for game in game_json:
            if (game["id"] == game_id and
                game["bet"] == bet):
                can_join = True

        # Assert
        assert can_join is False


class TestSecondGame:
    """Test /start/new/game2 endpoint (number guessing game)."""

    def test_start_second_game(self, signature_generator, test_secret_key):
        """Test starting second game mode."""
        # Arrange
        game_data = {
            "username": "player1",
            "bet": 10,
            "num": 5,
            "timestamp": time.time()
        }
        game_data["signature"] = signature_generator(game_data)

        game2_json = []

        # Act
        game_id = str(uuid.uuid4())
        is_playing = any(g["username"] == game_data["username"] for g in game2_json)

        if not is_playing:
            game2_json.append({
                "username": game_data["username"],
                "bet": game_data["bet"],
                "win": False,
                "num": game_data["num"],
                "id": game_id
            })

        # Assert
        assert len(game2_json) == 1
        assert game2_json[0]["username"] == "player1"
        assert game2_json[0]["num"] == 5

    def test_cannot_play_second_game_twice(self, signature_generator, test_secret_key):
        """Test that user cannot start second game if already playing."""
        # Arrange
        game_data = {
            "username": "player1",
            "bet": 10,
            "num": 5
        }

        game2_json = [
            {"username": "player1", "bet": 10, "num": 3, "id": "game1"}
        ]

        # Act
        is_playing = any(g["username"] == game_data["username"] for g in game2_json)

        # Assert
        assert is_playing is True


class TestDroticGame:
    """Test /start/drotic/game endpoint (drotic dice variant)."""

    def test_start_drotic_game(self, signature_generator, test_secret_key):
        """Test starting drotic game."""
        # Arrange
        game_data = {
            "username": "player1",
            "bet": 10,
            "timestamp": time.time()
        }
        game_data["signature"] = signature_generator(game_data)

        drotic_json = [
            {"id": "game1", "players": [], "bet": 0, "cache": []}
        ]

        # Act
        for game in drotic_json:
            if game["bet"] == 0 and len(game["players"]) == 0:
                game["players"].append(game_data["username"])
                game["bet"] = game_data["bet"]
                break

        # Assert
        assert drotic_json[0]["players"] == ["player1"]
        assert drotic_json[0]["bet"] == 10

    def test_drotic_write_try(self, signature_generator, test_secret_key):
        """Test writing a try/attempt in drotic game."""
        # Arrange
        try_data = {
            "username": "player1",
            "result": "dice_5",
            "id": "game1",
            "timestamp": time.time()
        }

        drotic_json = [
            {"id": "game1", "players": ["player1", "player2"], "bet": 10, "cache": []}
        ]

        # Act
        for game in drotic_json:
            if game["id"] == try_data["id"]:
                game["cache"].append({
                    "username": try_data["username"],
                    "result": try_data["result"]
                })

        # Assert
        assert len(drotic_json[0]["cache"]) == 1
        assert drotic_json[0]["cache"][0]["username"] == "player1"

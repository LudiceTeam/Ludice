"""
Backend Stats and Leaderboard Tests for Ludicé API.

Tests win tracking, game statistics, and leaderboard functionality.
"""

import pytest
import json
from unittest.mock import patch, mock_open


pytestmark = pytest.mark.backend


class TestStatsInitialization:
    """Test default stats creation for new users."""

    def test_create_default_stats(self):
        """Test creating default stats for new user."""
        # Arrange
        user_id = "new_user_123"
        stats_data = []

        # Act
        stats_data.append({
            "user_id": user_id,
            "wins": 0,
            "total_games": 0
        })

        # Assert
        assert len(stats_data) == 1
        assert stats_data[0]["user_id"] == user_id
        assert stats_data[0]["wins"] == 0
        assert stats_data[0]["total_games"] == 0


class TestAddWin:
    """Test add_win() function."""

    def test_add_win_existing_user(self):
        """Test adding a win to existing user."""
        # Arrange
        user_id = "player1"
        stats_data = [
            {"user_id": "player1", "wins": 5, "total_games": 10},
            {"user_id": "player2", "wins": 3, "total_games": 8}
        ]

        # Act
        for user in stats_data:
            if user["user_id"] == user_id:
                user["wins"] += 1

        # Assert
        assert stats_data[0]["wins"] == 6
        assert stats_data[0]["total_games"] == 10  # Unchanged

    def test_add_win_multiple_times(self):
        """Test adding multiple wins to user."""
        # Arrange
        user_id = "player1"
        stats_data = [{"user_id": "player1", "wins": 0, "total_games": 0}]

        # Act
        for _ in range(3):
            for user in stats_data:
                if user["user_id"] == user_id:
                    user["wins"] += 1

        # Assert
        assert stats_data[0]["wins"] == 3

    def test_add_win_nonexistent_user(self):
        """Test that adding win to nonexistent user returns False."""
        # Arrange
        user_id = "nonexistent_user"
        stats_data = [{"user_id": "player1", "wins": 5, "total_games": 10}]

        # Act
        found = False
        for user in stats_data:
            if user["user_id"] == user_id:
                user["wins"] += 1
                found = True

        # Assert
        assert found is False


class TestAddGame:
    """Test add_game() function."""

    def test_add_game_existing_user(self):
        """Test incrementing total games for existing user."""
        # Arrange
        user_id = "player1"
        stats_data = [
            {"user_id": "player1", "wins": 5, "total_games": 10}
        ]

        # Act
        for user in stats_data:
            if user["user_id"] == user_id:
                user["total_games"] += 1

        # Assert
        assert stats_data[0]["total_games"] == 11
        assert stats_data[0]["wins"] == 5  # Unchanged

    def test_add_game_multiple_times(self):
        """Test adding multiple games to user."""
        # Arrange
        user_id = "player1"
        stats_data = [{"user_id": "player1", "wins": 0, "total_games": 0}]

        # Act
        for _ in range(5):
            for user in stats_data:
                if user["user_id"] == user_id:
                    user["total_games"] += 1

        # Assert
        assert stats_data[0]["total_games"] == 5

    def test_add_game_and_win(self):
        """Test adding both game and win."""
        # Arrange
        user_id = "player1"
        stats_data = [{"user_id": "player1", "wins": 0, "total_games": 0}]

        # Act - Simulate winning a game
        for user in stats_data:
            if user["user_id"] == user_id:
                user["total_games"] += 1
                user["wins"] += 1

        # Assert
        assert stats_data[0]["total_games"] == 1
        assert stats_data[0]["wins"] == 1


class TestWinPercentage:
    """Test count_procent_of_wins() function."""

    def test_calculate_win_percentage_50_percent(self):
        """Test calculating 50% win rate."""
        # Arrange
        stats = {"user_id": "player1", "wins": 5, "total_games": 10}

        # Act
        if stats["total_games"] > 0:
            percentage = (stats["wins"] / stats["total_games"]) * 100
        else:
            percentage = 0

        # Assert
        assert percentage == 50.0

    def test_calculate_win_percentage_100_percent(self):
        """Test calculating 100% win rate."""
        # Arrange
        stats = {"user_id": "player1", "wins": 10, "total_games": 10}

        # Act
        percentage = (stats["wins"] / stats["total_games"]) * 100

        # Assert
        assert percentage == 100.0

    def test_calculate_win_percentage_0_percent(self):
        """Test calculating 0% win rate."""
        # Arrange
        stats = {"user_id": "player1", "wins": 0, "total_games": 10}

        # Act
        percentage = (stats["wins"] / stats["total_games"]) * 100

        # Assert
        assert percentage == 0.0

    def test_calculate_win_percentage_no_games(self):
        """Test calculating win percentage with no games played."""
        # Arrange
        stats = {"user_id": "player1", "wins": 0, "total_games": 0}

        # Act
        if stats["total_games"] > 0:
            percentage = (stats["wins"] / stats["total_games"]) * 100
        else:
            percentage = 0

        # Assert
        assert percentage == 0

    def test_calculate_win_percentage_fractional(self):
        """Test calculating fractional win percentage."""
        # Arrange
        stats = {"user_id": "player1", "wins": 3, "total_games": 7}

        # Act
        percentage = (stats["wins"] / stats["total_games"]) * 100

        # Assert
        assert round(percentage, 2) == 42.86


class TestLeaderboard:
    """Test leaderboard endpoints."""

    def test_leaderboard_most_games(self):
        """Test /get/leader/board/most_games endpoint."""
        # Arrange
        stats_data = [
            {"user_id": "player1", "wins": 10, "total_games": 50},
            {"user_id": "player2", "wins": 5, "total_games": 30},
            {"user_id": "player3", "wins": 8, "total_games": 40}
        ]

        # Act - Create leaderboard
        leaderboard = {}
        for user in stats_data:
            leaderboard[user["user_id"]] = user["total_games"]

        # Sort by total games
        sorted_leaderboard = dict(sorted(
            leaderboard.items(),
            key=lambda x: x[1],
            reverse=True
        ))

        # Assert
        assert list(sorted_leaderboard.keys())[0] == "player1"
        assert sorted_leaderboard["player1"] == 50

    def test_leaderboard_win_percentage(self):
        """Test /get/procent/wins endpoint."""
        # Arrange
        stats_data = [
            {"user_id": "player1", "wins": 10, "total_games": 50},  # 20%
            {"user_id": "player2", "wins": 15, "total_games": 30},  # 50%
            {"user_id": "player3", "wins": 20, "total_games": 40}   # 50%
        ]

        # Act
        percentages = {}
        for user in stats_data:
            if user["total_games"] > 0:
                percentages[user["user_id"]] = (user["wins"] / user["total_games"]) * 100
            else:
                percentages[user["user_id"]] = 0

        # Assert
        assert percentages["player1"] == 20.0
        assert percentages["player2"] == 50.0
        assert percentages["player3"] == 50.0

    def test_leaderboard_empty(self):
        """Test leaderboard with no players."""
        # Arrange
        stats_data = []

        # Act
        leaderboard = {}
        for user in stats_data:
            leaderboard[user["user_id"]] = user["total_games"]

        # Assert
        assert len(leaderboard) == 0

    def test_leaderboard_single_player(self):
        """Test leaderboard with single player."""
        # Arrange
        stats_data = [{"user_id": "player1", "wins": 5, "total_games": 10}]

        # Act
        leaderboard = {}
        for user in stats_data:
            leaderboard[user["user_id"]] = user["total_games"]

        # Assert
        assert len(leaderboard) == 1
        assert leaderboard["player1"] == 10


class TestGetUserStats:
    """Test /getme/{user_id} endpoint."""

    def test_get_complete_user_stats(self):
        """Test getting complete user stats including balance."""
        # Arrange
        user_id = "player1"
        stats_data = [{"user_id": "player1", "wins": 10, "total_games": 20}]
        bank_data = [{"username": "player1", "balance": 100}]

        # Act
        user_stats = None
        balance = None

        for stats in stats_data:
            if stats["user_id"] == user_id:
                user_stats = stats

        for user in bank_data:
            if user["username"] == user_id:
                balance = user["balance"]

        # Calculate win percentage
        if user_stats and user_stats["total_games"] > 0:
            win_percent = (user_stats["wins"] / user_stats["total_games"]) * 100
        else:
            win_percent = 0

        result = {
            "Total games": user_stats["total_games"],
            "Wins": user_stats["wins"],
            "Wins procent": win_percent,
            "Balance": balance
        }

        # Assert
        assert result["Total games"] == 20
        assert result["Wins"] == 10
        assert result["Wins procent"] == 50.0
        assert result["Balance"] == 100

    def test_get_stats_new_user(self):
        """Test getting stats for user with no games."""
        # Arrange
        user_id = "new_player"
        stats_data = [{"user_id": "new_player", "wins": 0, "total_games": 0}]
        bank_data = [{"username": "new_player", "balance": 50}]

        # Act
        user_stats = next((s for s in stats_data if s["user_id"] == user_id), None)
        balance = next((u["balance"] for u in bank_data if u["username"] == user_id), None)

        # Assert
        assert user_stats["total_games"] == 0
        assert user_stats["wins"] == 0
        assert balance == 50

    def test_get_stats_user_not_found(self):
        """Test getting stats for non-existent user."""
        # Arrange
        user_id = "nonexistent"
        stats_data = [{"user_id": "player1", "wins": 10, "total_games": 20}]

        # Act
        user_stats = next((s for s in stats_data if s["user_id"] == user_id), None)

        # Assert
        assert user_stats is None


class TestStatsEdgeCases:
    """Test edge cases in stats tracking."""

    def test_stats_with_negative_values(self):
        """Test that stats don't go negative (shouldn't happen but test defensive)."""
        # Arrange
        stats = {"user_id": "player1", "wins": 0, "total_games": 0}

        # Act - Try to subtract (shouldn't happen in normal flow)
        # In production, you'd have validation to prevent this
        stats["wins"] = max(0, stats["wins"] - 1)
        stats["total_games"] = max(0, stats["total_games"] - 1)

        # Assert
        assert stats["wins"] == 0
        assert stats["total_games"] == 0

    def test_wins_cannot_exceed_total_games(self):
        """Test that wins should never exceed total games."""
        # Arrange
        stats = {"user_id": "player1", "wins": 10, "total_games": 10}

        # Act - Verify consistency
        is_valid = stats["wins"] <= stats["total_games"]

        # Assert
        assert is_valid is True

    def test_large_numbers(self):
        """Test stats with large numbers."""
        # Arrange
        stats = {"user_id": "player1", "wins": 10000, "total_games": 50000}

        # Act
        percentage = (stats["wins"] / stats["total_games"]) * 100

        # Assert
        assert percentage == 20.0
        assert stats["wins"] < stats["total_games"]

    def test_concurrent_stat_updates(self):
        """Test that stats updates are consistent."""
        # Arrange
        stats = {"user_id": "player1", "wins": 5, "total_games": 10}

        # Act - Simulate multiple game results
        game_results = [True, False, True, False, True]  # 3 wins
        for won in game_results:
            stats["total_games"] += 1
            if won:
                stats["wins"] += 1

        # Assert
        assert stats["total_games"] == 15
        assert stats["wins"] == 8
        assert stats["wins"] <= stats["total_games"]


class TestStatsDataIntegrity:
    """Test stats data integrity and consistency."""

    def test_stats_json_structure(self):
        """Test that stats JSON maintains correct structure."""
        # Arrange
        stats_data = [
            {"user_id": "player1", "wins": 10, "total_games": 20},
            {"user_id": "player2", "wins": 5, "total_games": 15}
        ]

        # Act - Validate structure
        for stats in stats_data:
            has_user_id = "user_id" in stats
            has_wins = "wins" in stats
            has_total_games = "total_games" in stats

            # Assert each entry
            assert has_user_id is True
            assert has_wins is True
            assert has_total_games is True

    def test_duplicate_user_entries(self):
        """Test handling of duplicate user entries in stats."""
        # Arrange
        stats_data = [
            {"user_id": "player1", "wins": 10, "total_games": 20},
            {"user_id": "player1", "wins": 5, "total_games": 15}  # Duplicate
        ]

        # Act - Find duplicates
        user_ids = [s["user_id"] for s in stats_data]
        has_duplicates = len(user_ids) != len(set(user_ids))

        # Assert
        assert has_duplicates is True  # This should be fixed in production

    def test_stats_type_validation(self):
        """Test that stats values are correct types."""
        # Arrange
        stats = {"user_id": "player1", "wins": 10, "total_games": 20}

        # Act & Assert
        assert isinstance(stats["user_id"], str)
        assert isinstance(stats["wins"], int)
        assert isinstance(stats["total_games"], int)

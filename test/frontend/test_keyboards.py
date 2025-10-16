"""
Frontend Keyboard Tests for Ludicé Telegram Bot.

Tests keyboard layouts, button configurations, and inline keyboard structures.
"""

import pytest
from aiogram.types import (
    ReplyKeyboardMarkup, InlineKeyboardMarkup,
    KeyboardButton, InlineKeyboardButton
)


pytestmark = pytest.mark.frontend


class TestStartKeyboard:
    """Test start_kb (main menu keyboard)."""

    def test_start_keyboard_exists(self):
        """Test that start keyboard is defined."""
        # Arrange & Act
        from frontend.keyboard.start import start_kb

        # Assert
        assert start_kb is not None
        assert isinstance(start_kb, ReplyKeyboardMarkup)

    def test_start_keyboard_has_buttons(self):
        """Test that start keyboard has buttons."""
        # Arrange & Act
        from frontend.keyboard.start import start_kb

        # Assert
        assert len(start_kb.keyboard) > 0

    def test_start_keyboard_includes_roll_button(self):
        """Test that start keyboard includes 'Roll' button."""
        # Arrange
        from frontend.keyboard.start import start_kb

        # Act
        all_buttons = [btn.text for row in start_kb.keyboard for btn in row]

        # Assert
        assert any("Roll" in btn or "🎲" in btn for btn in all_buttons)

    def test_start_keyboard_includes_top_up_button(self):
        """Test that start keyboard includes 'Top up' button."""
        # Arrange
        from frontend.keyboard.start import start_kb

        # Act
        all_buttons = [btn.text for row in start_kb.keyboard for btn in row]

        # Assert
        assert any("Top up" in btn or "🔝" in btn for btn in all_buttons)

    def test_start_keyboard_includes_profile_button(self):
        """Test that start keyboard includes 'Profile' button."""
        # Arrange
        from frontend.keyboard.start import start_kb

        # Act
        all_buttons = [btn.text for row in start_kb.keyboard for btn in row]

        # Assert
        assert any("Profile" in btn or "👤" in btn for btn in all_buttons)

    def test_start_keyboard_includes_help_button(self):
        """Test that start keyboard includes 'Help' button."""
        # Arrange
        from frontend.keyboard.start import start_kb

        # Act
        all_buttons = [btn.text for row in start_kb.keyboard for btn in row]

        # Assert
        assert any("Help" in btn or "❓" in btn for btn in all_buttons)

    def test_start_keyboard_resize_enabled(self):
        """Test that start keyboard has resize enabled."""
        # Arrange & Act
        from frontend.keyboard.start import start_kb

        # Assert
        assert start_kb.resize_keyboard is True

    def test_start_keyboard_one_time(self):
        """Test that start keyboard is one-time."""
        # Arrange & Act
        from frontend.keyboard.start import start_kb

        # Assert
        assert start_kb.one_time_keyboard is True


class TestStarsKeyboard:
    """Test keyboard_stars (payment options)."""

    def test_stars_keyboard_exists(self):
        """Test that stars keyboard is defined."""
        # Arrange & Act
        from frontend.keyboard.start import keyboard_stars

        # Assert
        assert keyboard_stars is not None
        assert isinstance(keyboard_stars, InlineKeyboardMarkup)

    def test_stars_keyboard_has_buttons(self):
        """Test that stars keyboard has inline buttons."""
        # Arrange & Act
        from frontend.keyboard.start import keyboard_stars

        # Assert
        assert len(keyboard_stars.inline_keyboard) > 0

    def test_stars_keyboard_includes_15_stars(self):
        """Test that keyboard includes 15 stars option."""
        # Arrange
        from frontend.keyboard.start import keyboard_stars

        # Act
        all_buttons = [
            btn.text
            for row in keyboard_stars.inline_keyboard
            for btn in row
        ]

        # Assert
        assert any("15" in btn for btn in all_buttons)

    def test_stars_keyboard_includes_50_stars(self):
        """Test that keyboard includes 50 stars option."""
        # Arrange
        from frontend.keyboard.start import keyboard_stars

        # Act
        all_buttons = [
            btn.text
            for row in keyboard_stars.inline_keyboard
            for btn in row
        ]

        # Assert
        assert any("50" in btn for btn in all_buttons)

    def test_stars_keyboard_includes_100_stars(self):
        """Test that keyboard includes 100 stars option."""
        # Arrange
        from frontend.keyboard.start import keyboard_stars

        # Act
        all_buttons = [
            btn.text
            for row in keyboard_stars.inline_keyboard
            for btn in row
        ]

        # Assert
        assert any("100" in btn for btn in all_buttons)

    def test_stars_keyboard_includes_1000_stars(self):
        """Test that keyboard includes 1000 stars option."""
        # Arrange
        from frontend.keyboard.start import keyboard_stars

        # Act
        all_buttons = [
            btn.text
            for row in keyboard_stars.inline_keyboard
            for btn in row
        ]

        # Assert
        assert any("1000" in btn or "1 000" in btn for btn in all_buttons)

    def test_stars_keyboard_callback_data(self):
        """Test that stars buttons have correct callback data."""
        # Arrange
        from frontend.keyboard.start import keyboard_stars

        # Act
        all_callback_data = [
            btn.callback_data
            for row in keyboard_stars.inline_keyboard
            for btn in row
        ]

        # Assert
        assert "star15" in all_callback_data
        assert "star50" in all_callback_data
        assert "star100" in all_callback_data
        assert "star1000" in all_callback_data

    def test_stars_keyboard_multiple_rows(self):
        """Test that stars keyboard has multiple rows."""
        # Arrange & Act
        from frontend.keyboard.start import keyboard_stars

        # Assert
        assert len(keyboard_stars.inline_keyboard) >= 2


class TestGameKeyboard:
    """Test game_kb (game selection keyboard)."""

    def test_game_keyboard_exists(self):
        """Test that game keyboard is defined."""
        # Arrange & Act
        from frontend.keyboard.start import game_kb

        # Assert
        assert game_kb is not None
        assert isinstance(game_kb, ReplyKeyboardMarkup)

    def test_game_keyboard_includes_dice(self):
        """Test that game keyboard includes Dice option."""
        # Arrange
        from frontend.keyboard.start import game_kb

        # Act
        all_buttons = [btn.text for row in game_kb.keyboard for btn in row]

        # Assert
        assert any("Dice" in btn or "🎲" in btn for btn in all_buttons)

    def test_game_keyboard_includes_target(self):
        """Test that game keyboard includes Target option."""
        # Arrange
        from frontend.keyboard.start import game_kb

        # Act
        all_buttons = [btn.text for row in game_kb.keyboard for btn in row]

        # Assert
        assert any("Target" in btn or "🎯" in btn for btn in all_buttons)

    def test_game_keyboard_resize_enabled(self):
        """Test that game keyboard has resize enabled."""
        # Arrange & Act
        from frontend.keyboard.start import game_kb

        # Assert
        assert game_kb.resize_keyboard is True


class TestButtonStructure:
    """Test button structure and properties."""

    def test_keyboard_button_is_text_only(self):
        """Test that regular keyboard buttons are text-only."""
        # Arrange
        from frontend.keyboard.start import start_kb

        # Act & Assert
        for row in start_kb.keyboard:
            for button in row:
                assert isinstance(button, KeyboardButton)
                assert hasattr(button, "text")

    def test_inline_button_has_callback_data(self):
        """Test that inline buttons have callback data."""
        # Arrange
        from frontend.keyboard.start import keyboard_stars

        # Act & Assert
        for row in keyboard_stars.inline_keyboard:
            for button in row:
                assert isinstance(button, InlineKeyboardButton)
                assert hasattr(button, "callback_data")
                assert button.callback_data is not None


class TestKeyboardUsability:
    """Test keyboard usability features."""

    def test_keyboards_have_input_placeholders(self):
        """Test that keyboards have input field placeholders."""
        # Arrange
        from frontend.keyboard.start import start_kb, game_kb

        # Assert
        assert start_kb.input_field_placeholder is not None
        assert game_kb.input_field_placeholder is not None

    def test_start_keyboard_placeholder_text(self):
        """Test that start keyboard has appropriate placeholder."""
        # Arrange & Act
        from frontend.keyboard.start import start_kb

        # Assert
        assert len(start_kb.input_field_placeholder) > 0


class TestKeyboardLayout:
    """Test keyboard layout organization."""

    def test_start_keyboard_has_two_rows(self):
        """Test that start keyboard is organized in 2 rows."""
        # Arrange & Act
        from frontend.keyboard.start import start_kb

        # Assert
        assert len(start_kb.keyboard) == 2

    def test_start_keyboard_row_distribution(self):
        """Test that start keyboard rows have 2 buttons each."""
        # Arrange & Act
        from frontend.keyboard.start import start_kb

        # Assert
        for row in start_kb.keyboard:
            assert len(row) == 2

    def test_game_keyboard_has_one_row(self):
        """Test that game keyboard has one row."""
        # Arrange & Act
        from frontend.keyboard.start import game_kb

        # Assert
        assert len(game_kb.keyboard) == 1

    def test_stars_keyboard_organized_in_grid(self):
        """Test that stars keyboard is organized in a grid layout."""
        # Arrange & Act
        from frontend.keyboard.start import keyboard_stars

        # Assert
        assert len(keyboard_stars.inline_keyboard) >= 3


class TestAllStarOptions:
    """Test all star payment options are available."""

    def test_all_tier_options_present(self):
        """Test that all payment tiers are present."""
        # Arrange
        from frontend.keyboard.start import keyboard_stars

        expected_tiers = [
            "star15", "star50", "star75", "star100",
            "star150", "star250", "star750", "star1000"
        ]

        # Act
        all_callback_data = [
            btn.callback_data
            for row in keyboard_stars.inline_keyboard
            for btn in row
        ]

        # Assert
        for tier in expected_tiers:
            assert tier in all_callback_data, f"{tier} should be in keyboard"

    def test_stars_display_star_emoji(self):
        """Test that star buttons display star emoji."""
        # Arrange
        from frontend.keyboard.start import keyboard_stars

        # Act
        all_button_texts = [
            btn.text
            for row in keyboard_stars.inline_keyboard
            for btn in row
        ]

        # Assert
        # Most buttons should have star emoji
        star_emoji_count = sum(1 for text in all_button_texts if "⭐" in text)
        assert star_emoji_count > 0


class TestKeyboardButtonCount:
    """Test button counts in keyboards."""

    def test_start_keyboard_has_four_buttons(self):
        """Test that start keyboard has exactly 4 buttons."""
        # Arrange
        from frontend.keyboard.start import start_kb

        # Act
        button_count = sum(len(row) for row in start_kb.keyboard)

        # Assert
        assert button_count == 4

    def test_game_keyboard_has_two_buttons(self):
        """Test that game keyboard has 2 buttons."""
        # Arrange
        from frontend.keyboard.start import game_kb

        # Act
        button_count = sum(len(row) for row in game_kb.keyboard)

        # Assert
        assert button_count == 2

    def test_stars_keyboard_has_many_options(self):
        """Test that stars keyboard has many payment options."""
        # Arrange
        from frontend.keyboard.start import keyboard_stars

        # Act
        button_count = sum(
            len(row) for row in keyboard_stars.inline_keyboard
        )

        # Assert
        assert button_count >= 8  # At least 8 payment options


class TestKeyboardImmutability:
    """Test that keyboards don't share mutable state."""

    def test_keyboards_are_independent(self):
        """Test that keyboard instances are independent."""
        # Arrange & Act
        from frontend.keyboard.start import start_kb, game_kb

        # Assert
        assert start_kb is not game_kb
        assert start_kb.keyboard is not game_kb.keyboard


class TestButtonEmojis:
    """Test that buttons include appropriate emojis."""

    def test_dice_button_has_emoji(self):
        """Test that Dice button includes dice emoji."""
        # Arrange
        from frontend.keyboard.start import game_kb

        # Act
        all_buttons = [btn.text for row in game_kb.keyboard for btn in row]
        dice_buttons = [btn for btn in all_buttons if "Dice" in btn]

        # Assert
        assert len(dice_buttons) > 0
        assert any("🎲" in btn for btn in dice_buttons)

    def test_target_button_has_emoji(self):
        """Test that Target button includes target emoji."""
        # Arrange
        from frontend.keyboard.start import game_kb

        # Act
        all_buttons = [btn.text for row in game_kb.keyboard for btn in row]
        target_buttons = [btn for btn in all_buttons if "Target" in btn]

        # Assert
        assert len(target_buttons) > 0
        assert any("🎯" in btn for btn in target_buttons)

    def test_roll_button_has_emoji(self):
        """Test that Roll button includes dice emoji."""
        # Arrange
        from frontend.keyboard.start import start_kb

        # Act
        all_buttons = [btn.text for row in start_kb.keyboard for btn in row]
        roll_buttons = [btn for btn in all_buttons if "Roll" in btn]

        # Assert
        assert len(roll_buttons) > 0
        assert any("🎲" in btn for btn in roll_buttons)

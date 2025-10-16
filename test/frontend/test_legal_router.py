"""
Frontend Legal Router Tests for Ludicé Telegram Bot.

Tests legal commands (/terms, /privacy, /gambling), callback handlers,
and terms acceptance flow.
"""

import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import CallbackQuery


pytestmark = pytest.mark.frontend


class TestLegalCommands:
    """Test legal document command handlers."""

    @pytest.mark.asyncio
    async def test_terms_command(self, mock_message):
        """Test /terms command displays Terms of Service."""
        # Arrange
        message = mock_message("/terms")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_terms

        # Act
        await cmd_terms(message)

        # Assert
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "Terms" in call_args or "terms" in call_args.lower()

    @pytest.mark.asyncio
    async def test_privacy_command(self, mock_message):
        """Test /privacy command displays Privacy Policy."""
        # Arrange
        message = mock_message("/privacy")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_privacy

        # Act
        await cmd_privacy(message)

        # Assert
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "Privacy" in call_args or "privacy" in call_args.lower()

    @pytest.mark.asyncio
    async def test_gambling_command(self, mock_message):
        """Test /gambling command displays Responsible Gambling policy."""
        # Arrange
        message = mock_message("/gambling")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_gambling

        # Act
        await cmd_gambling(message)

        # Assert
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "Gambling" in call_args or "gambling" in call_args.lower()

    @pytest.mark.asyncio
    async def test_help_command(self, mock_message):
        """Test /help command displays support information."""
        # Arrange
        message = mock_message("/help")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_support

        # Act
        await cmd_support(message)

        # Assert
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "support" in call_args.lower() or "help" in call_args.lower()

    @pytest.mark.asyncio
    async def test_support_command(self, mock_message):
        """Test /support command displays contact information."""
        # Arrange
        message = mock_message("/support")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_support

        # Act
        await cmd_support(message)

        # Assert
        message.answer.assert_called_once()

    @pytest.mark.asyncio
    async def test_fairplay_command(self, mock_message):
        """Test /fairplay command displays Fair Play policy."""
        # Arrange
        message = mock_message("/fairplay")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_fairplay

        # Act
        await cmd_fairplay(message)

        # Assert
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "Fair" in call_args or "fair" in call_args.lower()

    @pytest.mark.asyncio
    async def test_refund_command(self, mock_message):
        """Test /refund command displays refund policy."""
        # Arrange
        message = mock_message("/refund")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_refund

        # Act
        await cmd_refund(message)

        # Assert
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "refund" in call_args.lower() or "withdrawal" in call_args.lower()

    @pytest.mark.asyncio
    async def test_withdrawal_command(self, mock_message):
        """Test /withdrawal command displays withdrawal policy."""
        # Arrange
        message = mock_message("/withdrawal")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_refund

        # Act
        await cmd_refund(message)

        # Assert
        message.answer.assert_called_once()


class TestLegalCommandsIncludeKeyboards:
    """Test that legal commands include navigation keyboards."""

    @pytest.mark.asyncio
    async def test_terms_includes_keyboard(self, mock_message):
        """Test that /terms includes navigation keyboard."""
        # Arrange
        message = mock_message("/terms")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_terms

        # Act
        await cmd_terms(message)

        # Assert
        call_kwargs = message.answer.call_args[1]
        assert "reply_markup" in call_kwargs

    @pytest.mark.asyncio
    async def test_privacy_includes_keyboard(self, mock_message):
        """Test that /privacy includes navigation keyboard."""
        # Arrange
        message = mock_message("/privacy")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_privacy

        # Act
        await cmd_privacy(message)

        # Assert
        call_kwargs = message.answer.call_args[1]
        assert "reply_markup" in call_kwargs

    @pytest.mark.asyncio
    async def test_gambling_includes_keyboard(self, mock_message):
        """Test that /gambling includes navigation keyboard."""
        # Arrange
        message = mock_message("/gambling")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_gambling

        # Act
        await cmd_gambling(message)

        # Assert
        call_kwargs = message.answer.call_args[1]
        assert "reply_markup" in call_kwargs


class TestCallbackHandlers:
    """Test callback query handlers for legal document navigation."""

    @pytest.mark.asyncio
    async def test_view_terms_callback(self, mock_callback_query):
        """Test view_terms callback handler."""
        # Arrange
        callback = mock_callback_query("view_terms")
        callback.message.edit_text = AsyncMock()

        from frontend.routers.legal_router import callback_view_terms

        # Act
        await callback_view_terms(callback)

        # Assert
        callback.message.edit_text.assert_called_once()
        call_args = callback.message.edit_text.call_args[0][0]
        assert "Terms" in call_args or "terms" in call_args.lower()

    @pytest.mark.asyncio
    async def test_view_privacy_callback(self, mock_callback_query):
        """Test view_privacy callback handler."""
        # Arrange
        callback = mock_callback_query("view_privacy")
        callback.message.edit_text = AsyncMock()

        from frontend.routers.legal_router import callback_view_privacy

        # Act
        await callback_view_privacy(callback)

        # Assert
        callback.message.edit_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_view_gambling_callback(self, mock_callback_query):
        """Test view_gambling callback handler."""
        # Arrange
        callback = mock_callback_query("view_gambling")
        callback.message.edit_text = AsyncMock()

        from frontend.routers.legal_router import callback_view_gambling

        # Act
        await callback_view_gambling(callback)

        # Assert
        callback.message.edit_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_view_refunds_callback(self, mock_callback_query):
        """Test view_refunds callback handler."""
        # Arrange
        callback = mock_callback_query("view_refunds")
        callback.message.edit_text = AsyncMock()

        from frontend.routers.legal_router import callback_view_refunds

        # Act
        await callback_view_refunds(callback)

        # Assert
        callback.message.edit_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_view_fairplay_callback(self, mock_callback_query):
        """Test view_fairplay callback handler."""
        # Arrange
        callback = mock_callback_query("view_fairplay")
        callback.message.edit_text = AsyncMock()

        from frontend.routers.legal_router import callback_view_fairplay

        # Act
        await callback_view_fairplay(callback)

        # Assert
        callback.message.edit_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_view_support_callback(self, mock_callback_query):
        """Test view_support callback handler."""
        # Arrange
        callback = mock_callback_query("view_support")
        callback.message.edit_text = AsyncMock()

        from frontend.routers.legal_router import callback_view_support

        # Act
        await callback_view_support(callback)

        # Assert
        callback.message.edit_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_view_full_terms_callback(self, mock_callback_query):
        """Test view_full_terms callback handler."""
        # Arrange
        callback = mock_callback_query("view_full_terms")
        callback.message.edit_text = AsyncMock()
        callback.answer = AsyncMock()

        from frontend.routers.legal_router import callback_view_full_terms

        # Act
        await callback_view_full_terms(callback)

        # Assert
        callback.message.edit_text.assert_called_once()
        callback.answer.assert_called_once()


class TestTermsAcceptance:
    """Test terms acceptance flow."""

    @pytest.mark.asyncio
    async def test_accept_terms_callback(self, mock_callback_query, mock_fsm_context):
        """Test accepting terms."""
        # Arrange
        callback = mock_callback_query("accept_terms")
        callback.message.edit_text = AsyncMock()
        callback.answer = AsyncMock()

        from frontend.routers.legal_router import callback_accept_terms

        # Act
        await callback_accept_terms(callback, mock_fsm_context)

        # Assert
        callback.message.edit_text.assert_called_once()
        call_args = callback.message.edit_text.call_args[0][0]
        assert "Accept" in call_args or "accept" in call_args.lower()
        mock_fsm_context.clear.assert_called_once()

    @pytest.mark.asyncio
    async def test_decline_terms_callback(self, mock_callback_query, mock_fsm_context):
        """Test declining terms."""
        # Arrange
        callback = mock_callback_query("decline_terms")
        callback.message.edit_text = AsyncMock()
        callback.answer = AsyncMock()

        from frontend.routers.legal_router import callback_decline_terms

        # Act
        await callback_decline_terms(callback, mock_fsm_context)

        # Assert
        callback.message.edit_text.assert_called_once()
        call_args = callback.message.edit_text.call_args[0][0]
        assert "Decline" in call_args or "decline" in call_args.lower()
        mock_fsm_context.clear.assert_called_once()

    @pytest.mark.asyncio
    async def test_accept_terms_clears_state(self, mock_callback_query, mock_fsm_context):
        """Test that accepting terms clears FSM state."""
        # Arrange
        callback = mock_callback_query("accept_terms")
        callback.message.edit_text = AsyncMock()

        from frontend.routers.legal_router import callback_accept_terms

        # Act
        await callback_accept_terms(callback, mock_fsm_context)

        # Assert
        mock_fsm_context.clear.assert_called_once()


class TestAgeVerification:
    """Test age verification flow."""

    @pytest.mark.asyncio
    async def test_confirm_age_callback(self, mock_callback_query, mock_fsm_context):
        """Test confirming age (18+)."""
        # Arrange
        callback = mock_callback_query("confirm_age")
        callback.message.edit_text = AsyncMock()

        # Mock show_terms_acceptance
        with patch("frontend.routers.legal_router.show_terms_acceptance", new=AsyncMock()) as mock_show:
            from frontend.routers.legal_router import callback_confirm_age

            # Act
            await callback_confirm_age(callback, mock_fsm_context)

        # Assert
        callback.message.edit_text.assert_called_once()
        mock_show.assert_called_once()

    @pytest.mark.asyncio
    async def test_underage_callback(self, mock_callback_query, mock_fsm_context):
        """Test underage user response."""
        # Arrange
        callback = mock_callback_query("underage")
        callback.message.edit_text = AsyncMock()
        callback.answer = AsyncMock()

        from frontend.routers.legal_router import callback_underage

        # Act
        await callback_underage(callback, mock_fsm_context)

        # Assert
        callback.message.edit_text.assert_called_once()
        call_args = callback.message.edit_text.call_args[0][0]
        assert "18" in call_args or "underage" in call_args.lower()
        mock_fsm_context.clear.assert_called_once()


class TestHelperFunctions:
    """Test helper functions for legal router."""

    @pytest.mark.asyncio
    async def test_show_terms_acceptance(self, mock_message, mock_fsm_context):
        """Test show_terms_acceptance helper function."""
        # Arrange
        message = mock_message()
        message.answer = AsyncMock()

        from frontend.routers.legal_router import show_terms_acceptance

        # Act
        await show_terms_acceptance(message, mock_fsm_context)

        # Assert
        message.answer.assert_called_once()
        mock_fsm_context.set_state.assert_called_once()

    @pytest.mark.asyncio
    async def test_show_gambling_reminder(self, mock_message):
        """Test show_gambling_reminder helper function."""
        # Arrange
        message = mock_message()
        message.answer = AsyncMock()

        from frontend.routers.legal_router import show_gambling_reminder

        # Act
        await show_gambling_reminder(message)

        # Assert
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "gambling" in call_args.lower() or "risk" in call_args.lower()


class TestKeyboardGeneration:
    """Test keyboard generation functions."""

    def test_acceptance_keyboard_structure(self):
        """Test that acceptance keyboard has correct structure."""
        # Arrange & Act
        from frontend.routers.legal_router import get_acceptance_keyboard

        keyboard = get_acceptance_keyboard()

        # Assert
        assert keyboard is not None
        assert hasattr(keyboard, "inline_keyboard")
        assert len(keyboard.inline_keyboard) > 0

    def test_legal_nav_keyboard_structure(self):
        """Test that legal navigation keyboard has correct structure."""
        # Arrange & Act
        from frontend.routers.legal_router import get_legal_nav_keyboard

        keyboard = get_legal_nav_keyboard()

        # Assert
        assert keyboard is not None
        assert hasattr(keyboard, "inline_keyboard")
        assert len(keyboard.inline_keyboard) > 0


class TestMarkdownFormatting:
    """Test that legal documents use proper Markdown formatting."""

    @pytest.mark.asyncio
    async def test_terms_uses_markdown(self, mock_message):
        """Test that terms command uses Markdown parse mode."""
        # Arrange
        message = mock_message("/terms")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_terms

        # Act
        await cmd_terms(message)

        # Assert
        call_kwargs = message.answer.call_args[1]
        assert call_kwargs.get("parse_mode") == "Markdown"

    @pytest.mark.asyncio
    async def test_privacy_uses_markdown(self, mock_message):
        """Test that privacy command uses Markdown parse mode."""
        # Arrange
        message = mock_message("/privacy")
        message.answer = AsyncMock()

        from frontend.routers.legal_router import cmd_privacy

        # Act
        await cmd_privacy(message)

        # Assert
        call_kwargs = message.answer.call_args[1]
        assert call_kwargs.get("parse_mode") == "Markdown"


class TestCallbackAnswering:
    """Test that all callbacks are properly answered."""

    @pytest.mark.asyncio
    async def test_view_terms_answers_callback(self, mock_callback_query):
        """Test that view_terms answers the callback."""
        # Arrange
        callback = mock_callback_query("view_terms")
        callback.message.edit_text = AsyncMock()
        callback.answer = AsyncMock()

        from frontend.routers.legal_router import callback_view_terms

        # Act
        await callback_view_terms(callback)

        # Assert
        callback.answer.assert_called_once()

    @pytest.mark.asyncio
    async def test_accept_terms_answers_callback(self, mock_callback_query, mock_fsm_context):
        """Test that accept_terms answers the callback."""
        # Arrange
        callback = mock_callback_query("accept_terms")
        callback.message.edit_text = AsyncMock()
        callback.answer = AsyncMock()

        from frontend.routers.legal_router import callback_accept_terms

        # Act
        await callback_accept_terms(callback, mock_fsm_context)

        # Assert
        callback.answer.assert_called_once()


class TestLegalTextConstants:
    """Test legal text constants."""

    def test_legal_text_constants_exist(self):
        """Test that all legal text constants are defined."""
        # Arrange & Act
        from frontend.common.legal_text import (
            TERMS_SUMMARY, TERMS_FULL, PRIVACY_SUMMARY,
            RESPONSIBLE_GAMBLING_WARNING, GAMBLING_REMINDER_SHORT,
            AGE_VERIFICATION, TERMS_ACCEPTANCE, SUPPORT_INFO,
            WITHDRAWAL_POLICY, FAIR_PLAY
        )

        # Assert
        assert len(TERMS_SUMMARY) > 0
        assert len(TERMS_FULL) > 0
        assert len(PRIVACY_SUMMARY) > 0
        assert len(RESPONSIBLE_GAMBLING_WARNING) > 0
        assert len(GAMBLING_REMINDER_SHORT) > 0
        assert len(AGE_VERIFICATION) > 0
        assert len(TERMS_ACCEPTANCE) > 0
        assert len(SUPPORT_INFO) > 0
        assert len(WITHDRAWAL_POLICY) > 0
        assert len(FAIR_PLAY) > 0

    def test_get_legal_text_function(self):
        """Test get_legal_text helper function."""
        # Arrange & Act
        from frontend.common.legal_text import get_legal_text

        terms = get_legal_text("terms_full")
        privacy = get_legal_text("privacy")

        # Assert
        assert len(terms) > 0
        assert len(privacy) > 0

    def test_get_legal_text_invalid_key(self):
        """Test get_legal_text with invalid key."""
        # Arrange & Act
        from frontend.common.legal_text import get_legal_text

        result = get_legal_text("nonexistent_key")

        # Assert
        assert "not found" in result.lower() or "contact" in result.lower()

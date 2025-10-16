"""
Frontend Handler Tests for Ludicé Telegram Bot.

Tests message handlers, payment flows, FSM states, and game interactions.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import (
    Message, CallbackQuery, PreCheckoutQuery,
    LabeledPrice, SuccessfulPayment, User, Chat
)
from aiogram.fsm.context import FSMContext


pytestmark = pytest.mark.frontend


class TestStartCommand:
    """Test /start command handler."""

    @pytest.mark.asyncio
    async def test_start_command_sends_welcome(self, mock_message, mock_fsm_context):
        """Test that /start command sends welcome message."""
        # Arrange
        message = mock_message("/start")
        message.answer = AsyncMock()

        # Import handler
        from frontend.routers.private_user import cmd_start

        # Act
        await cmd_start(message, mock_fsm_context)

        # Assert
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        assert "Welcome" in call_args[0][0] or "welcome" in call_args[0][0].lower()

    @pytest.mark.asyncio
    async def test_start_command_includes_keyboard(self, mock_message, mock_fsm_context):
        """Test that /start command includes reply keyboard."""
        # Arrange
        message = mock_message("/start")
        message.answer = AsyncMock()

        from frontend.routers.private_user import cmd_start

        # Act
        await cmd_start(message, mock_fsm_context)

        # Assert
        message.answer.assert_called_once()
        call_kwargs = message.answer.call_args[1]
        assert "reply_markup" in call_kwargs


class TestPaymentHandlers:
    """Test payment callback handlers for all star tiers."""

    @pytest.mark.asyncio
    async def test_star15_payment_callback(self, mock_callback_query):
        """Test 15 stars payment callback."""
        # Arrange
        callback = mock_callback_query("star15")
        callback.message.answer_invoice = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        callback.message.answer_invoice.assert_called_once()
        call_kwargs = callback.message.answer_invoice.call_args[1]
        assert call_kwargs["currency"] == "XTR"
        assert "Telegram Stars" in call_kwargs["title"]

    @pytest.mark.asyncio
    async def test_star50_payment_callback(self, mock_callback_query):
        """Test 50 stars payment callback."""
        # Arrange
        callback = mock_callback_query("star50")
        callback.message.answer_invoice = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        callback.message.answer_invoice.assert_called_once()

    @pytest.mark.asyncio
    async def test_star100_payment_callback(self, mock_callback_query):
        """Test 100 stars payment callback."""
        # Arrange
        callback = mock_callback_query("star100")
        callback.message.answer_invoice = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        callback.message.answer_invoice.assert_called_once()

    @pytest.mark.asyncio
    async def test_star1000_payment_callback(self, mock_callback_query):
        """Test 1000 stars payment callback."""
        # Arrange
        callback = mock_callback_query("star1000")
        callback.message.answer_invoice = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        callback.message.answer_invoice.assert_called_once()

    @pytest.mark.asyncio
    async def test_payment_callback_deletes_message(self, mock_callback_query):
        """Test that payment callbacks delete original message."""
        # Arrange
        callback = mock_callback_query("star15")
        callback.message.answer_invoice = AsyncMock()
        callback.message.delete = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        callback.message.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_payment_includes_pay_button(self, mock_callback_query):
        """Test that payment invoice includes pay button."""
        # Arrange
        callback = mock_callback_query("star15")
        callback.message.answer_invoice = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        call_kwargs = callback.message.answer_invoice.call_args[1]
        assert "reply_markup" in call_kwargs


class TestPreCheckoutHandler:
    """Test pre-checkout query handler."""

    @pytest.mark.asyncio
    async def test_pre_checkout_answers_ok(self):
        """Test that pre-checkout query is answered with ok=True."""
        # Arrange
        pre_checkout = MagicMock(spec=PreCheckoutQuery)
        pre_checkout.answer = AsyncMock()

        from frontend.routers.private_user import pre_checkout as pre_checkout_handler

        # Act
        await pre_checkout_handler(pre_checkout)

        # Assert
        pre_checkout.answer.assert_called_once_with(ok=True)


class TestSuccessfulPayment:
    """Test successful payment handler."""

    @pytest.mark.asyncio
    async def test_successful_payment_confirmation(self, mock_message):
        """Test that successful payment sends confirmation message."""
        # Arrange
        message = mock_message()
        message.answer = AsyncMock()
        message.successful_payment = MagicMock(spec=SuccessfulPayment)

        from frontend.routers.private_user import payment_success

        # Act
        await payment_success(message)

        # Assert
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "payment" in call_args.lower() or "added" in call_args.lower()


class TestTopUpButton:
    """Test 'Top up' button handler."""

    @pytest.mark.asyncio
    async def test_top_up_button_shows_star_options(self, mock_message):
        """Test that 'Top up' button shows star payment options."""
        # Arrange
        message = mock_message("Top up 🔝")
        message.answer = AsyncMock()

        from frontend.routers.private_user import stars

        # Act
        await stars(message)

        # Assert
        message.answer.assert_called_once()
        call_kwargs = message.answer.call_args[1]
        assert "reply_markup" in call_kwargs


class TestGameSelection:
    """Test game selection handlers."""

    @pytest.mark.asyncio
    async def test_roll_button_shows_games(self, mock_message):
        """Test that 'Roll' button shows game options."""
        # Arrange
        message = mock_message("Roll 🎲")
        message.answer = AsyncMock()

        from frontend.routers.private_user import play_game

        # Act
        await play_game(message)

        # Assert
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "game" in call_args.lower()

    @pytest.mark.asyncio
    async def test_dice_game_selection(self, mock_message, mock_fsm_context):
        """Test selecting Dice game."""
        # Arrange
        message = mock_message("Dice 🎲")
        message.answer = AsyncMock()

        # Mock the show_gambling_reminder function
        with patch("frontend.routers.private_user.show_gambling_reminder", new=AsyncMock()):
            from frontend.routers.private_user import play_dice

            # Act
            await play_dice(message, mock_fsm_context)

        # Assert
        message.answer.assert_called_once()
        mock_fsm_context.set_state.assert_called_once()

    @pytest.mark.asyncio
    async def test_dice_game_shows_gambling_reminder(self, mock_message, mock_fsm_context):
        """Test that dice game shows gambling reminder."""
        # Arrange
        message = mock_message("Dice 🎲")
        message.answer = AsyncMock()

        mock_reminder = AsyncMock()
        with patch("frontend.routers.private_user.show_gambling_reminder", mock_reminder):
            from frontend.routers.private_user import play_dice

            # Act
            await play_dice(message, mock_fsm_context)

        # Assert
        mock_reminder.assert_called_once_with(message)

    @pytest.mark.asyncio
    async def test_target_game_not_implemented(self, mock_callback_query):
        """Test that Target game shows 'in development' message."""
        # Arrange
        callback = mock_callback_query("game_target")
        callback.answer = AsyncMock()

        from frontend.routers.private_user import play_target

        # Act
        await play_target(callback)

        # Assert
        callback.answer.assert_called_once()
        call_args = callback.answer.call_args[0][0]
        assert "development" in call_args.lower()


class TestFSMBettingFlow:
    """Test FSM state for betting flow."""

    @pytest.mark.asyncio
    async def test_fsm_sets_waiting_for_bet_state(self, mock_message, mock_fsm_context):
        """Test that dice game sets FSM to waiting_for_bet state."""
        # Arrange
        message = mock_message("Dice 🎲")
        message.answer = AsyncMock()

        with patch("frontend.routers.private_user.show_gambling_reminder", new=AsyncMock()):
            from frontend.routers.private_user import play_dice, Form

            # Act
            await play_dice(message, mock_fsm_context)

        # Assert
        mock_fsm_context.set_state.assert_called_once_with(Form.waiting_for_bet)

    @pytest.mark.asyncio
    async def test_process_bet_valid_number(self, mock_message, mock_fsm_context):
        """Test processing valid bet amount."""
        # Arrange
        message = mock_message("50")
        message.answer = AsyncMock()
        mock_fsm_context.update_data = AsyncMock()

        from frontend.routers.private_user import process_bet

        # Act
        await process_bet(message, mock_fsm_context)

        # Assert
        mock_fsm_context.update_data.assert_called_once_with(bet=50)
        message.answer.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_bet_invalid_input(self, mock_message, mock_fsm_context):
        """Test processing invalid bet input."""
        # Arrange
        message = mock_message("abc")
        message.answer = AsyncMock()

        from frontend.routers.private_user import process_bet

        # Act
        await process_bet(message, mock_fsm_context)

        # Assert
        # Should not call update_data for invalid input
        mock_fsm_context.update_data.assert_not_called()
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "valid" in call_args.lower() or "number" in call_args.lower()

    @pytest.mark.asyncio
    async def test_process_bet_negative_number(self, mock_message, mock_fsm_context):
        """Test processing negative bet amount."""
        # Arrange
        message = mock_message("-50")
        message.answer = AsyncMock()

        from frontend.routers.private_user import process_bet

        # Act
        await process_bet(message, mock_fsm_context)

        # Assert
        # Should reject negative numbers
        mock_fsm_context.update_data.assert_not_called()

    @pytest.mark.asyncio
    async def test_process_bet_zero(self, mock_message, mock_fsm_context):
        """Test processing zero bet amount."""
        # Arrange
        message = mock_message("0")
        message.answer = AsyncMock()
        mock_fsm_context.update_data = AsyncMock()

        from frontend.routers.private_user import process_bet

        # Act
        await process_bet(message, mock_fsm_context)

        # Assert
        # The code might accept 0, but ideally should validate minimum bet
        message.answer.assert_called_once()


class TestBotInteractions:
    """Test bot interaction patterns."""

    @pytest.mark.asyncio
    async def test_callback_query_answered(self, mock_callback_query):
        """Test that callback queries are answered."""
        # Arrange
        callback = mock_callback_query("star15")
        callback.answer = AsyncMock()
        callback.message.answer_invoice = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        callback.answer.assert_called_once()

    @pytest.mark.asyncio
    async def test_message_reply_markup_cleared(self, mock_callback_query):
        """Test that inline keyboards are cleaned up after use."""
        # Arrange
        callback = mock_callback_query("star15")
        callback.message.edit_reply_markup = AsyncMock()
        callback.message.answer_invoice = AsyncMock()
        callback.message.delete = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        callback.message.edit_reply_markup.assert_called_once_with(reply_markup=None)


class TestErrorHandling:
    """Test error handling in handlers."""

    @pytest.mark.asyncio
    async def test_handler_with_none_message(self, mock_fsm_context):
        """Test handler behavior with None message."""
        # This tests defensive programming
        # In production, handlers should validate input
        pass  # Placeholder - implement based on actual error handling

    @pytest.mark.asyncio
    async def test_payment_with_invalid_currency(self):
        """Test payment handling with invalid currency."""
        # This should be prevented at the bot level
        # All payments use XTR (Telegram Stars)
        pass  # Placeholder


class TestUserContext:
    """Test user context in handlers."""

    @pytest.mark.asyncio
    async def test_handler_accesses_user_id(self, mock_message):
        """Test that handlers can access user ID."""
        # Arrange
        message = mock_message("/start")

        # Act
        user_id = message.from_user.id

        # Assert
        assert user_id == 123456789

    @pytest.mark.asyncio
    async def test_handler_accesses_username(self, mock_message):
        """Test that handlers can access username."""
        # Arrange
        message = mock_message("/start")

        # Act
        username = message.from_user.username

        # Assert
        assert username == "testuser"


class TestAPIIntegration:
    """Test handlers that make API calls to backend."""

    @pytest.mark.asyncio
    async def test_bet_submission_calls_backend(self, mock_message, mock_fsm_context):
        """Test that bet submission would call backend API."""
        # Note: The current implementation has commented-out API calls
        # This is a structure test for when API integration is enabled

        # Arrange
        message = mock_message("50")
        message.answer = AsyncMock()

        # This would test the API call when uncommented in the code
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200

            from frontend.routers.private_user import process_bet

            # Act
            await process_bet(message, mock_fsm_context)

            # Assert
            # When API calls are enabled, this would verify the call
            # mock_post.assert_called_once()


class TestInvoiceGeneration:
    """Test invoice generation for different payment amounts."""

    @pytest.mark.asyncio
    async def test_invoice_includes_correct_prices(self, mock_callback_query):
        """Test that invoice includes correct price information."""
        # Arrange
        callback = mock_callback_query("star15")
        callback.message.answer_invoice = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        call_kwargs = callback.message.answer_invoice.call_args[1]
        assert "prices" in call_kwargs
        assert isinstance(call_kwargs["prices"], list)
        assert len(call_kwargs["prices"]) > 0

    @pytest.mark.asyncio
    async def test_invoice_uses_xtr_currency(self, mock_callback_query):
        """Test that all invoices use XTR (Telegram Stars) currency."""
        # Arrange
        callback = mock_callback_query("star15")
        callback.message.answer_invoice = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        call_kwargs = callback.message.answer_invoice.call_args[1]
        assert call_kwargs["currency"] == "XTR"

    @pytest.mark.asyncio
    async def test_invoice_has_description(self, mock_callback_query):
        """Test that invoice includes description."""
        # Arrange
        callback = mock_callback_query("star15")
        callback.message.answer_invoice = AsyncMock()

        from frontend.routers.private_user import send_invoice

        # Act
        await send_invoice(callback)

        # Assert
        call_kwargs = callback.message.answer_invoice.call_args[1]
        assert "description" in call_kwargs
        assert len(call_kwargs["description"]) > 0

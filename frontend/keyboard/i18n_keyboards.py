"""
Internationalized keyboards for the Ludicé bot.
Generates keyboards with text in the user's preferred language.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from localization import get_text


def get_start_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """
    Get the main start keyboard in the user's language.

    Args:
        user_id: Telegram user ID

    Returns:
        Localized ReplyKeyboardMarkup
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text("buttons.roll", user_id)),
                KeyboardButton(text=get_text("buttons.help", user_id)),
            ],
            [
                KeyboardButton(text=get_text("buttons.profile", user_id)),
                KeyboardButton(text=get_text("buttons.top_up", user_id)),
            ]
        ],
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder=get_text("menu.choose_option", user_id)
    )


def get_game_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """
    Get the game selection keyboard in the user's language.

    Args:
        user_id: Telegram user ID

    Returns:
        Localized ReplyKeyboardMarkup
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text("buttons.dice", user_id)),
                KeyboardButton(text=get_text("buttons.target", user_id)),
            ]
        ],
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder=get_text("menu.choose_game", user_id)
    )


def get_language_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Get the language selection keyboard.
    Shows all available languages.

    Returns:
        InlineKeyboardMarkup with language options
    """
    from localization.i18n import get_available_languages

    languages = get_available_languages()

    # Create keyboard rows with 2 languages per row
    keyboard = []
    row = []

    for lang_code, lang_name in sorted(languages.items()):
        # Get the flag from the translation file if available
        from localization.i18n import _i18n
        flag = _i18n.translations.get(lang_code, {}).get('_language_flag', '')

        button_text = f"{flag} {lang_name}" if flag else lang_name
        row.append(InlineKeyboardButton(text=button_text, callback_data=f"lang_{lang_code}"))

        if len(row) == 2:
            keyboard.append(row)
            row = []

    # Add remaining button if any
    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_legal_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Get the terms acceptance keyboard in the user's language.

    Args:
        user_id: Telegram user ID

    Returns:
        Localized InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("terms.accept", user_id), callback_data="accept_terms"),
            InlineKeyboardButton(text=get_text("terms.read_full", user_id), callback_data="view_full_terms")
        ],
        [
            InlineKeyboardButton(text=get_text("terms.decline", user_id), callback_data="decline_terms")
        ]
    ])


def get_waiting_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Get the waiting for opponent keyboard in the user's language.

    Args:
        user_id: Telegram user ID

    Returns:
        Localized InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("buttons.cancel_search", user_id), callback_data="cancel_search")]
    ])


def get_dice_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Get the roll dice keyboard in the user's language.

    Args:
        user_id: Telegram user ID

    Returns:
        Localized InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("buttons.roll_dice", user_id), callback_data="roll_dice")]
    ])


def get_play_again_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Get the play again keyboard in the user's language.

    Args:
        user_id: Telegram user ID

    Returns:
        Localized InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("buttons.play_again", user_id), callback_data="play_again")],
        [InlineKeyboardButton(text=get_text("menu.main_menu", user_id), callback_data="main_menu")]
    ])


# Payment keyboard remains the same as it uses star amounts
def get_payment_keyboard() -> InlineKeyboardMarkup:
    """
    Get the payment amount selection keyboard.
    Uses numeric amounts which are universal.

    Returns:
        InlineKeyboardMarkup with payment options
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="15 ⭐", callback_data="star15"),
                InlineKeyboardButton(text="50 ⭐", callback_data="star50"),
                InlineKeyboardButton(text="75 ⭐", callback_data="star75"),
                InlineKeyboardButton(text="100 ⭐", callback_data="star100"),
            ],
            [
                InlineKeyboardButton(text="150 ⭐", callback_data="star150"),
                InlineKeyboardButton(text="250 ⭐", callback_data="star250"),
                InlineKeyboardButton(text="350 ⭐", callback_data="star350"),
                InlineKeyboardButton(text="750 ⭐", callback_data="star750"),
            ],
            [
                InlineKeyboardButton(text="1 000 ⭐", callback_data="star1000"),
                InlineKeyboardButton(text="1 500 ⭐", callback_data="star1500"),
                InlineKeyboardButton(text="2 500 ⭐", callback_data="star2500"),
                InlineKeyboardButton(text="5 000 ⭐", callback_data="star5000"),
            ],
            [
                InlineKeyboardButton(text="10 000 ⭐", callback_data="star10000"),
                InlineKeyboardButton(text="25 000 ⭐", callback_data="star25000"),
                InlineKeyboardButton(text="35 000 ⭐", callback_data="star35000"),
                InlineKeyboardButton(text="50 000 ⭐", callback_data="star50000"),
            ],
            [
                InlineKeyboardButton(text="100 000 ⭐", callback_data="star100000"),
                InlineKeyboardButton(text="150 000 ⭐", callback_data="star150000"),
                InlineKeyboardButton(text="500 000 ⭐", callback_data="star500000"),
            ],
            [
                InlineKeyboardButton(text="1 000 000 ⭐", callback_data="star1000000"),
            ]
        ]
    )

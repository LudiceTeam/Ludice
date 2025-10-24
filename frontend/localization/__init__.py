"""
Localization module for Ludicé bot.
Provides multi-language support for all user-facing text.
"""

from .i18n import (
    I18n,
    get_text,
    set_user_language,
    get_user_language,
    get_available_languages
)

__all__ = [
    'I18n',
    'get_text',
    'set_user_language',
    'get_user_language',
    'get_available_languages'
]

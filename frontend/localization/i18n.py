"""
Internationalization (i18n) system for the Ludicé bot.
Handles language selection, user preferences, and text translation.
"""

import json
from pathlib import Path
from typing import Dict
from .user_preferences import UserPreferences

class I18n:
    """Manages translations and user language preferences."""

    def __init__(self, locales_dir: str = None, default_language: str = "en"):
        """
        Initialize the i18n manager.

        Args:
            locales_dir: Directory containing translation files
            default_language: Default language code (e.g., 'en', 'ru')
        """
        if locales_dir is None:
            locales_dir = Path(__file__).parent / "locales"

        self.locales_dir = Path(locales_dir)
        self.default_language = default_language
        self.translations: Dict[str, Dict] = {}

        # Use persistent user preferences
        self.user_prefs = UserPreferences()

        # Load all available translations
        self._load_translations()

    def _load_translations(self):
        """Load all translation files from the locales directory."""
        if not self.locales_dir.exists():
            self.locales_dir.mkdir(parents=True, exist_ok=True)
            return

        for file_path in self.locales_dir.glob("*.json"):
            language_code = file_path.stem
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[language_code] = json.load(f)
            except Exception as e:
                print(f"Error loading translation file {file_path}: {e}")

    def set_user_language(self, user_id: int, language_code: str):
        """
        Set the preferred language for a user.

        Args:
            user_id: Telegram user ID
            language_code: Language code (e.g., 'en', 'ru')
        """
        if language_code in self.translations:
            self.user_prefs.set_language(user_id, language_code)
        else:
            print(f"Warning: Language '{language_code}' not available. Using default.")
            self.user_prefs.set_language(user_id, self.default_language)

    def get_user_language(self, user_id: int) -> str:
        """
        Get the preferred language for a user.

        Args:
            user_id: Telegram user ID

        Returns:
            Language code
        """
        return self.user_prefs.get_language(user_id, self.default_language)

    def get(self, key: str, user_id: int = None, language: str = None, **kwargs) -> str:
        """
        Get translated text for a key.

        Args:
            key: Translation key (supports nested keys with dots, e.g., 'menu.start')
            user_id: Telegram user ID (used to get user's preferred language)
            language: Override language code
            **kwargs: Format parameters for the translation string

        Returns:
            Translated text
        """
        # Determine which language to use
        if language is None:
            if user_id is not None:
                language = self.get_user_language(user_id)
            else:
                language = self.default_language

        # Get the translation
        translation = self._get_translation(key, language)

        # Format with parameters if provided
        if kwargs:
            try:
                return translation.format(**kwargs)
            except (KeyError, ValueError) as e:
                print(f"Error formatting translation '{key}': {e}")
                return translation

        return translation

    def _get_translation(self, key: str, language: str) -> str:
        """
        Get translation from the language dictionary.

        Args:
            key: Translation key (supports nested keys with dots)
            language: Language code

        Returns:
            Translated text or the key itself if not found
        """
        # Check if language exists
        if language not in self.translations:
            language = self.default_language

        # Navigate nested dictionary using dot notation
        parts = key.split('.')
        value = self.translations.get(language, {})

        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                # Fallback to default language
                if language != self.default_language:
                    return self._get_translation(key, self.default_language)
                # Return key if not found
                print(f"Warning: Translation key '{key}' not found for language '{language}'")
                return key

        return str(value)

    def get_available_languages(self) -> Dict[str, str]:
        """
        Get all available languages.

        Returns:
            Dictionary of language codes to language names
        """
        languages = {}
        for lang_code, translations in self.translations.items():
            # Each translation file should have a _language_name key
            languages[lang_code] = translations.get('_language_name', lang_code.upper())
        return languages


# Global i18n instance
_i18n = I18n()


def get_text(key: str, user_id: int = None, language: str = None, **kwargs) -> str:
    """
    Convenience function to get translated text.

    Args:
        key: Translation key
        user_id: Telegram user ID
        language: Override language code
        **kwargs: Format parameters

    Returns:
        Translated text
    """
    return _i18n.get(key, user_id, language, **kwargs)


def set_user_language(user_id: int, language_code: str):
    """
    Set user's preferred language.

    Args:
        user_id: Telegram user ID
        language_code: Language code
    """
    _i18n.set_user_language(user_id, language_code)


def get_user_language(user_id: int) -> str:
    """
    Get user's preferred language.

    Args:
        user_id: Telegram user ID

    Returns:
        Language code
    """
    return _i18n.get_user_language(user_id)


def get_available_languages() -> Dict[str, str]:
    """
    Get all available languages.

    Returns:
        Dictionary of language codes to language names
    """
    return _i18n.get_available_languages()

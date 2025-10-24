"""
User language preferences storage for the Ludicé bot.
Persists user language selections to a JSON file.
"""

import json
from pathlib import Path
from threading import Lock
from typing import Dict

class UserPreferences:
    """Manages user language preferences with file persistence."""

    def __init__(self, preferences_file: str = None):
        """
        Initialize user preferences manager.

        Args:
            preferences_file: Path to the JSON file storing preferences
        """
        if preferences_file is None:
            # Store in data directory (same as other bot data files)
            data_dir = Path(__file__).parent.parent.parent / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            preferences_file = data_dir / "user_languages.json"

        self.preferences_file = Path(preferences_file)
        self.lock = Lock()
        self._preferences: Dict[str, str] = {}

        # Load existing preferences
        self._load()

    def _load(self):
        """Load user preferences from file."""
        if self.preferences_file.exists():
            try:
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    self._preferences = json.load(f)
            except Exception as e:
                print(f"Error loading user preferences: {e}")
                self._preferences = {}
        else:
            self._preferences = {}

    def _save(self):
        """Save user preferences to file."""
        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self._preferences, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving user preferences: {e}")

    def set_language(self, user_id: int, language_code: str):
        """
        Set user's preferred language.

        Args:
            user_id: Telegram user ID
            language_code: Language code (e.g., 'en', 'ru', 'es', 'fr')
        """
        with self.lock:
            self._preferences[str(user_id)] = language_code
            self._save()

    def get_language(self, user_id: int, default: str = "en") -> str:
        """
        Get user's preferred language.

        Args:
            user_id: Telegram user ID
            default: Default language if user has no preference

        Returns:
            Language code
        """
        with self.lock:
            return self._preferences.get(str(user_id), default)

    def remove_user(self, user_id: int):
        """
        Remove user's language preference.

        Args:
            user_id: Telegram user ID
        """
        with self.lock:
            if str(user_id) in self._preferences:
                del self._preferences[str(user_id)]
                self._save()

    def get_all_preferences(self) -> Dict[str, str]:
        """
        Get all user preferences.

        Returns:
            Dictionary of user IDs to language codes
        """
        with self.lock:
            return self._preferences.copy()


# Global preferences instance
_preferences = UserPreferences()


def set_user_language(user_id: int, language_code: str):
    """
    Set user's preferred language.

    Args:
        user_id: Telegram user ID
        language_code: Language code
    """
    _preferences.set_language(user_id, language_code)


def get_user_language(user_id: int, default: str = "en") -> str:
    """
    Get user's preferred language.

    Args:
        user_id: Telegram user ID
        default: Default language

    Returns:
        Language code
    """
    return _preferences.get_language(user_id, default)

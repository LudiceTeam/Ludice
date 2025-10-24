# Multi-Language Support (i18n) Guide

This guide explains how the internationalization (i18n) system works in the Ludicé Telegram bot and how to extend it with additional languages.

## Overview

The bot now supports multiple languages with a complete translation system:
- **Supported Languages**: English (en), Russian (ru), Spanish (es), French (fr)
- **User Preferences**: Language choices are saved persistently
- **Complete Coverage**: All user-facing text, buttons, and messages are translatable

## Architecture

### Components

1. **Localization Module** (`frontend/localization/`)
   - `i18n.py` - Core translation engine
   - `user_preferences.py` - User language preference storage
   - `locales/` - Translation files (JSON)

2. **Internationalized Keyboards** (`frontend/keyboard/i18n_keyboards.py`)
   - Dynamic keyboards that adapt to user's language

3. **Multi-Language Legal Text** (`frontend/common/legal_text.py`)
   - Terms of Service in all supported languages

## User Flow

1. User sends `/start` command
2. Bot displays language selection menu
3. User selects preferred language
4. Language preference is saved to `data/user_languages.json`
5. All subsequent messages appear in the selected language

## Adding a New Language

### Step 1: Create Translation File

Create a new JSON file in `frontend/localization/locales/` (e.g., `de.json` for German):

```json
{
  "_language_name": "Deutsch",
  "_language_flag": "🇩🇪",

  "language": {
    "select": "Bitte wählen Sie Ihre Sprache:",
    "selected": "✅ Sprache auf Deutsch gesetzt!",
    "change": "🌐 Sprache ändern"
  },

  "menu": {
    "welcome": "Willkommen bei Ludicé! Wählen Sie eine Option:",
    "main_menu": "🏠 Hauptmenü",
    "choose_game": "Wählen Sie ein Spiel:",
    "choose_option": "Wählen Sie eine Option..."
  },

  "buttons": {
    "roll": "Würfeln 🎲",
    "help": "Hilfe ❓",
    "profile": "Profil 👤",
    "top_up": "Aufladen 🔝",
    "dice": "Würfel 🎲",
    "target": "Ziel 🎯",
    "play_again": "🎲 Nochmal spielen",
    "cancel_search": "❌ Suche abbrechen",
    "roll_dice": "🎲 Würfeln"
  },

  "game": {
    "dice_selected": "🎲 Sie haben Würfel gewählt! Wie viel möchten Sie setzen?",
    "invalid_bet": "❌ Bitte geben Sie eine gültige Zahl für Ihren Einsatz ein.",
    "minimum_bet": "❌ Mindesteinsatz beträgt 10 Sterne. Bitte geben Sie einen gültigen Betrag ein."
    // ... add all other keys
  }

  // Include all other translation keys from en.json
}
```

### Step 2: Add Legal Text Translation

Update `frontend/common/legal_text.py`:

```python
LEGAL_TEXTS = {
    # ... existing languages
    "de": """
📋 **Ludicé - Nutzungsbedingungen**

**1. BERECHTIGUNG**
• Muss 18+ Jahre alt sein
• Gültiges Telegram-Konto erforderlich
// ... rest of terms
"""
}
```

### Step 3: Test the Language

1. Restart the bot
2. Send `/start`
3. Select the new language
4. Verify all text appears correctly

## Translation File Structure

### Special Keys

- `_language_name`: Display name of the language
- `_language_flag`: Flag emoji for the language picker

### Key Naming Convention

Use dot notation for nested organization:
- `category.subcategory.key`
- Example: `game.opponent_found`, `errors.auth_failed`

### Format Parameters

Use Python format string syntax for dynamic values:

```json
{
  "game.opponent_found": "🎮 Opponent found!\nBet: {bet} ⭐\n\nRoll your dice!"
}
```

Usage in code:
```python
get_text("game.opponent_found", user_id, bet=100)
```

## Using Translations in Code

### Basic Usage

```python
from localization import get_text

# Get translated text for user
message_text = get_text("menu.welcome", user_id)
```

### With Format Parameters

```python
# Translation: "Your roll: {roll}"
text = get_text("game.your_roll", user_id, roll=dice_value)
```

### Getting User's Language

```python
from localization import get_user_language

user_lang = get_user_language(user_id)  # Returns 'en', 'ru', etc.
```

### Setting User's Language

```python
from localization import set_user_language

set_user_language(user_id, "ru")
```

## Creating Internationalized Keyboards

### Reply Keyboards

```python
from keyboard.i18n_keyboards import get_start_keyboard

# Keyboard with buttons in user's language
keyboard = get_start_keyboard(user_id)
await message.answer("Text", reply_markup=keyboard)
```

### Inline Keyboards

```python
from keyboard.i18n_keyboards import get_dice_keyboard

# Inline keyboard for rolling dice
keyboard = get_dice_keyboard(user_id)
await message.answer("Roll!", reply_markup=keyboard)
```

### Custom Keyboards

Create new keyboards in `frontend/keyboard/i18n_keyboards.py`:

```python
def get_custom_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Custom keyboard in user's language."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text("buttons.custom", user_id),
            callback_data="custom_action"
        )]
    ])
```

## Handling Text-Based Button Presses

Since ReplyKeyboardMarkup sends text, you need to match button text dynamically:

```python
@router.message(F.text)
async def handle_buttons(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if text == get_text("buttons.roll", user_id):
        # Handle "Roll" button press
        await handle_roll(message)
```

## File Locations

### Translation Files
- `frontend/localization/locales/*.json`

### User Preferences Storage
- `data/user_languages.json` (auto-created)

### Keyboard Definitions
- `frontend/keyboard/i18n_keyboards.py`

### Core Modules
- `frontend/localization/i18n.py` - Translation engine
- `frontend/localization/user_preferences.py` - Preference storage

## Best Practices

### 1. Complete Coverage
Ensure all user-facing text is translatable:
- Error messages
- Success confirmations
- Game instructions
- Payment flows

### 2. Consistent Tone
Maintain consistent tone and formality across languages for the same keys.

### 3. Context Awareness
Provide enough context in translation keys:
- `game.opponent_found` (good)
- `found` (bad - lacks context)

### 4. Format String Safety
Always include the same format parameters across all languages:

```json
{
  "en": "Hello {name}, you have {count} stars",
  "ru": "Привет {name}, у вас {count} звёзд"
}
```

### 5. Test All Languages
Test the complete user flow in each supported language.

## Troubleshooting

### Missing Translation Key

If a key is missing:
1. The system returns the key itself as a fallback
2. A warning is logged to console
3. Check console for: `Warning: Translation key 'x.y.z' not found`

### User Language Not Saving

Check that:
- `data/` directory exists
- Bot has write permissions
- No JSON syntax errors in `user_languages.json`

### Keyboard Not Updating

Ensure you're using the i18n keyboard functions:
```python
# ✅ Correct
from keyboard.i18n_keyboards import get_start_keyboard
keyboard = get_start_keyboard(user_id)

# ❌ Incorrect
from keyboard import start
keyboard = start.start_kb  # This uses hardcoded English
```

## Adding More Translation Keys

1. Add the key to all language files in `locales/`:
   ```json
   {
     "new_category": {
       "new_key": "Translated text"
     }
   }
   ```

2. Use in code:
   ```python
   text = get_text("new_category.new_key", user_id)
   ```

3. Restart the bot (translations are loaded at startup)

## Performance Notes

- Translations are loaded once at startup
- User preferences use file locking for thread safety
- Language detection is O(1) lookup
- No performance impact from multiple languages

## Future Enhancements

Consider implementing:
- Language auto-detection based on Telegram client language
- In-app language switching command (e.g., `/language`)
- Translation contributor credits
- Professional translation review
- Language-specific formatting (dates, numbers, currency)

## Support

For questions or issues with the i18n system:
1. Check this documentation
2. Review example code in `frontend/routers/private_user.py`
3. Contact: @ludicegifter

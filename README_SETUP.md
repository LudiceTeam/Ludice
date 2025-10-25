# 🎮 Ludicé Bot - Quick Start Guide

## ✅ Environment Fixed!

Your development environment is now properly configured.

## 🚀 Running the Bot

### Option 1: Using the Start Script
```bash
./start_bot.sh
```

### Option 2: Using VS Code
1. **Reload VS Code Window**: 
   - Press `Cmd+Shift+P`
   - Type "Reload Window" and press Enter
   
2. **Select the Correct Python Interpreter**:
   - Press `Cmd+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose: `Python 3.9.17 ('venv': venv) ./venv/bin/python`

3. **Run/Debug**:
   - Press `F5` or go to Run → Start Debugging
   - Select "Python: Ludicé Bot" from the dropdown

### Option 3: Command Line
```bash
cd frontend
../venv/bin/python app.py
```

## 🌍 Multi-Language Features

Your bot now supports **4 languages**:
- 🇬🇧 English
- 🇷🇺 Russian  
- 🇪🇸 Spanish
- 🇫🇷 French

Users can select their language when they first use `/start`

## 📁 Important Files

- **VS Code Config**: `.vscode/settings.json` - Python interpreter settings
- **Launch Config**: `.vscode/launch.json` - Debug configurations
- **Translations**: `frontend/localization/locales/*.json`
- **User Languages**: `data/user_languages.json` (auto-created)

## 🔧 VS Code Configuration Created

Two configuration files were created:

1. **`.vscode/settings.json`** - Tells VS Code to use your virtual environment
2. **`.vscode/launch.json`** - Debug configurations for bot and backend

## ⚠️ Important Notes

1. **Always use the venv Python**: `/Users/vikrorkhanin/Ludice/venv/bin/python`
2. **Reload VS Code** after making these changes
3. **Check the Python interpreter** in the bottom-left of VS Code

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'aiogram'"
- VS Code is using the wrong Python interpreter
- Solution: Reload VS Code window and select the venv interpreter

### Bot won't start
```bash
# Check if dependencies are installed in venv
/Users/vikrorkhanin/Ludice/venv/bin/python -m pip list | grep aiogram
```

### Need to reinstall dependencies
```bash
/Users/vikrorkhanin/Ludice/venv/bin/python -m pip install -r requirements.txt
```

## 📚 Documentation

- **i18n Guide**: `docs/i18n-guide.md` - How to add more languages
- **Project Overview**: `CLAUDE.md` - Architecture and development guide

## 🎉 You're All Set!

The bot is ready to run with full multi-language support!

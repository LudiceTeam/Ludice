# Contributing to Ludicé

Thank you for your interest in contributing to Ludicé! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- 🐛 **Report bugs** - Help us identify and fix issues
- ✨ **Suggest features** - Share ideas for new features
- 📝 **Improve documentation** - Help others understand the project
- 🌍 **Add translations** - Support more languages
- 💻 **Submit code** - Implement features or fix bugs
- 🧪 **Write tests** - Improve code coverage

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Ludice.git
cd Ludice
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

## 📋 Development Guidelines

### Code Style

We follow PEP 8 for Python code with these tools:

```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy frontend/ backend/
```

### Git Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
feat: add new game mode
fix: resolve payment processing bug
docs: update API documentation
style: format code with black
refactor: simplify game logic
test: add unit tests for payments
chore: update dependencies
```

Examples:
```
feat(i18n): add German language support
fix(api): correct signature verification
docs(readme): update installation instructions
```

### Testing

All new features must include tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_game_logic.py
```

### Documentation

- Update documentation for any user-facing changes
- Add docstrings to all functions and classes
- Update API documentation for new endpoints
- Include examples in documentation

## 🌍 Adding Translations

To add a new language:

1. **Create translation file:**
```bash
# Copy English template
cp frontend/localization/locales/en.json frontend/localization/locales/de.json
```

2. **Translate all strings:**
```json
{
  "_language_name": "Deutsch",
  "_language_flag": "🇩🇪",
  "menu": {
    "welcome": "Willkommen bei Ludicé!",
    ...
  }
}
```

3. **Add legal text:**
Edit `frontend/common/legal_text.py` and add the translated terms.

4. **Test thoroughly** - Test all bot interactions in the new language

See [docs/i18n-guide.md](i18n-guide.md) for detailed instructions.

## 🐛 Reporting Bugs

### Before Submitting

1. Check existing [issues](https://github.com/yourusername/Ludice/issues)
2. Try to reproduce the bug
3. Collect relevant information

### Bug Report Template

```markdown
**Describe the bug**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.9.17]
- Bot version: [e.g., 1.0.0]

**Additional context**
Any other relevant information.
```

## ✨ Feature Requests

### Before Requesting

1. Check if the feature already exists
2. Search existing feature requests
3. Consider if it fits the project scope

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives**
Other solutions you've considered.

**Additional context**
Mockups, examples, or other context.
```

## 🔄 Pull Request Process

### 1. Ensure Quality

Before submitting:

```bash
# Format code
black .

# Check linting
flake8 .

# Run tests
pytest

# Check coverage
pytest --cov=.
```

### 2. Update Documentation

- Update README.md if needed
- Add docstrings to new code
- Update API documentation
- Include usage examples

### 3. Submit PR

1. Push your changes to your fork
2. Create a Pull Request to the `dev` branch
3. Fill out the PR template completely
4. Link related issues

### 4. Code Review

- Respond to reviewer feedback
- Make requested changes
- Keep the discussion constructive
- Be patient - reviews take time

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings
- [ ] Related issues linked

## 🏗️ Project Structure

Understanding the codebase:

```
Ludicé/
├── frontend/              # Telegram Bot
│   ├── routers/          # Message handlers
│   │   ├── private_user.py    # User interactions
│   │   └── admin_user.py      # Admin commands
│   ├── localization/     # i18n system
│   │   ├── i18n.py          # Translation engine
│   │   └── locales/         # Translation files
│   └── keyboard/         # UI components
│
├── backend/              # API Server
│   ├── new.py           # Main API
│   └── redis/           # Balance service
│
├── web/                 # Mini App
│   ├── js/             # Frontend logic
│   └── css/            # Styles
│
├── data/               # Persistent storage
└── docs/              # Documentation
```

## 🔐 Security

### Reporting Security Issues

**DO NOT** create public issues for security vulnerabilities.

Instead, email [security@ludicé.com](mailto:security@ludice.com) with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We'll respond within 48 hours.

### Security Best Practices

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Validate all user input
- Follow the principle of least privilege
- Keep dependencies updated

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards other members

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Violations can be reported to [conduct@ludicé.com](mailto:conduct@ludice.com). All complaints will be reviewed and investigated.

## 📞 Getting Help

- 💬 **Discord**: [Join our server](https://discord.gg/ludice)
- 📧 **Email**: [dev@ludicé.com](mailto:dev@ludice.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/Ludice/issues)
- 📚 **Docs**: [Documentation](../README.md)

## 🙏 Recognition

Contributors are recognized in several ways:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Special role in Discord (for regular contributors)
- Swag for significant contributions

## 📖 Additional Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Aiogram Documentation](https://docs.aiogram.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

Thank you for contributing to Ludicé! 🎲

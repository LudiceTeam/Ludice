# Legal Documents - Implementation Guide

This directory contains comprehensive legal documentation for the Ludicé Telegram bot.

## 📁 Files Overview

### Main Legal Documents

1. **TERMS_OF_SERVICE.md** - Complete Terms of Service
   - 22 comprehensive sections
   - Covers eligibility, game rules, payments, liability, dispute resolution
   - **Action Required**: Update jurisdiction and governing law (Section 15.4, 15.5)

2. **PRIVACY_POLICY.md** - Complete Privacy Policy
   - GDPR and CCPA compliant
   - Data collection, usage, retention, and user rights
   - **Action Required**: Specify server locations (Section 8.1)

3. **RESPONSIBLE_GAMBLING.md** - Responsible Gambling Policy
   - Warning signs, help resources, self-exclusion
   - International support hotlines
   - Age verification procedures

4. **BOT_SUMMARY.md** - Quick reference summary
   - Condensed version for users
   - Key points from all policies

### Bot Integration Files

5. **frontend/common/legal_text.py** - Python constants
   - Pre-formatted legal text for bot display
   - Easy integration into aiogram handlers

6. **frontend/routers/legal_router.py** - Router implementation
   - Complete legal commands implementation
   - Terms acceptance flow
   - Age verification flow

## 🚀 Integration Guide

### Step 1: Review and Customize

Before deploying, you MUST update these placeholders:

#### In TERMS_OF_SERVICE.md:
```markdown
Line 281: [YOUR JURISDICTION]  # e.g., "the State of California"
Line 286: [YOUR JURISDICTION]  # Same as above
```

#### In PRIVACY_POLICY.md:
```markdown
Line 208: [Specify your server locations]  # e.g., "United States (AWS US-East-1), Europe (AWS EU-West-1)"
Line 475: [Your physical address for legal compliance]  # Required for GDPR/CCPA
```

#### In BOT_SUMMARY.md and legal_text.py:
- Update contact information if different from @ludicegifter
- Add support email if available
- Update "Last Updated" dates

### Step 2: Add Legal Router to Bot

In `frontend/app.py`, import and include the legal router:

```python
from routers.legal_router import legal_router

# ... existing code ...

dp.include_router(legal_router)  # Add this line
dp.include_router(start_router)
dp.include_router(game_router)
```

### Step 3: Implement Terms Acceptance for New Users

Modify your `/start` command in `frontend/routers/private_user.py`:

```python
from routers.legal_router import show_terms_acceptance

@start_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Check if user has accepted terms (you'll need database check)
    has_accepted = await check_user_acceptance(user_id)  # TODO: Implement

    if not has_accepted:
        await show_terms_acceptance(message, state)
        return

    # Regular start flow
    await message.answer("Welcome to Ludicé bot. Choose an option:", reply_markup=start.start_kb)
```

### Step 4: Add Gambling Reminder Before Games

In your game start handlers:

```python
from routers.legal_router import show_gambling_reminder

@game_router.message(F.text == "Dice 🎲")
async def play_dice(message: types.Message, state: FSMContext):
    # Show responsible gambling reminder
    await show_gambling_reminder(message)

    await message.answer("🎲 You chose to play Dice! What amount are you willing to bet?")
    await state.set_state(Form.waiting_for_bet)
```

### Step 5: Store Terms Acceptance in Database

You need to track terms acceptance. Add to your database schema:

```python
# Example database model (adjust for your DB)
class UserTermsAcceptance:
    user_id: int  # Telegram user ID
    username: str
    accepted_at: datetime
    version: str  # e.g., "2025-01"
    ip_address: str  # Optional
    age_verified: bool
```

Implement storage in `callback_accept_terms()` in legal_router.py:

```python
@legal_router.callback_query(F.data == "accept_terms")
async def callback_accept_terms(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    username = callback.from_user.username or "Unknown"

    # Store in your database
    await your_database.store_acceptance(
        user_id=user_id,
        username=username,
        accepted_at=datetime.now(),
        version="2025-01",
        age_verified=True
    )

    # ... rest of the function
```

## 📋 Available Bot Commands

After integration, users can use:

- `/terms` - View Terms of Service
- `/privacy` - View Privacy Policy
- `/gambling` - View Responsible Gambling policy
- `/help` or `/support` - Contact information
- `/fairplay` - Fair Play policy
- `/refund` or `/withdrawal` - Refund policy

## ⚖️ Legal Compliance Checklist

Before going live, ensure:

### Required Actions:
- [ ] Update jurisdiction/governing law in Terms (Section 15)
- [ ] Add physical address in Privacy Policy (for GDPR/CCPA)
- [ ] Specify server locations in Privacy Policy
- [ ] Implement database storage for terms acceptance
- [ ] Set up age verification workflow
- [ ] Review with legal counsel (HIGHLY RECOMMENDED)

### Recommended Actions:
- [ ] Add support email address
- [ ] Set up data export functionality
- [ ] Implement account deletion workflow
- [ ] Create self-exclusion database table
- [ ] Set up automated "Last Updated" date tracking
- [ ] Add terms version tracking

### Testing:
- [ ] Test terms acceptance flow for new users
- [ ] Test all /commands (terms, privacy, gambling, etc.)
- [ ] Verify all inline buttons work
- [ ] Test terms decline workflow
- [ ] Test age verification (if implemented)

## 🌍 International Compliance

### GDPR (EU Users)
- ✅ Data collection transparency
- ✅ User rights (access, deletion, portability)
- ✅ Lawful basis for processing
- ⚠️ **ACTION REQUIRED**: Designate Data Protection Officer if needed
- ⚠️ **ACTION REQUIRED**: Register with supervisory authority if required

### CCPA (California Users)
- ✅ Disclosure of data collection
- ✅ Right to know and delete
- ✅ No selling of personal information
- ⚠️ **ACTION REQUIRED**: Add "Do Not Sell My Info" link if collecting CA user data

### Gambling Regulations
- ✅ 18+ age requirement
- ✅ Responsible gambling resources
- ✅ Self-exclusion program
- ⚠️ **ACTION REQUIRED**: Verify compliance with local gambling laws
- ⚠️ **ACTION REQUIRED**: May need gambling license depending on jurisdiction

## 🔄 Updating Legal Documents

When you update legal documents:

1. **Update the Document**
   - Modify TERMS_OF_SERVICE.md, PRIVACY_POLICY.md, or RESPONSIBLE_GAMBLING.md
   - Update "Last Updated" date

2. **Update Bot Text**
   - Update corresponding text in `frontend/common/legal_text.py`
   - Update BOT_SUMMARY.md

3. **Notify Users**
   - Send in-bot notification to all users
   - Consider re-requiring acceptance for material changes

4. **Track Version**
   - Use version numbers (e.g., "2025-01", "2025-02")
   - Store which version each user accepted

## 📞 Support Setup

Ensure @ludicegifter Telegram account:
- Is monitored regularly
- Has staff trained on legal policies
- Can handle:
  - Account deletion requests
  - Data export requests
  - Self-exclusion requests
  - Privacy inquiries
  - Dispute resolution

## ⚠️ Legal Disclaimer

**IMPORTANT:** These documents are templates and should be reviewed by a qualified attorney before use. Requirements vary by:
- Jurisdiction
- User location
- Business structure
- Gambling laws
- Data protection regulations

**We strongly recommend** consulting with:
1. A lawyer specializing in online gambling
2. A privacy/data protection attorney
3. A regulatory compliance expert

## 📚 Additional Resources

- Telegram Bot Terms: https://core.telegram.org/bots/terms
- GDPR Resources: https://gdpr.eu/
- CCPA Guide: https://oag.ca.gov/privacy/ccpa
- Responsible Gambling Standards: https://www.responsiblegambling.org/
- Problem Gambling Resources: https://www.ncpgambling.org/

## 🆘 Getting Help

For questions about implementing these legal documents:
- Check the code comments in legal_router.py
- Review example implementations
- Consult the aiogram documentation for FSM and routers
- Seek legal counsel for compliance questions

---

**Last Updated:** January 2025

# After /start
TERMS_FULL = """
📋 **Ludicé - Terms of Service**

**1. ELIGIBILITY**
• Must be 18+ years old
• Valid Telegram account required
• Legal capacity to enter contracts

**2. GAME RULES**
• Dice game: highest roll wins
• Minimum bet: 10 Stars
• NO gaming commission - winners get 100%
• ~25% purchase fee when buying Stars
• Fair random results (Telegram system)

**3. PAYMENTS**
• Purchase Stars through Telegram
• Non-refundable (except errors/fraud)
• No cash value or conversion

**4. PROHIBITED CONDUCT**
• Cheating or collusion
• Multiple accounts
• Bots or automation
• Harassment or illegal activity

**5. LIABILITY**
• Service provided "as is"
• No guarantee of winnings
• Not responsible for Telegram outages

**6. TERMINATION**
• We may suspend accounts for violations
• You can delete your account anytime
• Balances handled per our policies

**📄 Full Terms**: 
**📞 Support**: @ludicegifter

Last Updated: January 2025
"""


def get_legal_text(key: str) -> str:
    """
    Get legal text by key.

    Args:
        key: One of the keys in LEGAL_TEXTS dictionary

    Returns:
        The corresponding legal text, or error message if key not found
    """
    return LEGAL_TEXTS.get(key, "Legal text not found. Contact @ludicegifter")

"""
Legal text for the Ludicé bot with multi-language support.
"""

# Default English Terms (fallback)
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

# Terms in different languages
LEGAL_TEXTS = {
    "en": TERMS_FULL,
    "ru": """
📋 **Ludicé - Условия обслуживания**

**1. ПРАВО НА УЧАСТИЕ**
• Должно быть 18+ лет
• Требуется действующий аккаунт Telegram
• Правоспособность заключать договоры

**2. ПРАВИЛА ИГРЫ**
• Игра в кости: побеждает самый высокий бросок
• Минимальная ставка: 10 звёзд
• БЕЗ комиссии за игру - победители получают 100%
• ~25% комиссия при покупке звёзд
• Честные случайные результаты (система Telegram)

**3. ПЛАТЕЖИ**
• Покупка звёзд через Telegram
• Невозвратные (кроме ошибок/мошенничества)
• Нет денежной стоимости или конвертации

**4. ЗАПРЕЩЕННОЕ ПОВЕДЕНИЕ**
• Обман или сговор
• Множественные аккаунты
• Боты или автоматизация
• Домогательства или незаконная деятельность

**5. ОТВЕТСТВЕННОСТЬ**
• Сервис предоставляется "как есть"
• Нет гарантии выигрыша
• Не несём ответственности за сбои Telegram

**6. ПРЕКРАЩЕНИЕ**
• Мы можем приостановить аккаунты за нарушения
• Вы можете удалить свой аккаунт в любое время
• Балансы обрабатываются согласно нашим правилам

**📄 Полные условия**:
**📞 Поддержка**: @ludicegifter

Последнее обновление: Январь 2025
""",
    "es": """
📋 **Ludicé - Términos de Servicio**

**1. ELEGIBILIDAD**
• Debe tener 18+ años
• Se requiere cuenta válida de Telegram
• Capacidad legal para celebrar contratos

**2. REGLAS DEL JUEGO**
• Juego de dados: gana la tirada más alta
• Apuesta mínima: 10 estrellas
• SIN comisión de juego - los ganadores obtienen el 100%
• ~25% de tarifa de compra al comprar estrellas
• Resultados aleatorios justos (sistema Telegram)

**3. PAGOS**
• Compra de estrellas a través de Telegram
• No reembolsable (excepto errores/fraude)
• Sin valor en efectivo o conversión

**4. CONDUCTA PROHIBIDA**
• Trampa o colusión
• Múltiples cuentas
• Bots o automatización
• Acoso o actividad ilegal

**5. RESPONSABILIDAD**
• Servicio proporcionado "tal cual"
• Sin garantía de ganancias
• No responsable de interrupciones de Telegram

**6. TERMINACIÓN**
• Podemos suspender cuentas por violaciones
• Puedes eliminar tu cuenta en cualquier momento
• Los saldos se manejan según nuestras políticas

**📄 Términos completos**:
**📞 Soporte**: @ludicegifter

Última actualización: Enero 2025
""",
    "fr": """
📋 **Ludicé - Conditions d'utilisation**

**1. ÉLIGIBILITÉ**
• Doit avoir 18 ans ou plus
• Compte Telegram valide requis
• Capacité légale de conclure des contrats

**2. RÈGLES DU JEU**
• Jeu de dés: le lancer le plus élevé gagne
• Mise minimale: 10 étoiles
• AUCUNE commission de jeu - les gagnants obtiennent 100%
• ~25% de frais d'achat lors de l'achat d'étoiles
• Résultats aléatoires équitables (système Telegram)

**3. PAIEMENTS**
• Achat d'étoiles via Telegram
• Non remboursable (sauf erreurs/fraude)
• Aucune valeur en espèces ou conversion

**4. CONDUITE INTERDITE**
• Triche ou collusion
• Comptes multiples
• Bots ou automation
• Harcèlement ou activité illégale

**5. RESPONSABILITÉ**
• Service fourni "tel quel"
• Aucune garantie de gains
• Pas responsable des pannes de Telegram

**6. RÉSILIATION**
• Nous pouvons suspendre les comptes pour violations
• Vous pouvez supprimer votre compte à tout moment
• Les soldes sont gérés selon nos politiques

**📄 Conditions complètes**:
**📞 Support**: @ludicegifter

Dernière mise à jour: Janvier 2025
"""
}


def get_legal_text(language: str = "en") -> str:
    """
    Get legal text in the specified language.

    Args:
        language: Language code (e.g., 'en', 'ru', 'es', 'fr')

    Returns:
        The terms of service text in the specified language
    """
    return LEGAL_TEXTS.get(language, LEGAL_TEXTS["en"])

"""
Context processors to make currency available in all templates
"""
from .currency_utils import get_user_currency


def currency_context(request):
    """Add currency information to template context"""
    if request.user.is_authenticated:
        currency = get_user_currency(request.user)
        return {
            'user_currency': currency['symbol'],
            'user_currency_code': currency['code'],
        }
    return {
        'user_currency': '$',
        'user_currency_code': 'USD',
    }






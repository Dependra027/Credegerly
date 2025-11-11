"""
Template tags for currency formatting
"""
from django import template
from ..currency_utils import format_currency, get_user_currency

register = template.Library()


@register.filter
def currency(value, user=None):
    """Format value as currency"""
    if value is None:
        value = 0
    
    currency_symbol = '$'  # Default fallback
    
    # Try to get currency from user object
    if user:
        # Check if it's a User object
        if hasattr(user, 'is_authenticated'):
            if user.is_authenticated:
                try:
                    currency_info = get_user_currency(user)
                    currency_symbol = currency_info['symbol']
                except Exception as e:
                    # If profile doesn't exist, get_user_currency will create it
                    try:
                        currency_info = get_user_currency(user)
                        currency_symbol = currency_info['symbol']
                    except Exception:
                        pass
        # Check if it's a request object
        elif hasattr(user, 'user'):
            if hasattr(user.user, 'is_authenticated') and user.user.is_authenticated:
                try:
                    currency_info = get_user_currency(user.user)
                    currency_symbol = currency_info['symbol']
                except Exception:
                    pass
    
    return format_currency(value, currency_symbol)


@register.filter
def currency_simple(value):
    """Format value as currency using context processor's user_currency"""
    if value is None:
        value = 0
    # This will use the user_currency from context processor
    # We'll format it in the template directly
    return value


@register.simple_tag
def currency_symbol(user=None):
    """Get currency symbol for user"""
    if user and user.is_authenticated:
        currency_info = get_user_currency(user)
        return currency_info['symbol']
    return '$'


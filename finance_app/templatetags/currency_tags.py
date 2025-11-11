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
    
    # Handle both user object and request object
    if hasattr(user, 'is_authenticated') and user.is_authenticated:
        currency_info = get_user_currency(user)
        return format_currency(value, currency_info['symbol'])
    elif hasattr(user, 'user') and hasattr(user.user, 'is_authenticated') and user.user.is_authenticated:
        # If passed request object
        currency_info = get_user_currency(user.user)
        return format_currency(value, currency_info['symbol'])
    else:
        # Fallback to context processor value or default
        return format_currency(value, '$')


@register.simple_tag
def currency_symbol(user=None):
    """Get currency symbol for user"""
    if user and user.is_authenticated:
        currency_info = get_user_currency(user)
        return currency_info['symbol']
    return '$'


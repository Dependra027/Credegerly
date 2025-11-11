"""
Currency utility functions for formatting and conversion
"""
from .models import UserProfile


def get_user_currency(user):
    """Get currency information for a user"""
    try:
        profile = user.profile
        return {
            'code': profile.currency_code,
            'symbol': profile.currency_symbol,
        }
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(
            user=user,
            country='US',
            currency_code='USD',
            currency_symbol='$'
        )
        return {
            'code': profile.currency_code,
            'symbol': profile.currency_symbol,
        }


def format_currency(amount, currency_symbol='$', decimal_places=2):
    """Format amount with currency symbol"""
    if amount is None:
        amount = 0
    
    # Format number with proper decimal places
    formatted_amount = f"{float(amount):,.{decimal_places}f}"
    
    # Handle currencies with symbol after amount
    if currency_symbol in ['€', '£', '¥', '₹', '₽', '₺']:
        return f"{formatted_amount} {currency_symbol}"
    else:
        return f"{currency_symbol}{formatted_amount}"


def get_currency_for_user(user):
    """Get currency symbol for user (for template use)"""
    currency = get_user_currency(user)
    return currency['symbol']






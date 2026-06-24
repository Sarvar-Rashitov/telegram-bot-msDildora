import random
import string
from datetime import datetime
from django.utils import timezone

def generate_referral_code(length=8):
    """Generate random referral code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def format_amount(amount):
    """Format amount with thousand separators"""
    return f"{amount:,.0f}"

def get_uzbek_date(dt):
    """Format date in Uzbek style"""
    if not dt:
        return "-"
    return dt.strftime("%d.%m.%Y")

def get_uzbek_datetime(dt):
    """Format datetime in Uzbek style"""
    if not dt:
        return "-"
    return dt.strftime("%d.%m.%Y %H:%M")

def days_until(target_date):
    """Calculate days until target date"""
    if not target_date:
        return None
    now = timezone.now()
    delta = target_date - now
    return delta.days

def is_subscription_active(subscription):
    """Check if subscription is active"""
    if not subscription:
        return False
    return subscription.status == 'active' and subscription.end_date > timezone.now()

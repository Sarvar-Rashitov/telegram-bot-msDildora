import uuid
from django.conf import settings
from .models import Payment

def create_payment(user, subscription, amount):
    """Create new payment"""
    merchant_trans_id = str(uuid.uuid4())
    
    payment = Payment.objects.create(
        user=user,
        subscription=subscription,
        amount=amount,
        merchant_trans_id=merchant_trans_id,
        status='pending'
    )
    
    # Generate Click payment URL
    payment_url = (
        f"https://my.click.uz/services/pay?"
        f"service_id={settings.CLICK_SERVICE_ID}"
        f"&merchant_id={settings.CLICK_MERCHANT_ID}"
        f"&amount={amount}"
        f"&transaction_param={merchant_trans_id}"
    )
    
    payment.payment_url = payment_url
    payment.save()
    
    return payment

def check_payment_status(merchant_trans_id):
    """Check payment status"""
    try:
        payment = Payment.objects.get(merchant_trans_id=merchant_trans_id)
        return payment.status
    except Payment.DoesNotExist:
        return None

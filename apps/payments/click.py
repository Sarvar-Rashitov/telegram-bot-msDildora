import hashlib
from django.conf import settings
from .models import Payment

class ClickService:
    @staticmethod
    def generate_hash(data):
        """Generate Click hash for validation"""
        text = (
            f"{data['click_trans_id']}"
            f"{data['service_id']}"
            f"{settings.CLICK_SECRET_KEY}"
            f"{data['merchant_trans_id']}"
            f"{data['amount']}"
            f"{data['action']}"
            f"{data['sign_time']}"
        )
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def validate_request(data):
        """Validate Click request"""
        expected_hash = ClickService.generate_hash(data)
        return expected_hash == data.get('sign_string')
    
    @staticmethod
    def prepare_payment(data):
        """Handle Click prepare request"""
        if not ClickService.validate_request(data):
            return {'error': -1, 'error_note': 'Invalid signature'}
        
        try:
            payment = Payment.objects.get(merchant_trans_id=data['merchant_trans_id'])
            
            if payment.status == 'success':
                return {'error': -4, 'error_note': 'Already paid'}
            
            if float(data['amount']) != float(payment.amount):
                return {'error': -2, 'error_note': 'Incorrect amount'}
            
            payment.click_trans_id = data['click_trans_id']
            payment.click_paydoc_id = data['click_paydoc_id']
            payment.status = 'processing'
            payment.save()
            
            return {
                'error': 0,
                'error_note': 'Success',
                'click_trans_id': data['click_trans_id'],
                'merchant_trans_id': data['merchant_trans_id'],
                'merchant_prepare_id': payment.id
            }
        except Payment.DoesNotExist:
            return {'error': -5, 'error_note': 'Order not found'}
    
    @staticmethod
    def complete_payment(data):
        """Handle Click complete request"""
        if not ClickService.validate_request(data):
            return {'error': -1, 'error_note': 'Invalid signature'}
        
        try:
            payment = Payment.objects.get(merchant_trans_id=data['merchant_trans_id'])
            
            if data['error'] < 0:
                payment.status = 'failed'
                payment.error_note = data.get('error_note', 'Payment failed')
                payment.save()
                return {'error': -9, 'error_note': 'Transaction cancelled'}
            
            payment.status = 'success'
            payment.save()
            
            # Activate subscription here
            if payment.subscription:
                from datetime import timedelta
                from django.utils import timezone
                
                subscription = payment.subscription
                subscription.status = 'active'
                subscription.start_date = timezone.now()
                subscription.end_date = timezone.now() + timedelta(days=subscription.tariff.duration_days)
                subscription.save()
            
            return {
                'error': 0,
                'error_note': 'Success',
                'click_trans_id': data['click_trans_id'],
                'merchant_trans_id': data['merchant_trans_id'],
                'merchant_confirm_id': payment.id
            }
        except Payment.DoesNotExist:
            return {'error': -5, 'error_note': 'Order not found'}

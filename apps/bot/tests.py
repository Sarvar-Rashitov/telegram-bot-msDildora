from django.test import TestCase
from apps.users.models import User
from apps.subscriptions.models import Tariff, Subscription
from apps.payments.models import Payment

class BotTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            telegram_id=123456789
        )
        self.tariff = Tariff.objects.create(
            name='Test Tariff',
            price=50000,
            duration_days=30
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.telegram_id, 123456789)
    
    def test_subscription_creation(self):
        subscription = Subscription.objects.create(
            user=self.user,
            tariff=self.tariff,
            status='pending'
        )
        self.assertEqual(subscription.status, 'pending')
    
    def test_payment_creation(self):
        subscription = Subscription.objects.create(
            user=self.user,
            tariff=self.tariff
        )
        payment = Payment.objects.create(
            user=self.user,
            subscription=subscription,
            amount=50000,
            merchant_trans_id='test123'
        )
        self.assertEqual(payment.status, 'pending')

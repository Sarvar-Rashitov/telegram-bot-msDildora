from django.db import models
from apps.users.models import User
from apps.subscriptions.models import Subscription

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Jarayonda'),
        ('success', 'Muvaffaqiyatli'),
        ('failed', 'Muvaffaqiyatsiz'),
        ('refunded', 'Qaytarilgan'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    click_trans_id = models.CharField(max_length=100, blank=True)
    click_paydoc_id = models.CharField(max_length=100, blank=True)
    merchant_trans_id = models.CharField(max_length=100, unique=True)
    payment_url = models.URLField(blank=True)
    error_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'To\'lov'
        verbose_name_plural = 'To\'lovlar'
    
    def __str__(self):
        return f"Payment {self.merchant_trans_id} - {self.amount}"

from django.db import models
from apps.users.models import User

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('user_created', 'Foydalanuvchi yaratildi'),
        ('subscription_created', 'Obuna yaratildi'),
        ('payment_completed', 'To\'lov amalga oshirildi'),
        ('channel_joined', 'Kanalga qo\'shildi'),
        ('broadcast_sent', 'Xabar yuborildi'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

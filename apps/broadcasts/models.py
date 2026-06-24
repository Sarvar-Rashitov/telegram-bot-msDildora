from django.db import models
from apps.users.models import User

class Broadcast(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('scheduled', 'Rejalashtirilgan'),
        ('sending', 'Yuborilmoqda'),
        ('completed', 'Tugallangan'),
        ('failed', 'Muvaffaqiyatsiz'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    image = models.ImageField(upload_to='broadcasts/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    target_all = models.BooleanField(default=True)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'broadcasts'
        verbose_name = 'Xabar yuborish'
        verbose_name_plural = 'Xabar yuborishlar'
    
    def __str__(self):
        return self.title

from django.db import models
from apps.users.models import User

class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Ochiq'),
        ('in_progress', 'Jarayonda'),
        ('resolved', 'Hal qilindi'),
        ('closed', 'Yopildi'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    admin_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'support_tickets'
        verbose_name = 'Murojaat'
        verbose_name_plural = 'Murojaatlar'
    
    def __str__(self):
        return f"{self.user.username} - {self.subject}"

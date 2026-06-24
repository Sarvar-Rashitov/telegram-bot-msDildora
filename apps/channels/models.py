from django.db import models

class TelegramChannel(models.Model):
    name = models.CharField(max_length=200)
    channel_id = models.BigIntegerField(unique=True)
    invite_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    member_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'telegram_channels'
        verbose_name = 'Kanal'
        verbose_name_plural = 'Kanallar'
    
    def __str__(self):
        return f"{self.name} ({self.channel_id})"

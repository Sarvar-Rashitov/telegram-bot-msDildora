from django.db import models

class BotSettings(models.Model):
    """Bot uchun sozlamalar - admin panelda boshqariladi"""
    key = models.CharField(max_length=100, unique=True, verbose_name="Kalit")
    value = models.TextField(verbose_name="Qiymat", blank=True)
    file = models.FileField(upload_to='bot_files/', null=True, blank=True, verbose_name="Fayl")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bot_settings'
        verbose_name = 'Bot Sozlama'
        verbose_name_plural = 'Bot Sozlamalari'
    
    def __str__(self):
        return self.key

class ContactInfo(models.Model):
    """Yordam bo'limi kontaktlari"""
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    contact_type = models.CharField(
        max_length=20, 
        choices=[
            ('phone', 'Telefon'),
            ('telegram', 'Telegram'),
            ('email', 'Email'),
            ('other', 'Boshqa')
        ],
        verbose_name="Tur"
    )
    value = models.CharField(max_length=255, verbose_name="Qiymat")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'contact_info'
        verbose_name = 'Kontakt'
        verbose_name_plural = 'Kontaktlar'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.title} - {self.value}"

class BotInfo(models.Model):
    """Bot haqida ma'lumotlar"""
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Mazmun")
    image = models.ImageField(upload_to='bot_info/', null=True, blank=True, verbose_name="Rasm")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bot_info'
        verbose_name = 'Ma\'lumot'
        verbose_name_plural = 'Ma\'lumotlar'
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.title

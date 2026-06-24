from django.contrib import admin
from .models import TelegramChannel

@admin.register(TelegramChannel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel_id', 'member_count', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'channel_id']

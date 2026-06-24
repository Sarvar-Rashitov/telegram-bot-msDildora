from django.contrib import admin
from .models import Broadcast

@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'sent_count', 'failed_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title']

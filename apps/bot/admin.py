from django.contrib import admin
from .models import BotSettings, ContactInfo, BotInfo

@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'description', 'updated_at']
    search_fields = ['key', 'description']
    readonly_fields = ['updated_at']

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'contact_type', 'value', 'is_active', 'order']
    list_filter = ['contact_type', 'is_active']
    search_fields = ['title', 'value']
    list_editable = ['is_active', 'order']

@admin.register(BotInfo)
class BotInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title', 'content']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at', 'updated_at']

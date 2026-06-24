from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'telegram_id', 'phone', 'is_blocked', 'created_at']
    list_filter = ['is_blocked', 'language', 'created_at']
    search_fields = ['username', 'telegram_id', 'phone']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Telegram', {'fields': ('telegram_id', 'phone', 'language', 'referral_code', 'referred_by', 'is_blocked')}),
    )

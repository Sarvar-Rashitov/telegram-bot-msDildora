from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'telegram_id', 'phone', 'is_registered', 'is_blocked', 'created_at']
    list_filter = ['is_registered', 'is_blocked', 'language', 'created_at']
    search_fields = ['username', 'telegram_id', 'phone', 'first_name', 'last_name']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Telegram Ma\'lumotlari', {
            'fields': ('telegram_id', 'telegram_username', 'phone', 'language')
        }),
        ('Shaxsiy Ma\'lumotlar', {
            'fields': ('age', 'occupation', 'is_registered')
        }),
        ('Referal', {
            'fields': ('referral_code', 'referred_by', 'balance')
        }),
        ('Holat', {
            'fields': ('is_blocked',)
        }),
    )
    
    def get_queryset(self, request):
        """Registered va unregistered userlarni ajratish"""
        qs = super().get_queryset(request)
        return qs

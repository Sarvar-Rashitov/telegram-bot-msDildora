from django.contrib import admin
from .models import Tariff, Subscription, PromoCode

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_days', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'tariff', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'is_trial', 'created_at']
    search_fields = ['user__username', 'user__telegram_id']

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'usage_limit', 'used_count', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code']

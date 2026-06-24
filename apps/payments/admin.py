from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['merchant_trans_id', 'user', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['merchant_trans_id', 'click_trans_id', 'user__username']
    readonly_fields = ['created_at', 'updated_at']

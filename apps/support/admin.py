from django.contrib import admin
from .models import SupportTicket

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'subject']

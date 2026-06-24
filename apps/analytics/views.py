from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User
from apps.subscriptions.models import Subscription
from apps.payments.models import Payment
from .models import AuditLog

@login_required
def analytics_dashboard(request):
    today = timezone.now().date()
    
    stats = {
        'total_users': User.objects.count(),
        'active_subscriptions': Subscription.objects.filter(status='active').count(),
        'today_payments': Payment.objects.filter(created_at__date=today, status='success').count(),
        'today_revenue': Payment.objects.filter(created_at__date=today, status='success').aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_revenue': Payment.objects.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0,
    }
    
    total_users = stats['total_users']
    subscribed_users = Subscription.objects.filter(status='active').values('user').distinct().count()
    stats['conversion_rate'] = (subscribed_users / total_users * 100) if total_users > 0 else 0
    
    recent_logs = AuditLog.objects.select_related('user').order_by('-created_at')[:20]
    
    return render(request, 'analytics/dashboard.html', {
        'stats': stats,
        'recent_logs': recent_logs
    })

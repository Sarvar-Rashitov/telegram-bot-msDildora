from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from apps.users.models import User
from apps.subscriptions.models import Subscription
from apps.payments.models import Payment
from django.db.models import Sum, Count

@login_required
@require_http_methods(["GET"])
def get_stats(request):
    """Get platform statistics"""
    total_users = User.objects.count()
    active_subscriptions = Subscription.objects.filter(status='active').count()
    total_revenue = Payment.objects.filter(status='success').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    return JsonResponse({
        'total_users': total_users,
        'active_subscriptions': active_subscriptions,
        'total_revenue': float(total_revenue),
    })

@login_required
@require_http_methods(["GET"])
def get_users(request):
    """Get users list"""
    users = User.objects.all().values(
        'id', 'username', 'telegram_id', 'created_at'
    )[:100]
    return JsonResponse({'users': list(users)})

@login_required
@require_http_methods(["GET"])
def get_subscriptions(request):
    """Get subscriptions list"""
    subscriptions = Subscription.objects.select_related(
        'user', 'tariff'
    ).values(
        'id', 'user__username', 'tariff__name', 'status', 'start_date', 'end_date'
    )[:100]
    return JsonResponse({'subscriptions': list(subscriptions)})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum, Count
from .models import Payment
import csv
from datetime import datetime, timedelta

@login_required
def payment_list(request):
    payments = Payment.objects.select_related('user', 'subscription__tariff').order_by('-created_at')
    
    # Filterlar
    status = request.GET.get('status')
    search = request.GET.get('search')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if status:
        payments = payments.filter(status=status)
    
    if search:
        payments = payments.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(transaction_id__icontains=search)
        )
    
    if date_from:
        payments = payments.filter(created_at__gte=date_from)
    
    if date_to:
        payments = payments.filter(created_at__lte=date_to)
    
    # Statistika
    stats = {
        'total_count': payments.count(),
        'success_count': payments.filter(status='success').count(),
        'pending_count': payments.filter(status='pending').count(),
        'total_amount': payments.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0,
    }
    
    context = {
        'payments': payments[:100],  # Pagination uchun
        'stats': stats,
        'status_filter': status,
        'search_query': search,
    }
    
    return render(request, 'payments/list.html', context)

@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment.objects.select_related('user', 'subscription__tariff'), pk=pk)
    return render(request, 'payments/detail.html', {'payment': payment})

@login_required
def payment_export(request):
    """To'lovlarni CSV sifatida export qilish"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="payments_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'User', 'Amount', 'Status', 'Transaction ID', 'Date'])
    
    payments = Payment.objects.select_related('user').order_by('-created_at')
    
    for payment in payments:
        writer.writerow([
            payment.id,
            payment.user.username,
            payment.amount,
            payment.status,
            payment.transaction_id,
            payment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response

@csrf_exempt
def click_prepare(request):
    from .click import ClickService
    data = request.POST.dict() if request.method == 'POST' else request.GET.dict()
    result = ClickService.prepare_payment(data)
    return JsonResponse(result)

@csrf_exempt
def click_complete(request):
    from .click import ClickService
    data = request.POST.dict() if request.method == 'POST' else request.GET.dict()
    result = ClickService.complete_payment(data)
    return JsonResponse(result)

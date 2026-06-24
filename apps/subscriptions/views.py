from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Subscription, Tariff, PromoCode
from datetime import timedelta

@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.select_related('user', 'tariff').order_by('-created_at')
    
    # Filterlar
    status = request.GET.get('status')
    search = request.GET.get('search')
    
    if status:
        subscriptions = subscriptions.filter(status=status)
    
    if search:
        subscriptions = subscriptions.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(tariff__name__icontains=search)
        )
    
    # Statistika
    stats = {
        'total': subscriptions.count(),
        'active': subscriptions.filter(status='active').count(),
        'pending': subscriptions.filter(status='pending').count(),
        'expired': subscriptions.filter(status='expired').count(),
    }
    
    context = {
        'subscriptions': subscriptions[:100],
        'stats': stats,
        'status_filter': status,
        'search_query': search or '',
    }
    
    return render(request, 'subscriptions/list.html', context)

@login_required
def subscription_detail(request, pk):
    subscription = get_object_or_404(
        Subscription.objects.select_related('user', 'tariff'),
        pk=pk
    )
    payments = subscription.payments.all().order_by('-created_at')
    
    context = {
        'subscription': subscription,
        'payments': payments,
    }
    
    return render(request, 'subscriptions/detail.html', context)

@login_required
def subscription_activate(request, pk):
    """Obunani aktivlashtirish"""
    subscription = get_object_or_404(Subscription, pk=pk)
    
    if subscription.status == 'pending':
        subscription.status = 'active'
        subscription.start_date = timezone.now()
        subscription.end_date = timezone.now() + timedelta(days=subscription.tariff.duration_days)
        subscription.save()
        messages.success(request, 'Obuna aktivlashtirildi')
    else:
        messages.error(request, 'Faqat pending obunalarni aktivlashtirish mumkin')
    
    return redirect('subscriptions:subscription_detail', pk=pk)

@login_required
def subscription_cancel(request, pk):
    """Obunani bekor qilish"""
    subscription = get_object_or_404(Subscription, pk=pk)
    
    subscription.status = 'cancelled'
    subscription.save()
    messages.success(request, 'Obuna bekor qilindi')
    
    return redirect('subscriptions:subscription_detail', pk=pk)

# Tariffs
@login_required
def tariff_list(request):
    tariffs = Tariff.objects.annotate(
        subscription_count=Count('subscriptions')
    ).order_by('-created_at')
    
    return render(request, 'subscriptions/tariffs.html', {'tariffs': tariffs})

@login_required
def tariff_create(request):
    if request.method == 'POST':
        tariff = Tariff.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description', ''),
            price=request.POST.get('price'),
            duration_days=request.POST.get('duration_days'),
            is_active=request.POST.get('is_active') == 'on'
        )
        messages.success(request, 'Tarif yaratildi')
        return redirect('subscriptions:tariff_list')
    
    return render(request, 'subscriptions/tariff_form.html')

@login_required
def tariff_edit(request, pk):
    tariff = get_object_or_404(Tariff, pk=pk)
    
    if request.method == 'POST':
        tariff.name = request.POST.get('name')
        tariff.description = request.POST.get('description', '')
        tariff.price = request.POST.get('price')
        tariff.duration_days = request.POST.get('duration_days')
        tariff.is_active = request.POST.get('is_active') == 'on'
        tariff.save()
        
        messages.success(request, 'Tarif yangilandi')
        return redirect('subscriptions:tariff_list')
    
    return render(request, 'subscriptions/tariff_form.html', {'tariff': tariff})

@login_required
def tariff_delete(request, pk):
    tariff = get_object_or_404(Tariff, pk=pk)
    
    if tariff.subscriptions.exists():
        messages.error(request, 'Bu tarifda obunalar bor, o\'chirib bo\'lmaydi!')
        return redirect('subscriptions:tariff_list')
    
    tariff.delete()
    messages.success(request, 'Tarif o\'chirildi')
    return redirect('subscriptions:tariff_list')

# Promo Codes
@login_required
def promo_list(request):
    promos = PromoCode.objects.annotate(
        used_count_actual=Count('subscriptions')
    ).order_by('-created_at')
    
    return render(request, 'subscriptions/promo_list.html', {'promos': promos})

@login_required
def promo_create(request):
    if request.method == 'POST':
        PromoCode.objects.create(
            code=request.POST.get('code').upper(),
            discount_percent=request.POST.get('discount_percent', 0),
            discount_amount=request.POST.get('discount_amount', 0),
            usage_limit=request.POST.get('usage_limit', 1),
            is_active=request.POST.get('is_active') == 'on'
        )
        messages.success(request, 'Promo kod yaratildi')
        return redirect('subscriptions:promo_list')
    
    return render(request, 'subscriptions/promo_form.html')

@login_required
def promo_edit(request, pk):
    promo = get_object_or_404(PromoCode, pk=pk)
    
    if request.method == 'POST':
        promo.code = request.POST.get('code').upper()
        promo.discount_percent = request.POST.get('discount_percent', 0)
        promo.discount_amount = request.POST.get('discount_amount', 0)
        promo.usage_limit = request.POST.get('usage_limit', 1)
        promo.is_active = request.POST.get('is_active') == 'on'
        promo.save()
        
        messages.success(request, 'Promo kod yangilandi')
        return redirect('subscriptions:promo_list')
    
    return render(request, 'subscriptions/promo_form.html', {'promo': promo})

@login_required
def promo_toggle(request, pk):
    """Promo kodni aktiv/noaktiv qilish"""
    promo = get_object_or_404(PromoCode, pk=pk)
    promo.is_active = not promo.is_active
    promo.save()
    
    status = 'aktivlashtirildi' if promo.is_active else 'o\'chirildi'
    messages.success(request, f'Promo kod {status}')
    
    return redirect('subscriptions:promo_list')

@login_required
def promo_delete(request, pk):
    promo = get_object_or_404(PromoCode, pk=pk)
    promo.delete()
    messages.success(request, 'Promo kod o\'chirildi')
    return redirect('subscriptions:promo_list')

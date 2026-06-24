from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subscription, Tariff, PromoCode

@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.select_related('user', 'tariff').order_by('-created_at')
    return render(request, 'subscriptions/list.html', {'subscriptions': subscriptions})

@login_required
def tariff_list(request):
    tariffs = Tariff.objects.all().order_by('-created_at')
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
    tariff.delete()
    messages.success(request, 'Tarif o\'chirildi')
    return redirect('subscriptions:tariff_list')

@login_required
def promo_list(request):
    promos = PromoCode.objects.all().order_by('-created_at')
    return render(request, 'subscriptions/promo_list.html', {'promos': promos})

@login_required
def promo_create(request):
    if request.method == 'POST':
        PromoCode.objects.create(
            code=request.POST.get('code'),
            discount_percent=request.POST.get('discount_percent', 0),
            discount_amount=request.POST.get('discount_amount', 0),
            usage_limit=request.POST.get('usage_limit', 1),
            is_active=request.POST.get('is_active') == 'on'
        )
        messages.success(request, 'Promo kod yaratildi')
        return redirect('subscriptions:promo_list')
    
    return render(request, 'subscriptions/promo_form.html')

@login_required
def promo_delete(request, pk):
    promo = get_object_or_404(PromoCode, pk=pk)
    promo.delete()
    messages.success(request, 'Promo kod o\'chirildi')
    return redirect('subscriptions:promo_list')

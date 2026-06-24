from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from .models import User
from apps.subscriptions.models import Subscription
from apps.payments.models import Payment
from apps.support.models import SupportTicket

@login_required
def dashboard(request):
    today = timezone.now().date()
    
    # Staff foydalanuvchilarni hisoblashdan o'chiramiz
    stats = {
        'total_users': User.objects.filter(is_staff=False).count(),
        'active_subscriptions': Subscription.objects.filter(status='active').count(),
        'today_revenue': Payment.objects.filter(created_at__date=today, status='success').aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_revenue': Payment.objects.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0,
        'pending_tickets': SupportTicket.objects.filter(status='open').count(),
        'today_payments': Payment.objects.filter(created_at__date=today, status='success').count(),
    }
    
    recent_users = User.objects.filter(is_staff=False).order_by('-created_at')[:5]
    recent_payments = Payment.objects.select_related('user').order_by('-created_at')[:5]
    
    return render(request, 'dashboard/index.html', {
        'stats': stats,
        'recent_users': recent_users,
        'recent_payments': recent_payments
    })

@login_required
def user_list(request):
    # Staff foydalanuvchilarni ko'rsatma
    users = User.objects.filter(is_staff=False)
    
    # Search
    search = request.GET.get('search', '')
    if search:
        users = users.filter(
            username__icontains=search
        ) | users.filter(
            telegram_id__icontains=search
        ) | users.filter(
            phone__icontains=search
        )
    
    users = users.order_by('-created_at')
    return render(request, 'users/list.html', {'users': users, 'search': search})

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Staff foydalanuvchi ko'rinmasin (o'z profilini ko'rish qoladi)
    if user.is_staff and user.id != request.user.id:
        messages.error(request, 'Ushbu foydalanuvchini ko\'ra olmaysiz')
        return redirect('users:user_list')
    
    return render(request, 'users/detail.html', {'user_obj': user})

@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Staff foydalanuvchini tahrirlashga ruxsat bermaymiz (o'z profilini tahrirlash qoladi)
    if user.is_staff and user.id != request.user.id:
        messages.error(request, 'Ushbu foydalanuvchini tahrirlaya olmaysiz')
        return redirect('users:user_list')
    
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.language = request.POST.get('language', 'uz')
        user.balance = request.POST.get('balance', user.balance)
        user.is_blocked = request.POST.get('is_blocked') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.save()
        
        messages.success(request, 'Foydalanuvchi yangilandi')
        return redirect('users:detail', pk=pk)
    
    return render(request, 'users/edit.html', {'user_obj': user})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.id != request.user.id:
        user.delete()
        messages.success(request, 'Foydalanuvchi o\'chirildi')
    else:
        messages.error(request, 'O\'zingizni o\'chira olmaysiz')
    return redirect('users:user_list')

@login_required
def user_add_balance(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        note = request.POST.get('note', '')
        
        user.balance += amount
        user.save()
        
        # Audit log
        from apps.analytics.models import AuditLog
        AuditLog.objects.create(
            user=request.user,
            action='user_created',
            description=f"Balansga {amount} so'm qo'shildi: {user.username}. Izoh: {note}"
        )
        
        messages.success(request, f"{amount} so'm balansga qo'shildi")
        return redirect('users:detail', pk=pk)
    
    return render(request, 'users/add_balance.html', {'user_obj': user})

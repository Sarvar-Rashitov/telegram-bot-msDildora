from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Broadcast
import subprocess

@login_required
def broadcast_list(request):
    broadcasts = Broadcast.objects.all().order_by('-created_at')
    return render(request, 'broadcasts/list.html', {'broadcasts': broadcasts})

@login_required
def broadcast_create(request):
    if request.method == 'POST':
        broadcast = Broadcast.objects.create(
            title=request.POST.get('title'),
            message=request.POST.get('message'),
            target_all=request.POST.get('target_all') == 'on',
            created_by=request.user
        )
        
        if 'image' in request.FILES:
            broadcast.image = request.FILES['image']
            broadcast.save()
        
        messages.success(request, 'Xabar yaratildi')
        return redirect('broadcasts:list')
    
    return render(request, 'broadcasts/form.html')

@login_required
def broadcast_detail(request, pk):
    broadcast = get_object_or_404(Broadcast, pk=pk)
    return render(request, 'broadcasts/detail.html', {'broadcast': broadcast})

@login_required
def broadcast_send(request, pk):
    """Broadcast yuborish"""
    broadcast = get_object_or_404(Broadcast, pk=pk)
    
    if broadcast.status != 'draft':
        messages.error(request, 'Bu xabar allaqachon yuborilgan yoki yuborilmoqda')
        return redirect('broadcasts:detail', pk=pk)
    
    try:
        # Management command orqali broadcast yuborish
        subprocess.Popen(['python', 'manage.py', 'send_broadcast', str(broadcast.id)])
        messages.success(request, 'Xabar yuborish boshlandi! Jarayon fonda davom etmoqda.')
    except Exception as e:
        messages.error(request, f'Xatolik: {e}')
    
    return redirect('broadcasts:detail', pk=pk)

@login_required
def broadcast_delete(request, pk):
    broadcast = get_object_or_404(Broadcast, pk=pk)
    broadcast.delete()
    messages.success(request, 'Xabar o\'chirildi')
    return redirect('broadcasts:list')

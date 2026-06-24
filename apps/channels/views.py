from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TelegramChannel

@login_required
def channel_list(request):
    channels = TelegramChannel.objects.all().order_by('-created_at')
    return render(request, 'channels/list.html', {'channels': channels})

@login_required
def channel_create(request):
    if request.method == 'POST':
        TelegramChannel.objects.create(
            name=request.POST.get('name'),
            channel_id=request.POST.get('channel_id'),
            invite_link=request.POST.get('invite_link', ''),
            description=request.POST.get('description', ''),
            is_active=request.POST.get('is_active') == 'on'
        )
        messages.success(request, 'Kanal qo\'shildi')
        return redirect('channels:list')
    
    return render(request, 'channels/form.html')

@login_required
def channel_edit(request, pk):
    channel = get_object_or_404(TelegramChannel, pk=pk)
    
    if request.method == 'POST':
        channel.name = request.POST.get('name')
        channel.channel_id = request.POST.get('channel_id')
        channel.invite_link = request.POST.get('invite_link', '')
        channel.description = request.POST.get('description', '')
        channel.is_active = request.POST.get('is_active') == 'on'
        channel.save()
        
        messages.success(request, 'Kanal yangilandi')
        return redirect('channels:list')
    
    return render(request, 'channels/form.html', {'channel': channel})

@login_required
def channel_delete(request, pk):
    channel = get_object_or_404(TelegramChannel, pk=pk)
    channel.delete()
    messages.success(request, 'Kanal o\'chirildi')
    return redirect('channels:list')

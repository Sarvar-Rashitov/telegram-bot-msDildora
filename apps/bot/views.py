from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from aiogram.types import Update
from aiogram import Bot
from .models import BotSettings, ContactInfo, BotInfo
from .forms import BotSettingsForm, ContactInfoForm, BotInfoForm

@login_required
def bot_settings_list(request):
    """Bot sozlamalari ro'yxati"""
    settings = BotSettings.objects.all()
    contacts = ContactInfo.objects.all().order_by('order')
    infos = BotInfo.objects.all().order_by('order')
    
    context = {
        'settings': settings,
        'contacts': contacts,
        'infos': infos,
    }
    return render(request, 'bot/settings_list.html', context)

@login_required
def bot_settings_edit(request, pk):
    """Bot sozlamani tahrirlash"""
    setting = get_object_or_404(BotSettings, pk=pk)
    
    if request.method == 'POST':
        form = BotSettingsForm(request.POST, request.FILES, instance=setting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sozlama yangilandi')
            return redirect('bot:settings_list')
    else:
        form = BotSettingsForm(instance=setting)
    
    return render(request, 'bot/settings_form.html', {'form': form, 'setting': setting})

@login_required
def contact_create(request):
    """Yangi kontakt qo'shish"""
    if request.method == 'POST':
        form = ContactInfoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kontakt qo\'shildi')
            return redirect('bot:settings_list')
    else:
        form = ContactInfoForm()
    
    return render(request, 'bot/contact_form.html', {'form': form})

@login_required
def contact_edit(request, pk):
    """Kontaktni tahrirlash"""
    contact = get_object_or_404(ContactInfo, pk=pk)
    
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kontakt yangilandi')
            return redirect('bot:settings_list')
    else:
        form = ContactInfoForm(instance=contact)
    
    return render(request, 'bot/contact_form.html', {'form': form, 'contact': contact})

@login_required
def contact_delete(request, pk):
    """Kontaktni o'chirish"""
    contact = get_object_or_404(ContactInfo, pk=pk)
    contact.delete()
    messages.success(request, 'Kontakt o\'chirildi')
    return redirect('bot:settings_list')

@login_required
def info_create(request):
    """Yangi ma'lumot qo'shish"""
    if request.method == 'POST':
        form = BotInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ma\'lumot qo\'shildi')
            return redirect('bot:settings_list')
    else:
        form = BotInfoForm()
    
    return render(request, 'bot/info_form.html', {'form': form})

@login_required
def info_edit(request, pk):
    """Ma'lumotni tahrirlash"""
    info = get_object_or_404(BotInfo, pk=pk)
    
    if request.method == 'POST':
        form = BotInfoForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ma\'lumot yangilandi')
            return redirect('bot:settings_list')
    else:
        form = BotInfoForm(instance=info)
    
    return render(request, 'bot/info_form.html', {'form': form, 'info': info})

@login_required
def info_delete(request, pk):
    """Ma'lumotni o'chirish"""
    info = get_object_or_404(BotInfo, pk=pk)
    info.delete()
    messages.success(request, 'Ma\'lumot o\'chirildi')
    return redirect('bot:settings_list')


# Telegram Bot Webhook (Production)
@csrf_exempt
async def telegram_webhook(request):
    """Telegram webhook endpoint - har safar yangi Bot instance"""
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)
    
    try:
        import logging
        logger = logging.getLogger(__name__)
        
        update_data = json.loads(request.body)
        update_id = update_data.get('update_id')
        logger.info(f"📨 Update qabul qilindi: {update_id}")
        
        from .bot import dp
        
        # Yangi Bot instance (har safar yangi session)
        webhook_bot = Bot(token=settings.BOT_TOKEN)
        
        update = Update(**update_data)
        await dp.feed_update(webhook_bot, update)
        
        # Session yopish
        await webhook_bot.session.close()
        
        logger.info(f"✅ Update qayta ishlandi: {update_id}")
        return JsonResponse({'ok': True})
    except json.JSONDecodeError as e:
        import logging
        logging.getLogger(__name__).error(f"JSON xatosi: {e}")
        return JsonResponse({'ok': False}, status=400)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"❌ Webhook xatosi: {e}", exc_info=True)
        return JsonResponse({'ok': False}, status=500)
